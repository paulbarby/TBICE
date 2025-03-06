import os
import time
import sqlite3
from PyQt6.QtCore import QThread, pyqtSignal
from database.db_manager import Database

class FolderWatcher(QThread):
    file_found = pyqtSignal(str, int)  # filepath, profile_id
    
    def __init__(self, db: Database, parent=None):
        super().__init__(parent)
        self.db = db
        self.db_path = db.db_path  # Store path to create thread-safe connection later
        self.thread_db = None  # This will hold our thread's database connection
        self.running = False
        self.profiles = {}
        self.processed_files = set()
        self.reload_profiles()
    
    def reload_profiles(self):
        profiles = self.db.get_profiles()
        self.profiles = {p['id']: p for p in profiles if p['is_active']}
        
    def create_thread_db(self):
        """Create a thread-specific database connection"""
        if self.thread_db is not None:
            # Close existing connection if there is one
            try:
                self.thread_db.close()
            except:
                pass
        
        # Create a new connection for this thread
        self.thread_db = sqlite3.connect(self.db_path)
        # Enable foreign keys
        cursor = self.thread_db.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        
    def load_processed_files_from_main(self, processed_files_list):
        """Load processed files from a list provided by the main thread"""
        self.processed_files.clear()
        for file_path in processed_files_list:
            self.processed_files.add(file_path)
    
    def load_processed_files(self):
        """Load processed files from database - ONLY CALL FROM WATCHER THREAD"""
        # This method should only be called from the run() method
        # or other methods running in the watcher thread
        if not self.isRunning():
            return  # Skip if not running in the thread
            
        if not self.thread_db:
            # Create connection if it doesn't exist
            self.create_thread_db()
            
        self.processed_files.clear()
        # Get all processed files for active profiles
        for profile_id in self.profiles.keys():
            try:
                cursor = self.thread_db.cursor()
                cursor.execute('''
                SELECT source_path FROM processed_files WHERE profile_id = ?
                ''', (profile_id,))
                
                files = [row[0] for row in cursor.fetchall()]
                for file_path in files:
                    self.processed_files.add(file_path)
            except sqlite3.Error as e:
                print(f"SQLite error in load_processed_files: {e}")
    
    def run(self):
        self.running = True
        
        # Create a thread-specific database connection
        self.create_thread_db()
        
        # Load processed files from database when starting
        self.load_processed_files()
        
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
        
        # Close the thread-specific database connection
        if self.thread_db:
            try:
                self.thread_db.close()
                self.thread_db = None
            except:
                pass