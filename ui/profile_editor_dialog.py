import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap, QIcon
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QLineEdit, 
    QPushButton, QComboBox, QSlider, QCheckBox, QSpinBox, QFileDialog, 
    QMessageBox
)
from PIL import Image
from database.db_manager import Database
from utils.image_processor import ImageProcessor

class ProfileEditorDialog(QDialog):
    def __init__(self, db: Database, profile_id=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.profile_id = profile_id
        self.profile = None
        self.preview_source_image = None
        self.preview_processed_image = None
        self.original_aspect_ratio = 1.0  # For maintaining aspect ratio
        
        if profile_id:
            self.profile = self.db.get_profile(profile_id)
        
        self.setWindowTitle("Profile Editor")
        self.resize(900, 700)
        
        # Set dialog icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "app-icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            
        self.setup_ui()
        
        if self.profile:
            self.load_profile_data()
    
    def setup_ui(self):
        main_layout = QVBoxLayout()
        
        # Profile name and paths
        form_layout = QHBoxLayout()
        
        # Left side: Basic settings
        left_group = QGroupBox("Profile Settings")
        left_layout = QVBoxLayout()
        
        # Profile name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Profile Name:"))
        self.name_input = QLineEdit()
        name_layout.addWidget(self.name_input)
        left_layout.addLayout(name_layout)
        
        # Source folder
        source_layout = QHBoxLayout()
        source_layout.addWidget(QLabel("Source Folder:"))
        self.source_input = QLineEdit()
        source_layout.addWidget(self.source_input)
        self.source_btn = QPushButton("Browse")
        self.source_btn.clicked.connect(self.browse_source)
        source_layout.addWidget(self.source_btn)
        left_layout.addLayout(source_layout)
        
        # Destination folder
        dest_layout = QHBoxLayout()
        dest_layout.addWidget(QLabel("Destination Folder:"))
        self.dest_input = QLineEdit()
        dest_layout.addWidget(self.dest_input)
        self.dest_btn = QPushButton("Browse")
        self.dest_btn.clicked.connect(self.browse_destination)
        dest_layout.addWidget(self.dest_btn)
        left_layout.addLayout(dest_layout)
        
        # Output format
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Output Format:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["JPG", "PNG", "WEBP", "GIF", "ICO"])
        format_layout.addWidget(self.format_combo)
        left_layout.addLayout(format_layout)
        
        # Filename pattern
        pattern_layout = QHBoxLayout()
        pattern_layout.addWidget(QLabel("Filename Pattern:"))
        self.pattern_input = QLineEdit()
        self.pattern_input.setPlaceholderText("{name}_{seq}")
        pattern_layout.addWidget(self.pattern_input)
        left_layout.addLayout(pattern_layout)
        
        # Pattern help text
        help_label = QLabel(
            "Available patterns: {name}, {seq}, {date}, {time}"
        )
        help_label.setStyleSheet("color: gray; font-size: 12px;")
        left_layout.addWidget(help_label)
        
        # Quality setting
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(QLabel("Quality:"))
        self.quality_slider = QSlider(Qt.Orientation.Horizontal)
        self.quality_slider.setMinimum(10)
        self.quality_slider.setMaximum(100)
        self.quality_slider.setValue(85)
        self.quality_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.quality_slider.setTickInterval(10)
        quality_layout.addWidget(self.quality_slider)
        self.quality_label = QLabel("85%")
        self.quality_slider.valueChanged.connect(self.update_quality_label)
        quality_layout.addWidget(self.quality_label)
        left_layout.addLayout(quality_layout)
        
        # Active status
        active_layout = QHBoxLayout()
        self.active_checkbox = QCheckBox("Active (Monitor source folder)")
        active_layout.addWidget(self.active_checkbox)
        left_layout.addLayout(active_layout)
        
        # Sample image selection
        preview_layout = QHBoxLayout()
        preview_layout.addWidget(QLabel("Preview Image:"))
        self.preview_btn = QPushButton("Select Sample Image")
        self.preview_btn.clicked.connect(self.select_preview_image)
        preview_layout.addWidget(self.preview_btn)
        left_layout.addLayout(preview_layout)
        
        left_group.setLayout(left_layout)
        form_layout.addWidget(left_group)
        
        # Right side: Image adjustments
        right_group = QGroupBox("Image Adjustments")
        right_layout = QVBoxLayout()
        
        # Resize settings
        resize_group = QGroupBox("Resize Options")
        resize_group_layout = QVBoxLayout()
        
        # Resize method selection
        resize_method_layout = QHBoxLayout()
        resize_method_layout.addWidget(QLabel("Resize Method:"))
        self.resize_method = QComboBox()
        self.resize_method.addItems(["Dimensions", "Percentage", "No Resize"])
        self.resize_method.currentIndexChanged.connect(self.update_resize_ui)
        resize_method_layout.addWidget(self.resize_method)
        resize_group_layout.addLayout(resize_method_layout)
        
        # Stacked layouts for different resize methods
        # 1. Dimensions resize
        self.dimensions_layout = QHBoxLayout()
        self.dimensions_layout.addWidget(QLabel("Width:"))
        self.resize_width = QSpinBox()
        self.resize_width.setMinimum(0)
        self.resize_width.setMaximum(10000)
        self.resize_width.setSpecialValueText("Original")
        self.dimensions_layout.addWidget(self.resize_width)
        self.dimensions_layout.addWidget(QLabel("×"))
        self.resize_height = QSpinBox()
        self.resize_height.setMinimum(0)
        self.resize_height.setMaximum(10000)
        self.resize_height.setSpecialValueText("Original")
        self.dimensions_layout.addWidget(self.resize_height)
        
        # Keep aspect ratio checkbox for dimensions
        self.keep_aspect_ratio = QCheckBox("Maintain Aspect Ratio")
        self.keep_aspect_ratio.setChecked(True)
        self.keep_aspect_ratio.stateChanged.connect(self.on_aspect_ratio_changed)
        self.dimensions_layout.addWidget(self.keep_aspect_ratio)
        
        # 2. Percentage resize
        self.percentage_layout = QHBoxLayout()
        self.percentage_layout.addWidget(QLabel("Scale:"))
        self.resize_percentage = QSpinBox()
        self.resize_percentage.setMinimum(1)
        self.resize_percentage.setMaximum(500)
        self.resize_percentage.setValue(100)
        self.resize_percentage.setSuffix("%")
        self.percentage_layout.addWidget(self.resize_percentage)
        
        # Container for the active resize method
        self.resize_method_container = QVBoxLayout()
        self.resize_method_container.addLayout(self.dimensions_layout)
        
        resize_group_layout.addLayout(self.resize_method_container)
        resize_group.setLayout(resize_group_layout)
        right_layout.addWidget(resize_group)
        
        # Crop settings
        crop_group = QGroupBox("Crop")
        crop_layout = QVBoxLayout()
        
        crop_top_layout = QHBoxLayout()
        crop_top_layout.addWidget(QLabel("Top:"))
        self.crop_top = QSpinBox()
        self.crop_top.setMinimum(0)
        self.crop_top.setMaximum(10000)
        crop_top_layout.addWidget(self.crop_top)
        crop_layout.addLayout(crop_top_layout)
        
        crop_left_right_layout = QHBoxLayout()
        crop_left_right_layout.addWidget(QLabel("Left:"))
        self.crop_left = QSpinBox()
        self.crop_left.setMinimum(0)
        self.crop_left.setMaximum(10000)
        crop_left_right_layout.addWidget(self.crop_left)
        crop_left_right_layout.addWidget(QLabel("Right:"))
        self.crop_right = QSpinBox()
        self.crop_right.setMinimum(0)
        self.crop_right.setMaximum(10000)
        crop_left_right_layout.addWidget(self.crop_right)
        crop_layout.addLayout(crop_left_right_layout)
        
        crop_bottom_layout = QHBoxLayout()
        crop_bottom_layout.addWidget(QLabel("Bottom:"))
        self.crop_bottom = QSpinBox()
        self.crop_bottom.setMinimum(0)
        self.crop_bottom.setMaximum(10000)
        crop_bottom_layout.addWidget(self.crop_bottom)
        crop_layout.addLayout(crop_bottom_layout)
        
        crop_group.setLayout(crop_layout)
        right_layout.addWidget(crop_group)
        
        # Enhancer sliders
        # Brightness
        brightness_layout = QHBoxLayout()
        brightness_layout.addWidget(QLabel("Brightness:"))
        self.brightness_slider = QSlider(Qt.Orientation.Horizontal)
        self.brightness_slider.setMinimum(0)
        self.brightness_slider.setMaximum(200)
        self.brightness_slider.setValue(100)
        self.brightness_slider.valueChanged.connect(self.update_preview)
        brightness_layout.addWidget(self.brightness_slider)
        self.brightness_label = QLabel("1.0")
        self.brightness_slider.valueChanged.connect(
            lambda v: self.brightness_label.setText(f"{v/100:.1f}")
        )
        brightness_layout.addWidget(self.brightness_label)
        right_layout.addLayout(brightness_layout)
        
        # Contrast
        contrast_layout = QHBoxLayout()
        contrast_layout.addWidget(QLabel("Contrast:"))
        self.contrast_slider = QSlider(Qt.Orientation.Horizontal)
        self.contrast_slider.setMinimum(0)
        self.contrast_slider.setMaximum(200)
        self.contrast_slider.setValue(100)
        self.contrast_slider.valueChanged.connect(self.update_preview)
        contrast_layout.addWidget(self.contrast_slider)
        self.contrast_label = QLabel("1.0")
        self.contrast_slider.valueChanged.connect(
            lambda v: self.contrast_label.setText(f"{v/100:.1f}")
        )
        contrast_layout.addWidget(self.contrast_label)
        right_layout.addLayout(contrast_layout)
        
        # Sharpness
        sharpness_layout = QHBoxLayout()
        sharpness_layout.addWidget(QLabel("Sharpness:"))
        self.sharpness_slider = QSlider(Qt.Orientation.Horizontal)
        self.sharpness_slider.setMinimum(0)
        self.sharpness_slider.setMaximum(200)
        self.sharpness_slider.setValue(100)
        self.sharpness_slider.valueChanged.connect(self.update_preview)
        sharpness_layout.addWidget(self.sharpness_slider)
        self.sharpness_label = QLabel("1.0")
        self.sharpness_slider.valueChanged.connect(
            lambda v: self.sharpness_label.setText(f"{v/100:.1f}")
        )
        sharpness_layout.addWidget(self.sharpness_label)
        right_layout.addLayout(sharpness_layout)
        
        # Saturation
        saturation_layout = QHBoxLayout()
        saturation_layout.addWidget(QLabel("Saturation:"))
        self.saturation_slider = QSlider(Qt.Orientation.Horizontal)
        self.saturation_slider.setMinimum(0)
        self.saturation_slider.setMaximum(200)
        self.saturation_slider.setValue(100)
        self.saturation_slider.valueChanged.connect(self.update_preview)
        saturation_layout.addWidget(self.saturation_slider)
        self.saturation_label = QLabel("1.0")
        self.saturation_slider.valueChanged.connect(
            lambda v: self.saturation_label.setText(f"{v/100:.1f}")
        )
        saturation_layout.addWidget(self.saturation_label)
        right_layout.addLayout(saturation_layout)
        
        # Update preview button
        update_preview_btn = QPushButton("Update Preview")
        update_preview_btn.clicked.connect(self.update_preview)
        right_layout.addWidget(update_preview_btn)
        
        # Connect all adjustment controls to update preview
        self.resize_width.valueChanged.connect(self.update_preview)
        self.resize_height.valueChanged.connect(self.update_preview)
        self.resize_percentage.valueChanged.connect(self.update_preview)
        self.crop_left.valueChanged.connect(self.update_preview)
        self.crop_right.valueChanged.connect(self.update_preview)
        self.crop_top.valueChanged.connect(self.update_preview)
        self.crop_bottom.valueChanged.connect(self.update_preview)
        self.quality_slider.valueChanged.connect(self.update_preview)
        
        right_group.setLayout(right_layout)
        form_layout.addWidget(right_group)
        
        main_layout.addLayout(form_layout)
        
        # Preview area
        preview_group = QGroupBox("Preview")
        preview_container = QHBoxLayout()
        
        # Source image preview
        source_preview_layout = QVBoxLayout()
        source_preview_layout.addWidget(QLabel("Source Image:"))
        self.source_preview = QLabel()
        self.source_preview.setMinimumSize(350, 250)
        self.source_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.source_preview.setStyleSheet("background-color: #f0f0f0; border: 1px solid #d1d1d6;")
        source_preview_layout.addWidget(self.source_preview)
        preview_container.addLayout(source_preview_layout)
        
        # Processed image preview
        processed_preview_layout = QVBoxLayout()
        processed_preview_layout.addWidget(QLabel("Processed Image:"))
        self.processed_preview = QLabel()
        self.processed_preview.setMinimumSize(350, 250)
        self.processed_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.processed_preview.setStyleSheet("background-color: #f0f0f0; border: 1px solid #d1d1d6;")
        processed_preview_layout.addWidget(self.processed_preview)
        preview_container.addLayout(processed_preview_layout)
        
        preview_group.setLayout(preview_container)
        main_layout.addWidget(preview_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save Profile")
        self.save_btn.clicked.connect(self.save_profile)
        button_layout.addWidget(self.save_btn)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        self.cancel_btn.setStyleSheet("background-color: #ff3b30;")
        button_layout.addWidget(self.cancel_btn)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
    
    def browse_source(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Select Source Folder", ""
        )
        if folder:
            self.source_input.setText(folder)
    
    def browse_destination(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Select Destination Folder", ""
        )
        if folder:
            self.dest_input.setText(folder)
    
    def select_preview_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Preview Image", "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp *.tiff *.ico)"
        )
        if file_path:
            try:
                self.preview_source_image = Image.open(file_path)
                self.update_preview()
                
                # Display source image
                pixmap = self.get_pixmap_from_pil_image(self.preview_source_image)
                self.source_preview.setPixmap(pixmap)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to load image: {e}")
    
    def update_quality_label(self, value):
        self.quality_label.setText(f"{value}%")
    
    def update_preview(self):
        if not self.preview_source_image:
            return
        
        try:
            # Create a temporary profile with current settings
            temp_profile = self.get_current_profile_data()
            
            # Create a processor with this profile
            processor = ImageProcessor(temp_profile)
            
            # Process the image - pass the source image object directly
            self.preview_processed_image = processor.process_image(self.preview_source_image)
            
            if self.preview_processed_image:
                # Display processed image
                pixmap = self.get_pixmap_from_pil_image(self.preview_processed_image)
                self.processed_preview.setPixmap(pixmap)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to update preview: {e}")
    
    def get_pixmap_from_pil_image(self, pil_image):
        # Convert PIL image to QPixmap for display
        if not pil_image:
            return QPixmap()
            
        # Make a copy to avoid modifying the original
        img = pil_image.copy()
        
        # Ensure we're in the correct mode for display
        if img.mode == "RGBA":
            img_mode = img
        else:
            img_mode = img.convert("RGBA")
        
        # Resize to fit in preview area while maintaining aspect ratio
        img_mode.thumbnail((350, 250))
        
        # Get the correct data from the image
        width, height = img_mode.size
        bytes_per_line = 4 * width
        buffer = img_mode.tobytes("raw", "RGBA")
        
        # Create QImage with the correct format and byte order
        qim = QImage(buffer, width, height, bytes_per_line, QImage.Format.Format_RGBA8888)
            
        pixmap = QPixmap.fromImage(qim)
        return pixmap
    
    def update_resize_ui(self):
        # Clear current layout
        while self.resize_method_container.count():
            item = self.resize_method_container.takeAt(0)
            if item.layout():
                item.layout().setParent(None)
        
        resize_method = self.resize_method.currentText()
        
        if resize_method == "Dimensions":
            self.resize_method_container.addLayout(self.dimensions_layout)
        elif resize_method == "Percentage":
            self.resize_method_container.addLayout(self.percentage_layout)
        # No resize doesn't need a UI
        
        self.update_preview()
    
    def on_aspect_ratio_changed(self, state):
        if self.preview_source_image and state == Qt.CheckState.Checked.value:
            # Calculate and store aspect ratio from current image
            width, height = self.preview_source_image.size
            if height > 0:  # Avoid division by zero
                self.original_aspect_ratio = width / height
        
        # If we are maintaining aspect ratio and have width, update height
        if state == Qt.CheckState.Checked.value and self.resize_width.value() > 0:
            new_height = int(self.resize_width.value() / self.original_aspect_ratio)
            self.resize_height.blockSignals(True)
            self.resize_height.setValue(new_height)
            self.resize_height.blockSignals(False)
            
        self.update_preview()
    
    def select_preview_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Preview Image", "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp *.tiff *.ico)"
        )
        if file_path:
            try:
                self.preview_source_image = Image.open(file_path)
                
                # Store aspect ratio for maintain aspect ratio feature
                width, height = self.preview_source_image.size
                if height > 0:
                    self.original_aspect_ratio = width / height
                
                self.update_preview()
                
                # Display source image
                pixmap = self.get_pixmap_from_pil_image(self.preview_source_image)
                self.source_preview.setPixmap(pixmap)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to load image: {e}")
    
    def get_current_profile_data(self):
        resize_method = self.resize_method.currentText()
        
        # Set resize width and height based on method
        if resize_method == "Dimensions":
            resize_width = self.resize_width.value()
            resize_height = self.resize_height.value()
        elif resize_method == "Percentage":
            # For percentage resize, we'll calculate dimensions during processing
            # based on original image size and percentage
            resize_width = -1  # Special value to indicate percentage resize
            resize_height = self.resize_percentage.value()  # Store percentage in height field
        else:  # No resize
            resize_width = 0
            resize_height = 0
        
        profile_data = {
            'name': self.name_input.text(),
            'source_folder': self.source_input.text(),
            'destination_folder': self.dest_input.text(),
            'output_format': self.format_combo.currentText(),
            'filename_pattern': self.pattern_input.text(),
            'is_active': 1 if self.active_checkbox.isChecked() else 0,
            'resize_width': resize_width,
            'resize_height': resize_height,
            'resize_method': resize_method,  # Store the method for later use
            'keep_aspect_ratio': self.keep_aspect_ratio.isChecked(),
            'crop_left': self.crop_left.value(),
            'crop_top': self.crop_top.value(),
            'crop_right': self.crop_right.value(),
            'crop_bottom': self.crop_bottom.value(),
            'brightness': self.brightness_slider.value() / 100.0,
            'contrast': self.contrast_slider.value() / 100.0,
            'sharpness': self.sharpness_slider.value() / 100.0,
            'saturation': self.saturation_slider.value() / 100.0,
            'quality': self.quality_slider.value()
        }
        return profile_data
    
    def save_profile(self):
        if not self.name_input.text():
            QMessageBox.warning(self, "Error", "Profile name is required")
            return
            
        if not self.source_input.text() or not os.path.isdir(self.source_input.text()):
            QMessageBox.warning(self, "Error", "Valid source folder is required")
            return
            
        if not self.dest_input.text():
            QMessageBox.warning(self, "Error", "Destination folder is required")
            return
        
        try:
            # Get current profile data
            current_data = self.get_current_profile_data()
            
            # Separate data for database tables
            profile_data = {
                'name': current_data['name'],
                'source_folder': current_data['source_folder'],
                'destination_folder': current_data['destination_folder'],
                'output_format': current_data['output_format'],
                'filename_pattern': current_data['filename_pattern'],
                'is_active': current_data['is_active']
            }
            
            # Get image settings
            settings_data = {
                'resize_width': current_data['resize_width'],
                'resize_height': current_data['resize_height'],
                'resize_method': current_data['resize_method'],
                'keep_aspect_ratio': 1 if current_data['keep_aspect_ratio'] else 0,
                'crop_left': current_data['crop_left'],
                'crop_top': current_data['crop_top'],
                'crop_right': current_data['crop_right'],
                'crop_bottom': current_data['crop_bottom'],
                'brightness': current_data['brightness'],
                'contrast': current_data['contrast'],
                'sharpness': current_data['sharpness'],
                'saturation': current_data['saturation'],
                'quality': current_data['quality']
            }
            
            # Save to database
            self.db.save_profile(profile_data, settings_data)
            
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save profile: {e}")
    
    def load_profile_data(self):
        if not self.profile:
            return
            
        # Load basic settings
        self.name_input.setText(self.profile['name'])
        self.source_input.setText(self.profile['source_folder'])
        self.dest_input.setText(self.profile['destination_folder'])
        self.pattern_input.setText(self.profile['filename_pattern'])
        
        # Set format
        format_index = self.format_combo.findText(self.profile['output_format'])
        if format_index >= 0:
            self.format_combo.setCurrentIndex(format_index)
        
        # Set active status
        self.active_checkbox.setChecked(bool(self.profile['is_active']))
        
        # Set resize method from database if available
        if 'resize_method' in self.profile and self.profile['resize_method']:
            self.resize_method.setCurrentText(self.profile['resize_method'])
        else:
            # Determine resize method based on stored values
            resize_width = self.profile['resize_width']
            resize_height = self.profile['resize_height']
            
            if resize_width == 0 and resize_height == 0:
                # No resize
                self.resize_method.setCurrentText("No Resize")
            elif resize_width == -1:
                # Percentage resize (stored in height field)
                self.resize_method.setCurrentText("Percentage")
                self.resize_percentage.setValue(resize_height)
            else:
                # Dimensions resize
                self.resize_method.setCurrentText("Dimensions")
                self.resize_width.setValue(resize_width)
                self.resize_height.setValue(resize_height)
        
        # Set aspect ratio checkbox if available
        if 'keep_aspect_ratio' in self.profile:
            self.keep_aspect_ratio.setChecked(bool(self.profile['keep_aspect_ratio']))
        
        # Update the resize UI to show the correct controls
        self.update_resize_ui()
        
        # Set crop values
        self.crop_left.setValue(self.profile['crop_left'])
        self.crop_top.setValue(self.profile['crop_top'])
        self.crop_right.setValue(self.profile['crop_right'])
        self.crop_bottom.setValue(self.profile['crop_bottom'])
        
        # Set enhancement sliders
        self.brightness_slider.setValue(int(self.profile['brightness'] * 100))
        self.contrast_slider.setValue(int(self.profile['contrast'] * 100))
        self.sharpness_slider.setValue(int(self.profile['sharpness'] * 100))
        self.saturation_slider.setValue(int(self.profile['saturation'] * 100))
        self.quality_slider.setValue(self.profile['quality'])
        
        # Update labels
        self.brightness_label.setText(f"{self.profile['brightness']:.1f}")
        self.contrast_label.setText(f"{self.profile['contrast']:.1f}")
        self.sharpness_label.setText(f"{self.profile['sharpness']:.1f}")
        self.saturation_label.setText(f"{self.profile['saturation']:.1f}")
        self.quality_label.setText(f"{self.profile['quality']}%")