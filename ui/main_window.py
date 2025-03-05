import os
from datetime import datetime
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QIcon, QPixmap
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QPushButton, QLabel, QListWidget, QListWidgetItem, QMessageBox,
    QMenuBar
)

from database.db_manager import Database
from utils.folder_watcher import FolderWatcher
from utils.image_processor import ImageProcessor
from utils.style_helper import StyleHelper
from ui.profile_editor_dialog import ProfileEditorDialog
from ui.profile_list_item import ProfileListItem

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.db = Database()
        self.watcher = FolderWatcher(self.db)
        self.watcher.file_found.connect(self.process_file)
        
        self.is_monitoring = False
        
        self.setWindowTitle("Image Converter")
        self.setMinimumSize(1000, 700)
        
        # Set application icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "app-icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.setup_ui()
        self.setup_menu()
        
        # Apply iOS-inspired style
        self.setStyleSheet(StyleHelper.get_application_style())
        
        # Load profiles
        self.load_profiles()
    
    def setup_ui(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        
        # App icon and title
        title_layout = QHBoxLayout()
        
        # App icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "app-icon.png")
        if os.path.exists(icon_path):
            icon_label = QLabel()
            pixmap = QPixmap(icon_path).scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            icon_label.setPixmap(pixmap)
            title_layout.addWidget(icon_label)
        
        # App title
        title_label = QLabel("Image Converter")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #007aff;")
        title_layout.addWidget(title_label)
        title_layout.addStretch(1)
        
        header_layout.addLayout(title_layout)
        
        # Global control buttons
        self.start_btn = QPushButton("Start Monitoring")
        self.start_btn.setIcon(QIcon.fromTheme("media-playback-start"))
        self.start_btn.clicked.connect(self.toggle_monitoring)
        header_layout.addWidget(self.start_btn)
        
        add_profile_btn = QPushButton("New Profile")
        add_profile_btn.clicked.connect(self.add_profile)
        header_layout.addWidget(add_profile_btn)
        
        main_layout.addLayout(header_layout)
        
        # Status bar
        self.status_label = QLabel("Status: Idle")
        self.status_label.setStyleSheet("background-color: #f0f0f0; padding: 8px; border-radius: 4px;")
        main_layout.addWidget(self.status_label)
        
        # Profiles list
        profiles_group = QGroupBox("Conversion Profiles")
        profiles_layout = QVBoxLayout()
        
        self.profiles_list = QListWidget()
        self.profiles_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.profiles_list.setMinimumHeight(400)
        self.profiles_list.itemClicked.connect(self.on_profile_selected)
        profiles_layout.addWidget(self.profiles_list)
        
        # Profile actions
        actions_layout = QHBoxLayout()
        
        self.edit_btn = QPushButton("Edit Profile")
        self.edit_btn.clicked.connect(self.edit_profile)
        self.edit_btn.setEnabled(False)
        actions_layout.addWidget(self.edit_btn)
        
        self.toggle_btn = QPushButton("Toggle Active")
        self.toggle_btn.clicked.connect(self.toggle_profile_status)
        self.toggle_btn.setEnabled(False)
        actions_layout.addWidget(self.toggle_btn)
        
        self.delete_btn = QPushButton("Delete Profile")
        self.delete_btn.setStyleSheet("background-color: #ff3b30;")
        self.delete_btn.clicked.connect(self.delete_profile)
        self.delete_btn.setEnabled(False)
        actions_layout.addWidget(self.delete_btn)
        
        profiles_layout.addLayout(actions_layout)
        
        profiles_group.setLayout(profiles_layout)
        main_layout.addWidget(profiles_group)
        
        # Processing log
        log_group = QGroupBox("Processing Log")
        log_layout = QVBoxLayout()
        
        self.log_list = QListWidget()
        log_layout.addWidget(self.log_list)
        
        log_controls_layout = QHBoxLayout()
        
        self.clear_log_btn = QPushButton("Clear Log")
        self.clear_log_btn.clicked.connect(self.clear_log)
        log_controls_layout.addWidget(self.clear_log_btn)
        
        self.help_btn = QPushButton("Help")
        self.help_btn.clicked.connect(self.show_help)
        log_controls_layout.addWidget(self.help_btn)
        
        log_layout.addLayout(log_controls_layout)
        
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
    
    def setup_menu(self):
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("File")
        
        new_profile_action = file_menu.addAction("New Profile")
        new_profile_action.triggered.connect(self.add_profile)
        
        # Start/Stop monitoring
        self.toggle_monitoring_action = file_menu.addAction("Start Monitoring")
        self.toggle_monitoring_action.triggered.connect(self.toggle_monitoring)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        
        # Profile menu
        profile_menu = menu_bar.addMenu("Profile")
        
        edit_profile_action = profile_menu.addAction("Edit Selected Profile")
        edit_profile_action.triggered.connect(self.edit_profile)
        edit_profile_action.setEnabled(False)
        self.edit_profile_action = edit_profile_action
        
        toggle_active_action = profile_menu.addAction("Toggle Active Status")
        toggle_active_action.triggered.connect(self.toggle_profile_status)
        toggle_active_action.setEnabled(False)
        self.toggle_active_action = toggle_active_action
        
        delete_profile_action = profile_menu.addAction("Delete Profile")
        delete_profile_action.triggered.connect(self.delete_profile)
        delete_profile_action.setEnabled(False)
        self.delete_profile_action = delete_profile_action
        
        # Help menu
        help_menu = menu_bar.addMenu("Help")
        
        how_to_use_action = help_menu.addAction("How to Use")
        how_to_use_action.triggered.connect(self.show_help)
        
        help_menu.addSeparator()
        
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about)
    
    def show_about(self):
        # Get app icon for about dialog
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "app-icon.png")
        icon_pixmap = None
        if os.path.exists(icon_path):
            icon_pixmap = QPixmap(icon_path).scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        # Create custom about dialog with icon
        about_dialog = QMessageBox(self)
        about_dialog.setWindowTitle("About Image Converter")
        about_dialog.setText("<h3>Image Converter</h3>")
        about_dialog.setInformativeText("A modern app to automate image conversion tasks.")
        about_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        if icon_pixmap:
            about_dialog.setIconPixmap(icon_pixmap)
        
        about_dialog.exec()
    
    def load_profiles(self):
        self.profiles_list.clear()
        profiles = self.db.get_profiles()
        
        for profile in profiles:
            item = QListWidgetItem()
            item_widget = ProfileListItem(profile)
            
            item.setData(Qt.ItemDataRole.UserRole, profile['id'])
            item.setSizeHint(item_widget.sizeHint())
            
            self.profiles_list.addItem(item)
            self.profiles_list.setItemWidget(item, item_widget)
    
    def on_profile_selected(self):
        # Enable buttons
        self.edit_btn.setEnabled(True)
        self.toggle_btn.setEnabled(True)
        self.delete_btn.setEnabled(True)
        
        # Enable menu actions
        self.edit_profile_action.setEnabled(True)
        self.toggle_active_action.setEnabled(True)
        self.delete_profile_action.setEnabled(True)
    
    def add_profile(self):
        dialog = ProfileEditorDialog(self.db, parent=self)
        if dialog.exec():
            self.load_profiles()
    
    def edit_profile(self):
        selected_items = self.profiles_list.selectedItems()
        if not selected_items:
            return
            
        profile_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
        
        dialog = ProfileEditorDialog(self.db, profile_id=profile_id, parent=self)
        if dialog.exec():
            self.load_profiles()
            
            # Stop monitoring if it was running
            if self.is_monitoring:
                self.toggle_monitoring()
    
    def toggle_profile_status(self):
        selected_items = self.profiles_list.selectedItems()
        if not selected_items:
            return
            
        profile_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
        profile = self.db.get_profile(profile_id)
        
        # Toggle status
        new_status = 0 if profile['is_active'] else 1
        self.db.update_profile_status(profile_id, new_status)
        
        # Reload profile list
        self.load_profiles()
        
        # Reload profiles in watcher
        self.watcher.reload_profiles()
    
    def delete_profile(self):
        selected_items = self.profiles_list.selectedItems()
        if not selected_items:
            return
            
        profile_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
        profile = self.db.get_profile(profile_id)
        
        reply = QMessageBox.question(
            self, 
            "Confirm Delete",
            f"Are you sure you want to delete the profile '{profile['name']}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_profile(profile_id)
            self.load_profiles()
            
            # Disable buttons
            self.edit_btn.setEnabled(False)
            self.toggle_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
            
            # Disable menu actions
            self.edit_profile_action.setEnabled(False)
            self.toggle_active_action.setEnabled(False)
            self.delete_profile_action.setEnabled(False)
            
            # Reload profiles in watcher
            self.watcher.reload_profiles()
    
    def toggle_monitoring(self):
        if self.is_monitoring:
            # Stop monitoring
            self.watcher.stop()
            self.watcher.wait()
            
            self.start_btn.setText("Start Monitoring")
            self.start_btn.setStyleSheet("")
            self.status_label.setText("Status: Idle")
            self.toggle_monitoring_action.setText("Start Monitoring")
            
            self.is_monitoring = False
        else:
            # Start monitoring
            self.watcher.reload_profiles()
            self.watcher.start()
            
            self.start_btn.setText("Stop Monitoring")
            self.start_btn.setStyleSheet("background-color: #ff3b30;")
            self.status_label.setText("Status: Monitoring folders")
            self.toggle_monitoring_action.setText("Stop Monitoring")
            
            self.is_monitoring = True
    
    def process_file(self, file_path, profile_id):
        try:
            profile = self.db.get_profile(profile_id)
            if not profile:
                return
                
            # Log the file detection
            self.log_message(f"Processing {file_path} with profile {profile['name']}")
            
            # Process the image
            processor = ImageProcessor(profile)
            img = processor.process_image(file_path)
            
            if img:
                # Make sure directory exists
                os.makedirs(profile['destination_folder'], exist_ok=True)
                
                # Get count of existing files for this profile
                try:
                    count = len(os.listdir(profile['destination_folder']))
                except:
                    count = 0
                
                # Save the processed image
                dest_path = processor.save_image(img, file_path, sequence_num=count+1)
                
                if dest_path:
                    # Log the processed file in database
                    self.db.log_processed_file(profile_id, file_path, dest_path)
                    
                    # Update UI log
                    self.log_message(f"Saved to {dest_path}")
                else:
                    self.log_message(f"Failed to save processed image", error=True)
            else:
                self.log_message(f"Failed to process {file_path}", error=True)
                
        except Exception as e:
            self.log_message(f"Error processing {file_path}: {e}", error=True)
    
    def log_message(self, message, error=False):
        # Create item with timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        item = QListWidgetItem(f"[{timestamp}] {message}")
        
        if error:
            item.setForeground(QColor('#ff3b30'))
        
        # Add to top of list
        self.log_list.insertItem(0, item)
    
    def clear_log(self):
        self.log_list.clear()
    
    def show_help(self):
        help_dialog = QMessageBox(self)
        help_dialog.setWindowTitle("How to Use Image Converter")
        help_dialog.setIcon(QMessageBox.Icon.Information)
        
        # Set icon to app icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "app-icon.png")
        if os.path.exists(icon_path):
            icon_pixmap = QPixmap(icon_path).scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            help_dialog.setIconPixmap(icon_pixmap)
        
        help_text = """
        <h3>How to Use Image Converter</h3>
        
        <p><b>Getting Started:</b></p>
        <ol>
            <li>Create a new profile by clicking "New Profile" or using the File menu</li>
            <li>Set source and destination folders</li>
            <li>Configure output format and filename pattern</li>
            <li>Adjust image settings (resize, crop, enhancements)</li>
            <li>Preview your changes with a sample image</li>
            <li>Save the profile</li>
        </ol>
        
        <p><b>Monitoring Folders:</b></p>
        <ol>
            <li>Activate profiles you want to use</li>
            <li>Click "Start Monitoring" to begin watching source folders</li>
            <li>New images in source folders will automatically be converted</li>
            <li>View the processing log for details</li>
        </ol>
        
        <p><b>Managing Profiles:</b></p>
        <ul>
            <li>Select a profile and click Edit to modify settings</li>
            <li>Toggle profiles on/off with the "Toggle Active" button</li>
            <li>Remove profiles with the Delete button</li>
        </ul>
        
        <p><b>Resize Options:</b></p>
        <ul>
            <li><b>Dimensions</b>: Specify exact width and height</li>
            <li><b>Percentage</b>: Scale by percentage (1-500%)</li>
            <li><b>No Resize</b>: Keep original dimensions</li>
            <li>Use "Maintain Aspect Ratio" to prevent distortion</li>
        </ul>
        """
        
        help_dialog.setText(help_text)
        help_dialog.exec()
    
    def closeEvent(self, event):
        # Stop monitoring thread
        if self.is_monitoring:
            self.watcher.stop()
            self.watcher.wait()
        
        # Close database connection
        self.db.close()
        
        event.accept()