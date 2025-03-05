import os
import time
from PyQt6.QtCore import QThread, pyqtSignal
from database.db_manager import Database

class FolderWatcher(QThread):
    file_found = pyqtSignal(str, int)  # filepath, profile_id
    
    def __init__(self, db: Database, parent=None):
        super().__init__(parent)
        self.db = db
        self.running = False
        self.profiles = {}
        self.processed_files = set()
        self.reload_profiles()
    
    def reload_profiles(self):
        profiles = self.db.get_profiles()
        self.profiles = {p['id']: p for p in profiles if p['is_active']}
    
    def run(self):
        self.running = True
        
        while self.running:
            for profile_id, profile in self.profiles.items():
                if not self.running:
                    break
                    
                source_folder = profile['source_folder']
                if not os.path.exists(source_folder):
                    continue
                
                # Check for new files
                for filename in os.listdir(source_folder):
                    if not self.running:
                        break
                        
                    file_path = os.path.join(source_folder, filename)
                    
                    # Skip directories and non-image files
                    if os.path.isdir(file_path):
                        continue
                        
                    # Check file extension
                    ext = os.path.splitext(filename)[1].lower()
                    if ext not in ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.ico'):
                        continue
                    
                    # Check if already processed
                    if file_path in self.processed_files:
                        continue
                    
                    # Emit signal for processing
                    self.file_found.emit(file_path, profile_id)
                    self.processed_files.add(file_path)
            
            # Sleep to avoid high CPU usage
            time.sleep(1)
    
    def stop(self):
        self.running = False