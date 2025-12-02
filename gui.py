import tkinter as tk
from tkinter import messagebox, scrolledtext
from scan import Scanner
from backup import BackupModule
from cleaner import Cleaner
from reporter import Reporter

class PrivacyToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Footprint Shrinker")
        self.root.geometry("600x500")
        
        # Initialize Modules
        self.scanner = Scanner()
        self.backup_mod = BackupModule()
        self.cleaner = Cleaner()
        self.reporter = Reporter()
        
        self.candidates = []
        self.total_size = 0

        # UI Elements
        self.label_title = tk.Label(root, text="Digital Footprint Shrinker", font=("Arial", 16, "bold"))
        self.label_title.pack(pady=10)

        self.btn_scan = tk.Button(root, text="1. Scan System", command=self.run_scan, bg="#3498db", fg="white", width=20)
        self.btn_scan.pack(pady=5)
        
        self.label_score = tk.Label(root, text="Current Privacy Score: Unknown", font=("Arial", 12))
        self.label_score.pack(pady=5)

        self.log_area = scrolledtext.ScrolledText(root, width=70, height=15)
        self.log_area.pack(pady=10)

        self.btn_clean = tk.Button(root, text="2. Backup & Clean", command=self.run_clean, bg="#e74c3c", fg="white", width=20, state=tk.DISABLED)
        self.btn_clean.pack(pady=5)

    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)

    def calculate_score(self, size_bytes):
        # Simple logic: More junk = Lower score
        # If junk > 1GB, score is 0. If 0 junk, score is 100.
        size_mb = size_bytes / (1024 * 1024)
        score = max(0, 100 - int(size_mb / 10)) 
        return score

    def run_scan(self):
        self.log("Scanning system for privacy traces... Please wait.")
        self.root.update()
        
        self.candidates, self.total_size = self.scanner.scan_system()
        
        count = len(self.candidates)
        mb_size = round(self.total_size / (1024*1024), 2)
        
        self.current_score = self.calculate_score(self.total_size)
        
        self.log(f"Scan Complete. Found {count} files.")
        self.log(f"Total Size: {mb_size} MB")
        self.label_score.config(text=f"Privacy Score: {self.current_score}/100 (Low is bad)")
        
        if count > 0:
            self.btn_clean.config(state=tk.NORMAL)
        else:
            self.log("System is clean!")

    def run_clean(self):
        if not messagebox.askyesno("Confirm", "Are you sure? Files will be backed up before deletion."):
            return

        self.log("Starting Backup...")
        self.root.update()
        backup_path, backed_up_count = self.backup_mod.perform_backup(self.candidates)
        self.log(f"Backup created at: {backup_path}")

        self.log("Cleaning files...")
        self.root.update()
        deleted_count, recovered_space = self.cleaner.remove_files(self.candidates)
        
        new_score = 100 # Assuming clean
        self.log(f"Cleanup Complete. Removed {deleted_count} files.")
        
        self.reporter.generate_html(deleted_count, recovered_space, backup_path, self.current_score, new_score)
        self.log("Report generated and opened in browser.")
        
        self.candidates = []
        self.btn_clean.config(state=tk.DISABLED)
        self.label_score.config(text=f"Privacy Score: {new_score}/100")

if __name__ == "__main__":
    root = tk.Tk()
    app = PrivacyToolApp(root)
    root.mainloop()