# Image Converter

A modern desktop application for automatic image conversion with a clean, iOS-inspired interface.

## Features

- Monitor folders for new images and automatically convert them
- Profiles for different conversion settings
- Image enhancements (resize, crop, brightness, contrast, etc.)
- Preview changes before saving
- Multiple output formats (JPG, PNG, WEBP, GIF)
- Custom filename patterns with sequence numbers
- Active/inactive profiles
- Processing log

## Requirements

- Python 3.8+
- PyQt6
- Pillow (PIL Fork)

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```
python main.py
```

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
- `/database/` - Database management
- `/ui/` - User interface components
- `/utils/` - Utility functions and classes
  - Image processing
  - Folder watching
  - UI styling

## License

MIT