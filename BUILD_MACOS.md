# Building TBICE for macOS

This guide will walk you through the process of creating a macOS application bundle (.app) and optionally a disk image (.dmg) installer for The Most Basic Image Converter Ever (TBICE).

## Prerequisites

1. **macOS** system (10.15 Catalina or newer recommended)
2. **Python 3.8 or newer** installed
3. **Git** (optional, but recommended for version control)
4. **Homebrew** (optional, but recommended for installing additional tools)

## Option 1: Using the Automated Build Script (Recommended)

The easiest way to build the application is to use the provided shell script:

1. Open Terminal
2. Navigate to the project directory:
   ```bash
   cd /path/to/image-converter
   ```
3. Make the build script executable:
   ```bash
   chmod +x build_macos.sh
   ```
4. Run the build script:
   ```bash
   ./build_macos.sh
   ```
5. Wait for the build process to complete
6. Find the application bundle in the `dist` folder

## Option 2: Manual Build Process

If you prefer to have more control over the build process, follow these steps:

### Step 1: Set Up Your Environment

1. Clone or download the repository:
   ```bash
   git clone https://github.com/your-username/tbice.git
   cd tbice
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

### Step 2: Create an Icon File (Optional)

macOS applications use .icns format for their icons:

1. Convert your PNG icon to .icns format:
   ```bash
   # Create an iconset directory
   mkdir AppIcon.iconset
   
   # Generate icons at various sizes
   sips -z 16 16 assets/app-icon.png --out AppIcon.iconset/icon_16x16.png
   sips -z 32 32 assets/app-icon.png --out AppIcon.iconset/icon_16x16@2x.png
   sips -z 32 32 assets/app-icon.png --out AppIcon.iconset/icon_32x32.png
   sips -z 64 64 assets/app-icon.png --out AppIcon.iconset/icon_32x32@2x.png
   sips -z 128 128 assets/app-icon.png --out AppIcon.iconset/icon_128x128.png
   sips -z 256 256 assets/app-icon.png --out AppIcon.iconset/icon_128x128@2x.png
   sips -z 256 256 assets/app-icon.png --out AppIcon.iconset/icon_256x256.png
   sips -z 512 512 assets/app-icon.png --out AppIcon.iconset/icon_256x256@2x.png
   sips -z 512 512 assets/app-icon.png --out AppIcon.iconset/icon_512x512.png
   sips -z 1024 1024 assets/app-icon.png --out AppIcon.iconset/icon_512x512@2x.png
   
   # Convert the iconset to .icns
   iconutil -c icns AppIcon.iconset -o assets/AppIcon.icns
   
   # Clean up
   rm -rf AppIcon.iconset
   ```

### Step 3: Build the Application Bundle

1. Build the application using PyInstaller:
   ```bash
   pyinstaller --name=TBICE \
               --windowed \
               --onedir \
               --icon=assets/AppIcon.icns \
               --add-data="assets:assets" \
               --osx-bundle-identifier=com.example.tbice \
               main.py
   ```

2. The application bundle will be created at `dist/TBICE.app`

### Step 4: Create a DMG Installer (Optional)

You can create a distributable disk image (.dmg) file:

1. Install create-dmg tool:
   ```bash
   brew install create-dmg
   ```

2. Create the DMG:
   ```bash
   create-dmg \
     --volname "TBICE Installer" \
     --volicon "assets/AppIcon.icns" \
     --window-pos 200 100 \
     --window-size 800 400 \
     --icon-size 100 \
     --icon "TBICE.app" 200 200 \
     --hide-extension "TBICE.app" \
     --app-drop-link 600 200 \
     "dist/TBICE-1.0.0.dmg" \
     "dist/TBICE.app"
   ```

## Troubleshooting

### Missing Dependencies

If you encounter errors about missing libraries:

1. Make sure you have installed all requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. For PyQt issues, try installing directly with brew:
   ```bash
   brew install pyqt@6
   ```

### Code Signing Issues

For distribution outside of development:

1. Sign the application bundle with your Developer ID:
   ```bash
   codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name (TEAMID)" "dist/TBICE.app"
   ```

2. Verify the signature:
   ```bash
   codesign --verify --verbose "dist/TBICE.app"
   ```

### Notarization for Distribution

For distribution via the internet, you'll need to notarize your application with Apple:

1. Create a ZIP archive of your app:
   ```bash
   ditto -c -k --keepParent "dist/TBICE.app" "dist/TBICE.zip"
   ```

2. Submit for notarization:
   ```bash
   xcrun notarytool submit "dist/TBICE.zip" --apple-id "your@apple.id" --password "app-specific-password" --team-id "TEAMID" --wait
   ```

3. Staple the notarization ticket:
   ```bash
   xcrun stapler staple "dist/TBICE.app"
   ```

## Need Help?

If you encounter issues not covered here, please open an issue on the GitHub repository.