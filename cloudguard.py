import os
import subprocess
import datetime
import platform

class CloudGuard:
    def __init__(self):
        if platform.system() != 'Windows':
            raise EnvironmentError("CloudGuard is only compatible with Windows operating system.")
        self.updates_scheduled = []
        self.update_list = self.check_for_updates()

    def check_for_updates(self):
        """Check for available Windows updates."""
        print("Checking for available Windows updates...")
        try:
            result = subprocess.run(['powershell', '-Command', 'Get-WindowsUpdate'], capture_output=True, text=True)
            updates = result.stdout.splitlines()
            print("Available updates:")
            for update in updates:
                print(update)
            return updates
        except Exception as e:
            print(f"An error occurred while checking for updates: {e}")
            return []

    def schedule_update(self, update_name, date_time):
        """Schedule a specific update to be installed at a given time."""
        if update_name not in self.update_list:
            print(f"Update '{update_name}' not found.")
            return
        try:
            scheduled_time = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
            self.updates_scheduled.append((update_name, scheduled_time))
            print(f"Update '{update_name}' scheduled for {scheduled_time}.")
        except ValueError:
            print("Incorrect date-time format. Use YYYY-MM-DD HH:MM:SS")

    def execute_scheduled_updates(self):
        """Execute the scheduled updates."""
        current_time = datetime.datetime.now()
        for update, scheduled_time in self.updates_scheduled:
            if current_time >= scheduled_time:
                print(f"Installing update: {update}")
                try:
                    subprocess.run(['powershell', '-Command', f'Install-WindowsUpdate -KBArticleID {update} -AcceptAll'], check=True)
                    print(f"Update '{update}' installed successfully.")
                except subprocess.CalledProcessError as e:
                    print(f"An error occurred while installing update '{update}': {e}")

    def list_scheduled_updates(self):
        """List all scheduled updates."""
        if not self.updates_scheduled:
            print("No updates scheduled.")
            return
        print("Scheduled updates:")
        for update, scheduled_time in self.updates_scheduled:
            print(f"{update} at {scheduled_time}")

# Example usage:
if __name__ == "__main__":
    cloudguard = CloudGuard()
    cloudguard.schedule_update("KB1234567", "2023-12-01 14:00:00")
    cloudguard.list_scheduled_updates()
    cloudguard.execute_scheduled_updates()