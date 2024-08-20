from crontab import CronTab
import os
import re
import subprocess

class CronManager:
    def __init__(self):
        self.cron = CronTab(user=True)

    async def setup_crontab_command(self, interval: int, address, start_time, end_time, sensorID, filename):
        if not start_time:
            start_time = 0
        if not end_time:
            end_time = 4294967295

        if self.get_cron_job(address):
            raise RuntimeError("A task is already scheduled for a sensor with the given address. Run the 'stop' command to remove that job.")

        command = self.create_cron_job_command(address, start_time, end_time, sensorID, filename)
        job = self.cron.new(command=command)
        job.minute.every(interval)
        self.cron.write()

    def create_cron_job_command(self, address, start_time, end_time, sensorID, filename):
        home_dir = os.path.expanduser("~")
        log_dir = os.path.join(home_dir, "Apogee", "apogee_connect_rpi", "logs")
        os.makedirs(log_dir, exist_ok=True)

        executable_path = self.get_executable("apogee", home_dir)

        command = f"{executable_path} run_data_collection {address} --file {filename} --id {sensorID} --start {start_time} --end {end_time} >> {log_dir}/ac_rpi.log 2>&1"
        return command

    def remove_crontab_job(self, address):
        print("Removing scheduled data collection")
        job = self.get_cron_job(address)
        if job:
            self.cron.remove(job)
            self.cron.write()

    def change_crontab_job_endtime(self, address, end_time):
        job = self.get_cron_job(address)
        if(job):
            command = job.command

            # Find and replace the command's end time
            new_command = re.sub(r'--end \d+', f'--end {end_time}', command)
            job.set_command(new_command)
            self.cron.write()
            print(f"Data collection end time successfully updated to: {end_time}")
        else:
            print(f"Error setting data collection end time. Please check address and try again.")

    def get_cron_job(self, address):
        for job in self.cron:
            # Add the 'run_data_collection' before the address to avoid the one-in-a-million chance that the address string is found in something like a filepath for a different sensor
            if f"run_data_collection {address}" in job.command:
                return job
        return None
    
    def get_executable(self, command_name, home_dir) -> str:
        # Most likely location
        executable_path = f"{home_dir}/.local/bin/apogee"

        if not os.path.isfile(executable_path):
            # Second most likely location
            executable_path = f"{home_dir}/.local/pipx/bin/apogee"

        if not os.path.isfile(executable_path):
            # Try to check for the location programmatically
            result = subprocess.run(['which', command_name], capture_output=True, text=True)
            if result.returncode == 0:
                executable_path = result.stdout.strip()
            else:
                raise RuntimeError(f"Could not find executable location. Please make sure 'apogee' executable is located at: {home_dir}/.local/bin/apogee or is part of $PATH") 

        return executable_path