import json
import os

class AppConfig:
    _instance = None 

    # Singleton
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            script_dir = os.path.dirname(os.path.realpath(__file__))
            parent_dir = os.path.dirname(script_dir)
            cls._instance.config_file = os.path.join(parent_dir, 'json/AppConfig.json')
            cls._instance.config = cls._instance.load_config()
        return cls._instance

    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
            
        except FileNotFoundError:
            print(f"Config file '{self.config_file}' not found. Using default settings.")
            return{}

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def print_config(self):
        print(json.dumps(self.config, indent=4))
            
    #
    # PRECISION
    #
    def get_precision(self):
        return self.config.get('precision', 2)

    def set_precision(self, precision: int):
        self.config['precision'] = precision
        self.save_config()

    #
    # UNITS
    #
    def get_temp_units(self):
        return self.config.get('units', {}).get('temperature')

    def set_temp_units(self, unit):
        if unit not in ["C", "F"]:
            raise ValueError("Unit must be 'C' (Celsius) or 'F' (Fahrenheit)")

        if 'units' not in self.config:
            self.config['units'] = {}
        self.config['units']['temperature'] = unit
        self.save_config()

    #
    # PAR FILTERING
    #
    def get_par_filtering(self):
        return self.config.get('par_filter', False)
    
    def set_par_filtering(self, enabled: bool):
        self.config['par_filter'] = enabled
        self.save_config()

    #
    # FILEPATH
    #
    def get_default_filepath(self):
        if 'default_path' in self.config:
            return self.config['default_path']
        
        home_dir = os.path.expanduser("~")
        return os.path.join(home_dir, "Apogee", "apogee_connect_rpi", "data")

    def set_default_filepath(self, path: str):
        self.config['default_path'] = path
        self.save_config()

    