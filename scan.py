import os
import platform

class Scanner:
    def __init__(self):
        self.candidates = []
        self.total_size = 0

    def get_paths(self):
        """Returns a list of paths to scan based on OS."""
        paths = []
        system = platform.system()
        
        if system == "Windows":
            # Common Windows junk locations
            paths.append(os.environ.get('TEMP')) # User Temp
            paths.append(os.path.join(os.environ.get('SystemRoot'), 'Temp')) # System Temp
        else:
            # Linux/Mac paths
            paths.append('/tmp')
            paths.append(os.path.expanduser('~/.cache'))
            
        return [p for p in paths if p and os.path.exists(p)]

    def scan_system(self):
        """Scans directories and returns file list and total size."""
        self.candidates = []
        self.total_size = 0
        search_paths = self.get_paths()

        for folder in search_paths:
            try:
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        filepath = os.path.join(root, file)
                        try:
                            size = os.path.getsize(filepath)
                            self.candidates.append((filepath, size))
                            self.total_size += size
                        except OSError:
                            continue # Skip files we can't read
            except PermissionError:
                continue
        
        return self.candidates, self.total_size