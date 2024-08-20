import datetime
import asyncio

from apogee_connect_rpi.Scripts.BleScanner import BleScanner
from apogee_connect_rpi.Scripts.SensorManager import SensorManager
from apogee_connect_rpi.Scripts.CollectionManager import CollectionManager
from apogee_connect_rpi.Scripts.AppConfig import AppConfig

class CommandImplement:
    def __init__(self):
        self.sensorManager = SensorManager()

    # 
    # COLLECT
    #
    async def collect(self, args):
        address = args.address

        if self.already_collecting_sensor(address):
           print("Sensor is already collecting data")
           exit(0) 
        
        if self.max_sensors_reached():
            self.sensorManager.print_collecting_sensor_list()
            print("\nMaximum of 5 sensors already reached")
            exit(0)

        current_time_epoch = int(datetime.datetime.now().timestamp())
        start = args.start
        end = args.end
        if end:
            if (end <= start) or (end <= current_time_epoch):
                print("End time must be after the start time and the current time")
                exit(0)
        
        file = self.get_file(address, args.file)

        collectionManager = CollectionManager(address, file)

        await collectionManager.collect_live_data(args.interval, start, end, args.append)

    def already_collecting_sensor(self, address) -> bool:
        return self.sensorManager.sensor_already_collecting(address)
    
    def max_sensors_reached(self) -> bool:
        MAX_SENSORS = 5
        current_sensor_length = self.sensorManager.get_sensor_list_length()
        return current_sensor_length >= MAX_SENSORS
    
    def get_file(self, address, file) -> str:
        if file:
            return file
        else:
            path = AppConfig().get_default_filepath()
            return f'{path}/{address.replace(":","-")}.csv'

    # 
    # CONFIG
    #
    async def config(self, args):
        config = AppConfig()

        # Just print the config if no arguments included with command
        if all(arg is None for arg in vars(args).values()):
            config.print_config()
        else:
            self.update_config(config, args)

    def update_config(self, config: AppConfig, args):
        if args.precision is not None:
            config.set_precision(args.precision)
        
        if args.temp is not None:
            config.set_temp_units(args.temp)

        if args.par_filtering is not None:
            config.set_par_filtering(args.par_filtering)

        if args.folder is not None:
            config.set_default_filepath(args.filepath)

    #
    # LIST
    #
    async def list(self):
        self.sensorManager.print_collecting_sensor_list()

    #
    # SCAN
    #
    async def scan(self, args):
        scan_time = args.time
        run_until_no_missing_packets = False

        # If not scan time was set, run at least 5 seconds until no discovered sensors are missing packets
        if not scan_time:
            scan_time = 5
            run_until_no_missing_packets = True

        scanner = BleScanner(scan_time, run_until_no_missing_packets)
        await scanner.startScan()

    #
    # STOP
    #
    async def stop(self, args):
        address = args.address
        end_time = args.end 

        collectionManager = CollectionManager(address, "")

        if end_time:
            await collectionManager.delayed_stop_data_collection(end_time)
        else:
            await collectionManager.stop_data_collection()

    #
    # CRONTAB DATA COLLECTION
    #
    async def run_data_collection(self, args):
        address = args.address
        file = args.file
        sensorID = args.id
        start_time = args.start
        end_time = args.end
        current_time_epoch = int(datetime.datetime.now().timestamp())

        # Check if it is before/after set start/end time
        if current_time_epoch < start_time:        
            exit(0)

        collectionManager = CollectionManager(address, file)
        await collectionManager.run_data_collection(sensorID)

        # Don't run this until after the collection to ensure you still get the final datapoint
        if current_time_epoch >= end_time:
            args.end = None # Set to None so that the stop command stops immediately
            await self.stop(args)
            exit(0)