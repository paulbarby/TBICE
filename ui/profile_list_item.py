from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel

class ProfileListItem(QWidget):
    def __init__(self, profile, parent=None):
        super().__init__(parent)
        self.profile = profile
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Status indicator
        self.status_indicator = QLabel()
        self.status_indicator.setFixedSize(12, 12)
        self.update_status_indicator()
        layout.addWidget(self.status_indicator)
        
        # Profile info
        info_layout = QVBoxLayout()
        
        # Profile name
        self.name_label = QLabel(self.profile['name'])
        self.name_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        info_layout.addWidget(self.name_label)
        
        # Profile details
        details = (
            f"Source: {self.profile['source_folder']} → "
            f"Destination: {self.profile['destination_folder']} | "
            f"Format: {self.profile['output_format']}"
        )
        self.details_label = QLabel(details)
        self.details_label.setStyleSheet("color: #666;")
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