import os
import shutil
import datetime

class BackupModule:
    def __init__(self):
        self.backup_dir = "Backups"

    def create_backup_folder(self):
        """Creates a timestamped folder."""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
        
        timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        folder_path = os.path.join(self.backup_dir, timestamp)
        os.makedirs(folder_path)
        return folder_path

    def perform_backup(self, file_list):
        """Copies files to the backup folder."""
        dest_folder = self.create_backup_folder()
        backup_count = 0
        
        for filepath, size in file_list:
            try:
                # Copy file, preserving metadata
                if os.path.isfile(filepath):
                    shutil.copy2(filepath, dest_folder)
                    backup_count += 1
            except Exception as e:
                print(f"Backup Error for {filepath}: {e}")
                
        return dest_folder, backup_count