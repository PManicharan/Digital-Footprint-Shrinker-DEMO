import os

class Cleaner:
    def remove_files(self, file_list):
        """Deletes files provided in the list."""
        deleted_count = 0
        recovered_space = 0
        
        for filepath, size in file_list:
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
                    deleted_count += 1
                    recovered_space += size
            except Exception as e:
                # Skip files that are currently in use by Windows
                continue
                
        return deleted_count, recovered_space