import json
import os

# Class to assist with storing which sensors are currently collecting data
class SensorManager:
    _instance = None

    # Singleton
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.path.dirname(script_dir)
        self.storage_file = os.path.join(parent_dir, 'json/CollectingSensors.json')
        self._sensor_list = self._load_sensor_list()

    def _load_sensor_list(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
                return data
        else:
            return []

    def _save_sensor_list(self):
        with open(self.storage_file, 'w') as f:
            json.dump(self._sensor_list, f, indent=4)

    def add_sensor(self, address: str, sensor_id: int, interval: int, start_time: int, end_time: int, filename: str):       
        if address not in self._sensor_list:
            info = {
                "interval": interval,
                "start_time": start_time if start_time is not None else "None",
                "end_time": end_time if end_time is not None else "None", 
                "logs": 0,
                "file": filename 
            }

            self._sensor_list[address] = info
            self._save_sensor_list()

    def remove_sensor(self, address):
        if address in self._sensor_list:
            del self._sensor_list[address]
            self._save_sensor_list()

    def get_sensor_list_length(self):
        return len(self._sensor_list)

    def sensor_already_collecting(self, address):
        return address in self._sensor_list
    
    def increment_collected_logs(self, address):
        if address in self._sensor_list:
            sensor_info = self._sensor_list[address]
            sensor_info["logs"] += 1
            self._save_sensor_list()
    
    def print_collecting_sensor_list(self):
        print("\n*Currently Collecting Sensors*")
        
        # Print the header row
        headers = ["Address", "Logs", "Interval", "Start Time", "End Time", "File"]
        print("{:^17} | {:^6} | {:^8} | {:^10} | {:^10} | {:^5}".format(*headers))

        # Print the row separator
        print('-' * 18 + '+' + '-' * 8 + '+' + '-' * 10 + '+' + '-' * 12 + '+' + '-' * 12 + '+' + '-' * 6)
        
        # Print the data rows
        for address, details in self._sensor_list.items():
            print("{:<17} | {:<6} | {:<8} | {:<10} | {:<10} | {:<5}".format(
                address, 
                details['logs'], 
                details['interval'], 
                details['start_time'], 
                details['end_time'], 
                details['file']
            ))