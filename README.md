# Image Converter

A modern desktop application for automatic image conversion with a clean, iOS-inspired interface.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20|%20macOS%20|%20Linux-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- Monitor folders for new images and automatically convert them
- Profiles for different conversion settings
- Image enhancements (resize, crop, brightness, contrast, sharpness, saturation)
- Preview changes before saving
- Multiple output formats (JPG, PNG, WEBP, GIF, ICO)
- Custom filename patterns with sequence numbers
- Active/inactive profiles
- Processing history with file tracking
- Modern, responsive user interface with iOS-inspired design

## Requirements

- Python 3.8+
- PyQt6
- Pillow (PIL Fork)

## Installation

### Method 1: Run from Source

1. Clone the repository
   ```
   git clone https://github.com/your-username/image-converter.git
   cd image-converter
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python main.py
   ```

### Method 2: Standalone Executables

#### Windows
1. Download the latest release from the [Releases](https://github.com/your-username/image-converter/releases) page
2. Run the installer or extract the ZIP file
3. Launch ImageConverter.exe

#### macOS
1. Download the DMG file from the [Releases](https://github.com/your-username/image-converter/releases) page
2. Open the DMG file and drag the application to your Applications folder
3. Launch Image Converter from your Applications folder

## Building from Source

- **Windows**: See [BUILD_WINDOWS.md](BUILD_WINDOWS.md) for detailed instructions
- **macOS**: See [BUILD_MACOS.md](BUILD_MACOS.md) for detailed instructions

## Usage

### Creating a Profile

1. Click "New Profile"
2. Enter profile details (name, source folder, destination folder)
3. Select output format and filename pattern
4. Adjust image settings (resize, crop, enhancements)
5. Preview changes with a sample image
6. Save the profile

### Monitoring Folders

- Click "Start Monitoring" to begin watching active profiles
- The application will automatically process new images in source folders
- View the processing log for details on converted files

## Project Structure

- `main.py` - Application entry point
- `/assets/` - Application resources (icons, images)
- `/database/` - Database management for profiles and settings
- `/ui/` - User interface components
  - `main_window.py` - The main application window
  - `profile_editor_dialog.py` - Dialog for creating/editing profiles
  - `profile_list_item.py` - Custom widget for profile display
- `/utils/` - Utility functions and classes
  - `image_processor.py` - Image processing functionality
  - `folder_watcher.py` - File system monitoring
  - `style_helper.py` - UI styling and theming
- `/web/` - Web page for the application's online presence

## Technical Details

- **Database**: SQLite database for storing profiles, settings, and processed file history
- **Image Processing**: Uses the Pillow library for image manipulation
- **UI Framework**: Built with PyQt6 for a modern look and feel
- **Threading**: Background thread for folder monitoring to maintain responsive UI
- **File Formats**: Support for JPG, PNG, WEBP, GIF, and ICO formats
- **Resize Methods**: Options for resizing by dimensions or percentage

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.