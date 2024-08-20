#!/usr/bin/env python3

import asyncio
import argparse
import sys
import re
from textwrap import dedent
from apogee_connect_rpi.Scripts.CommandImplement import CommandImplement
from apogee_connect_rpi.version import __version__

class Main:
    def __init__(self):
        self.commandImplement = CommandImplement()

        self.parser = argparse.ArgumentParser(
            description='Apogee Connect for Raspberry Pi',
            usage=dedent('''
                Intract with Apogee bluetooth sensors for automatic data collection
                         
                Available Commands:
                collect    Collect data from a sensor
                config     Change or read app configuration
                list       Show a list of currently collecting sensors
                scan       Scan for nearby sensors
                stop       Stop data collection for a sensor
            '''))
        
        self.parser.add_argument('command', help='Any command from the above list may be used')
        self.parser.add_argument('-v', '--version', action='version', version=__version__, help='Show version number of application')

        args = self.parser.parse_args(sys.argv[1:2])

        # Make sure there is a command
        if not hasattr(self, args.command):
            print('Unrecognized command')
            self.parser.print_help()
            exit(1)

        # Run command asynchronously
        asyncio.run(self.dispatch_command(args.command))
    
    async def dispatch_command(self, command):
        # Get the primary command and check if there is function in this class with a matching name
        await getattr(self, command)()

    #
    # COMMANDS
    #   
    async def collect(self):
        parser = argparse.ArgumentParser(description='Collect data from an Apogee sensor via bluetooth')
        parser.add_argument('address', type=self._mac_address,
                            help='MAC address of sensor in the format of XX:XX:XX:XX:XX:XX')
        parser.add_argument('-i', '--interval', metavar='INTERVAL', type=self._positive_int, default=5,
                            help="Collect data every INTERVAL minutes (must be a positive integer)")
        parser.add_argument('-s', '--start', metavar='START', type=self._positive_int,
                            help="Start time for data collection using epoch time (Unix timestamp in seconds)")
        parser.add_argument('-e', '--end', metavar='END', type=self._positive_int,
                            help="End time for data collection using epoch time (Unix timestamp in seconds)")
        parser.add_argument('-f', '--file', metavar='FILE', type=str,
                            help="Filepath to write data to csv file")
        parser.add_argument('-a', '--append', action='store_true',
                            help="Append to file instead of overwriting")
        args = parser.parse_args(sys.argv[2:])

        await self.commandImplement.collect(args)
        
    async def config(self):
        parser = argparse.ArgumentParser(description='Collect data from an Apogee sensor via bluetooth')
        parser.add_argument('-p', '--precision', metavar='PRECISION', type=self._positive_int,
                            help="Change the maximum number of decimals displayed for data")
        parser.add_argument('-f', '--filepath', metavar='FILEPATH', type=str,
                            help="The default folder to save collected data.")
        parser.add_argument('-t', '--temp', metavar='TEMP', type=self._valid_temp,
                            help="Change preferred temperature units. Enter “C” for Celsius and “F” for Fahrenheit (without quotations).")
        parser.add_argument('-pf', '--par-filtering', metavar='PAR_FILTERING', type=self._adaptable_bool,
                            help='Filter negative PAR (PPFD) values to compensate for sensor "noise" in low-light conditions. Enter "True" or "False" (without quotations)')
        args = parser.parse_args(sys.argv[2:])

        await self.commandImplement.config(args)

    async def list(self):
        parser = argparse.ArgumentParser(description='Show list of Apogee bluetooth sensors that are currently collecting data')
        args = parser.parse_args(sys.argv[2:])

        await self.commandImplement.list()

    async def scan(self):
        parser = argparse.ArgumentParser(description='Scan for nearby Apogee bluetooth sensors')
        parser.add_argument('-t', '--time', metavar='TIME', type=self._positive_int,
                            help="Scan for TIME seconds")
        args = parser.parse_args(sys.argv[2:])

        await self.commandImplement.scan(args)

    async def stop(self):
        parser = argparse.ArgumentParser(description='Stop data collection from an Apogee sensor via bluetooth')
        parser.add_argument('address', type=self._mac_address,
                            help='MAC address of sensor in the format of XX:XX:XX:XX:XX:XX')
        parser.add_argument('-e', '--end', metavar='END', type=self._positive_int,
                            help="End time for data collection using epoch time (Unix timestamp in seconds)")
        args = parser.parse_args(sys.argv[2:])

        await self.commandImplement.stop(args)

    # This function is only intended to be run by crontab command on a schedule, never by a user, thus the longer command name
    async def run_data_collection(self):
        parser = argparse.ArgumentParser(description='Private command run by crontab scheduler')
        parser.add_argument('address', type=self._mac_address,
                            help='MAC address of sensor in the format of XX:XX:XX:XX:XX:XX')
        parser.add_argument('--file', metavar='FILE', type=str,
                            help="The default folder to save collected data.")
        parser.add_argument('--id', metavar='ID', type=int,
                            help="ID of sensor")
        parser.add_argument('-s', '--start', metavar='START', type=int,
                            help="Start time for data collection using epoch time (Unix timestamp in seconds)")
        parser.add_argument('-e', '--end', metavar='END', type=int,
                            help="End time for data collection using epoch time (Unix timestamp in seconds)")
        
        args = parser.parse_args(sys.argv[2:])

        await self.commandImplement.run_data_collection(args)

    #
    # CUSTOM DATA TYPES
    #   
    def _positive_int(self, value):
        try:
            ivalue = int(value)
            if ivalue <= 0:
                raise argparse.ArgumentTypeError(f"{value} is not a positive integer")
            return ivalue
        except ValueError:
            raise argparse.ArgumentTypeError(f"{value} is not a valid integer")

    def _mac_address(self, value):
        pattern = re.compile("^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$")
        if not pattern.match(value):
            raise argparse.ArgumentTypeError(f"{value} is not a valid MAC address. Format must follow XX:XX:XX:XX:XX:XX")
        return value
    
    def _valid_temp(self, value):
        if value.upper() not in ['C', 'F']:
            raise argparse.ArgumentTypeError(f"Invalid temperature unit '{value}'. Must be 'C' or 'F'.")
        return value.upper()
    
    def _adaptable_bool(self, value):
        if value.lower() in ('true', '1', 't'):
            return True
        elif value.lower() in ('false', '0', 'f'):
            return False
        else:
            raise argparse.ArgumentTypeError(f"Boolean value expected (true/false), got '{value}'.")

#
# MAIN
#  
def main():
    Main()

if __name__ == '__main__':
    main()