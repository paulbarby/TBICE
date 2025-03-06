from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from database.db_manager import Database

class ProfileListItem(QWidget):
    def __init__(self, profile, db=None, parent=None):
        super().__init__(parent)
        self.profile = profile
        self.db = db if db else Database()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 4, 8, 4)
        
        # Status indicator
        self.status_indicator = QLabel()
        self.status_indicator.setFixedSize(12, 12)
        self.update_status_indicator()
        layout.addWidget(self.status_indicator)
        
        # Profile info
        info_layout = QVBoxLayout()
        
        # Profile name and processed files count
        name_layout = QHBoxLayout()
        
        self.name_label = QLabel(self.profile['name'])
        self.name_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        name_layout.addWidget(self.name_label)
        
        # Add processed files counter
        processed_count = self.db.get_processed_files_count(self.profile['id'])
        self.files_count_label = QLabel(f"({processed_count} files processed)")
        self.files_count_label.setStyleSheet("color: #007aff; font-size: 12px;")
        name_layout.addWidget(self.files_count_label)
        
        name_layout.addStretch(1)
        info_layout.addLayout(name_layout)
        
        # Profile details
        details = (
            f"Source: {self.profile['source_folder']} → "
            f"Destination: {self.profile['destination_folder']} | "
            f"Format: {self.profile['output_format']}"
        )
        self.details_label = QLabel(details)
        self.details_label.setStyleSheet("color: #666; font-size: 10px;")
        self.details_label.setWordWrap(True)
        info_layout.addWidget(self.details_label)
        
        layout.addLayout(info_layout, 1)
        
        self.setLayout(layout)
    
    def update_status_indicator(self):
        if self.profile['is_active']:
            self.status_indicator.setStyleSheet(
                "background-color: #34c759; border-radius: 6px;"
            )
        else:
            self.status_indicator.setStyleSheet(
                "background-color: #ff3b30; border-radius: 6px;"
            )
    
    def update_files_count(self):
        processed_count = self.db.get_processed_files_count(self.profile['id'])
        self.files_count_label.setText(f"({processed_count} files processed)")