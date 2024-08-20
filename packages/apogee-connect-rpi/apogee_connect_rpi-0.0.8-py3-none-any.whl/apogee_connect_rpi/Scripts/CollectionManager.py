import bleak
import struct
import asyncio  
import datetime

from apogee_connect_rpi.Scripts.SensorClasses import *
from apogee_connect_rpi.Helpers.ApogeeUuids import *
from apogee_connect_rpi.Scripts.SensorManager import SensorManager
from apogee_connect_rpi.Scripts.CronManager import CronManager
from apogee_connect_rpi.Scripts.CsvManager import CsvManager


class CollectionManager:
    def __init__(self, address: str, filename: str):
        self.address = address
        self.filename = filename
        self.sampling_interval_const = 15
        self.sensor = None
        self.bleak_client = None 

        self.sensorManager = SensorManager()
        self.cronManager = CronManager()
        self.fileManager = CsvManager()

    #
    # SENSOR CONNECTION
    #
    async def connect(self):
        if not self.bleak_client:
            try: 
                print(f"Connecting to sensor {self.address}")
                self.bleak_client = bleak.BleakClient(self.address)
                await self.bleak_client.connect()

            except asyncio.TimeoutError as e:
                print(f"Could not connect to sensor {self.address}. {e}")
                exit(1)

            except bleak.BleakError as e:
                print(f"Could not connect to sensor {self.address}. {e}")
                exit(1)

    async def disconnect(self):
        if self.bleak_client:
            try:
                await self.bleak_client.disconnect()
                self.bleak_client = None
            
            except bleak.BleakError as e:
                print(f"Could not disconnect from sensor {self.address}. {e}")
                exit(1)

    #
    # INITIATE COLLECTION
    #
    async def collect_live_data(self, interval: int, start_time, end_time, appending):
        await self.connect()
        await self.populate_sensor_info()
        await self.check_sensor_time()

        if self.sensor is None:
            print("Error retrieving sensor information")
            return

        self.fileManager.create_csv(self.sensor, self.filename, appending)
 
        try:            
            # Set last timestamp transferred to current time to avoid getting old data
            await self.set_last_timestamp_transferred()

            # Configure data logging settings and turn logging on 
            bytearray_data = self.get_logging_bytearray(interval, start_time, end_time)
            await self.initiate_logging(bytearray_data)

            if self.sensor.type == "Guardian":
                await self.cronManager.setup_crontab_command(interval, self.address, start_time, end_time, self.sensor.sensorID, self.filename)
            else:
                # For mCache, it will try to connect every minute so it doesn't have to figure out how to line up with firmware in the event of an abnormal interval
                await self.cronManager.setup_crontab_command(1, self.address, start_time, end_time, self.sensor.sensorID, self.filename)
                await self.turn_on_gateway_mode()

            # Add sensor to list of currently collecting sensors
            self.sensorManager.add_sensor(self.sensor.address, self.sensor.sensorID, interval, start_time, end_time, self.filename)

            print(f"Data collection continuing in background. Logs will be collected at {self.filename}. \nThis terminal may be closed.")

        except bleak.BleakError as e:
            print(f"Error retrieving sensor data: {e}")
        
        except RuntimeError as e:
            print(e)
            await self.stop_data_collection()
            
        await self.disconnect()
    
    async def turn_on_gateway_mode(self):
        await self.bleak_client.write_gatt_char(dataLogCollectionRateUUID, bytearray([1]), True)

    async def turn_off_gateway_mode(self):
        await self.bleak_client.write_gatt_char(dataLogCollectionRateUUID, bytearray([0]), True)
                  

    async def set_last_timestamp_transferred(self):
        current_time_epoch = int(datetime.datetime.now().timestamp())
        await self.bleak_client.write_gatt_char(lastTransferredTimestampUUID, bytearray(struct.pack('<I', current_time_epoch)), True)

    def get_logging_bytearray(self, interval: int, start_time, end_time):
        logging_interval = interval * 60 # Convert to minutes
        data_array = [self.sampling_interval_const, logging_interval]

        # Determine need to set a custom start/end time
        if start_time:
            data_array.append(start_time)
        if end_time:
            if not start_time:
                data_array.append(0) # Add a 0 for start time if there is an end time but no start time
            data_array.append(end_time)

        # Convert array to bytearray for gatt characteristic
        bytearray_data = bytearray()
        for num in data_array:
            bytearray_data.extend(struct.pack('<I', num)) 
        
        return bytearray_data

    async def check_sensor_time(self):
        data = await self.bleak_client.read_gatt_char(currentTimeUUID)
        data_packet = bytes(data)
        sensor_time = struct.unpack('<I', data_packet[:4])[0]

        current_time_epoch = int(datetime.datetime.now().timestamp())

        # Update time on sensor if more than a minute off
        time_difference = abs(current_time_epoch - sensor_time)
        if time_difference > 60:
            print("Updating time on sensor")
            await self.bleak_client.write_gatt_char(currentTimeUUID, bytearray(struct.pack('<I', current_time_epoch)), True)      

    async def initiate_logging(self, bytearray_data):
        # Start data logging
        print("Starting data collection...")
        await self.bleak_client.write_gatt_char(dataLoggingIntervalsUUID, bytearray_data, True)
        await self.bleak_client.write_gatt_char(dataLoggingControlUUID, bytearray([1]), True)

    async def populate_sensor_info(self):
        await self.connect()

        try:
            print("Getting sensor info")
            sensorID_data = await self.bleak_client.read_gatt_char(sensorIDUUID)
            hw_data = await self.bleak_client.read_gatt_char(hardwareVersionUUID)
            fw_data = await self.bleak_client.read_gatt_char(firmwareVersionUUID)

            sensorID = int.from_bytes(sensorID_data, byteorder='little', signed=False)           
            hw = int(hw_data.decode('utf-8'))
            fw = int(fw_data.decode('utf-8'))

            self.sensor = get_sensor_class_from_ID(sensorID, self.address)

            if not self.sensor.compatibleFirmware(int(hw), int(fw)):
                print("Firmware needs to be updated in order to be compatible with this application")
                exit(1)
        
        except bleak.BleakError as e:
            print(f"Error getting sensor info, {e}")
            exit(1)

    #
    # DATA COLLECTION
    #
    async def run_data_collection(self, sensorID):
        await self.align_data_collection()

        await self.connect()
        self.sensor = get_sensor_class_from_ID(sensorID, self.address)

        print(f'Collecting data from {self.address}' )
        try:
            data = await self.bleak_client.read_gatt_char(dataLogTransferUUID)
            self.handle_live_data(data)

        except asyncio.TimeoutError as e:
                print(f"Could not connect to sensor {self.address}. {e}")
                exit(1)

        except bleak.BleakError as e:
            print(f"Could not connect to sensor {self.address}. {e}")
            exit(1)

        finally:
            await self.disconnect()

    def handle_live_data(self, data):
        data_packet = bytes(data)
        hex_representation = data_packet.hex()
        print(f"Received packet from {self.address}: {hex_representation}")

        # Ensure the data packet is complete or if it is just all "FF" indicating no data to collect
        if len(data_packet) < 8:
            print("No data to collect")
            return
        
        # Get packet header information
        timestamp = struct.unpack('<I', data_packet[:4])[0]
        intervalBetweenTimestamps = struct.unpack('<H', data_packet[4:6])[0]
        measurementsPerInterval = struct.unpack('<B', data_packet[6:7])[0]
                
        data = []
        # This loop should usually only run once, but just in case a collection is missed and there are multiple sets in packet
        # Separate packet into groups based on timestamp (e.g., groups of 5 datapoints for the Guardian, groups of 1 datapoint for microcache)
        for startIndex in range(8, len(data_packet) - 1, 4 * measurementsPerInterval):
            endIndex = min(startIndex + (4 * measurementsPerInterval), len(data_packet))
            groupedArray = data_packet[startIndex:endIndex]

            # Get each datapoint within the current timestamp
            data = []
            for i in range(0, len(groupedArray), 4):
                raw = struct.unpack('<i', groupedArray[i:(i + 4)])[0]

                # Divide by 10,000 to scale from ten-thousandths to ones
                dataValue = raw / 10000.0

                data.append(dataValue)

            # Calculate all live data based on specific sensor class
            live_data = self.sensor.calculate_live_data(data)

            self.fileManager.write_to_csv(timestamp, live_data, self.sensor, self.filename)
            self.sensorManager.increment_collected_logs(self.address)

            # Increment timestamp in case there are multiple logs in a single packet
            timestamp += intervalBetweenTimestamps

        return
    
    async def align_data_collection(self):
        # Data logs won't be available until two sampling intervals after the minute. So pause a little until they are ready
        current_time_epoch = int(datetime.datetime.now().timestamp())
        seconds_since_minute_start = current_time_epoch % 60

        if seconds_since_minute_start <= (self.sampling_interval_const * 2):
            await asyncio.sleep((self.sampling_interval_const * 30) - seconds_since_minute_start)

        print(f"\nTimestamp: {datetime.datetime.now()}")

    # 
    # STOP COLLECTION
    #
    async def stop_data_collection(self):
        while not self.bleak_client:
            await self.connect()
            await asyncio.sleep(1)

        self.cronManager.remove_crontab_job(self.address)
            
        print("Removing sensor from list")
        self.sensorManager.remove_sensor(self.address)

        print("Stopping Live Data")
        await self.bleak_client.write_gatt_char(dataLoggingControlUUID, bytearray([0]), True)

        await self.turn_off_gateway_mode()

        await self.disconnect()

    async def delayed_stop_data_collection(self, end_time: int):
        print("Updating data collection end time")
        self.cronManager.change_crontab_job_endtime(self.address, end_time)