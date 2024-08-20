import os
import csv
import datetime

from apogee_connect_rpi.Helpers.liveDataTypes import liveDataTypes
from apogee_connect_rpi.Scripts.AppConfig import AppConfig

class CsvManager:
    def __init__(self):
        config = AppConfig()
        self.precision = config.get_precision()
    
    def write_to_csv(self, timestamp, live_data, sensor, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        file_exists = os.path.isfile(filename)

        if not file_exists:
            self.create_csv(sensor, filename)

        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')

            datetime = self.convert_timestamp_dattime(timestamp)
            truncated_values = [datetime] + [self.truncate_float(value, self.precision) for value in live_data]
            writer.writerow(truncated_values)
    
    def create_csv(self, sensor, filename, appending = False):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        file_exists = os.path.isfile(filename)

        if file_exists and appending:
            print("Appending data to existing file")
            return
        
        if file_exists and not appending:
            overwrite = input(f"\nThe file '{filename}' already exists. If you want to append to the existing file, use the flag '-a' with your collect command.\nDo you want to overwrite it? [Y/N]: ")
            if overwrite.lower() != 'y':
                print("File not overwritten. Exiting command.")
                exit(1)
            else:
                print("Overwriting file")
            
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            labels_with_units = ["Timestamp"] + [self.format_label_with_units(label) for label in sensor.live_data_labels]
            writer.writerow(labels_with_units)

    #
    # HELPERS
    #        
    def format_label_with_units(self, label):
        if label in liveDataTypes:
            units = liveDataTypes[label]["units"]
            return f"{label} ({units})"
        else:
            return label
    
    def truncate_float(self, value, precision=2):
        return f"{value:.{precision}f}"
    
    def convert_timestamp_dattime(self, timestamp):
        return datetime.datetime.fromtimestamp(timestamp).strftime('%c')