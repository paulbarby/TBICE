class StyleHelper:
    @staticmethod
    def get_application_style():
        # iOS-like style with light and elegant design
        return """
        QMainWindow, QDialog {
            background-color: #f5f5f7;
        }
        
        QMenuBar {
            background-color: white;
            color: #333333;
            border-bottom: 1px solid #d1d1d6;
            padding: 2px;
        }
        
        QMenuBar::item {
            background-color: transparent;
            padding: 4px 8px;
            border-radius: 4px;
            margin: 1px 2px;
        }
        
        QMenuBar::item:selected {
            background-color: #e5f1fb;
            color: #007aff;
        }
        
        QWidget {
            font-family: 'SF Pro Display', 'Segoe UI', Arial, sans-serif;
            font-size: 14px;
            color: #333333;
        }
        
        QLabel {
            color: #333333;
        }
        
        QPushButton {
            background-color: #007aff;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: 500;
        }
        
        QPushButton:hover {
            background-color: #0069d9;
        }
        
        QPushButton:pressed {
            background-color: #0058b7;
        }
        
        QPushButton:disabled {
            background-color: #b3d7ff;
            color: #f0f0f0;
        }
        
        QLineEdit, QComboBox, QSpinBox {
            border: 1px solid #d1d1d6;
            border-radius: 8px;
            padding: 8px;
            background-color: white;
        }
        
        QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
            border: 1px solid #007aff;
        }
        
        QComboBox::drop-down {
            border: none;
            width: 20px;
        }
        
        QComboBox QAbstractItemView {
            background-color: white;
            color: #333333;
            border: 1px solid #d1d1d6;
            selection-background-color: #e5f1fb;
            selection-color: #007aff;
        }
        
        QMenu {
            background-color: white;
            color: #333333;
            border: 1px solid #d1d1d6;
            padding: 5px;
        }
        
        QMenu::item {
            padding: 5px 25px 5px 30px;
            border-radius: 4px;
        }
        
        QMenu::item:selected {
            background-color: #e5f1fb;
            color: #007aff;
        }
        
        QMenu::separator {
            height: 1px;
            background-color: #d1d1d6;
            margin: 5px 15px;
        }
        
        QListWidget, QTabWidget {
            background-color: white;
            border: 1px solid #d1d1d6;
            border-radius: 8px;
        }
        
        QListWidget::item {
            padding: 8px;
            border-bottom: 1px solid #f0f0f0;
        }
        
        QListWidget::item:selected {
            background-color: #e5f1fb;
            color: #007aff;
        }
        
        QTabWidget::pane { 
            border: 1px solid #d1d1d6;
            border-radius: 8px;
            background-color: white;
        }
        
        QTabBar::tab {
            background-color: #f5f5f7;
            border: 1px solid #d1d1d6;
            border-bottom: none;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            padding: 8px 16px;
            margin-right: 2px;
        }
        
        QTabBar::tab:selected {
            background-color: white;
            border-bottom: 1px solid white;
        }
        
        QSlider::groove:horizontal {
            border: none;
            height: 4px;
            background-color: #d1d1d6;
            border-radius: 2px;
        }
        
        QSlider::handle:horizontal {
            background-color: #007aff;
            border: none;
            width: 18px;
            margin: -7px 0;
            border-radius: 9px;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 1px solid #d1d1d6;
            border-radius: 8px;
            margin-top: 16px;
            padding-top: 16px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 8px;
            color: #007aff;
        }
        
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
        }
        
        QCheckBox::indicator:checked {
            background-color: #007aff;
            border: none;
            border-radius: 4px;
        }
        """