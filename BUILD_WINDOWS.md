# Building TBICE for Windows

This guide will walk you through the process of creating an executable (.exe) file for The Most Basic Image Converter Ever (TBICE) for Windows.

## Prerequisites

1. **Python 3.8 or newer** installed on your Windows system
2. **Git** (optional, but recommended for version control)
3. **Administrator privileges** may be required for installation

## Step 1: Set Up Your Environment

1. Clone or download the repository:
   ```
   git clone https://github.com/your-username/tbice.git
   cd tbice
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   pip install pyinstaller
   ```

## Step 2: Build the Executable

### Option 1: Using the Build Script

The repository includes a build script that automates the process:

1. Run the build script:
   ```
   python build_exe.py
   ```

2. Wait for the build process to complete. This might take a few minutes.

3. Find the executable in the `dist` folder.

### Option 2: Manual Build

If you prefer to build manually:

1. Run PyInstaller with the appropriate options:
   ```
   pyinstaller --name=TBICE --onefile --windowed --clean --noconfirm --icon=assets/app-icon.ico --add-data="assets;assets" main.py
   ```

2. The executable will be created in the `dist` folder.

## Step 3: Run the Application

1. Navigate to the `dist` folder
2. Double-click `TBICE.exe` to launch the application

## Troubleshooting

### Missing DLL Errors

If you get errors about missing DLLs:

1. Make sure all required packages are installed:
   ```
   pip install -r requirements.txt
   ```

2. Try including the missing DLLs explicitly:
   ```
   pyinstaller --add-binary="path/to/missing.dll;." ...
   ```

### Antivirus Warnings

Some antivirus software may flag PyInstaller-created executables as suspicious. This is a false positive.

1. Add an exception in your antivirus software
2. Consider signing the executable with a certificate for distribution

### Application Crashes on Startup

If the application crashes immediately:

1. Run it from the command line to see error messages:
   ```
   cd dist
   TBICE.exe
   ```

2. Check that all required files and dependencies are included in the build

## Creating an Installer (Optional)

To create a proper installer:

1. Install [NSIS (Nullsoft Scriptable Install System)](https://nsis.sourceforge.io/Download)

2. Create an NSIS script (a basic template is included in the `installer` folder)

3. Compile the installer:
   ```
   makensis installer/installer_script.nsi
   ```

## Distributing Your Application

Before distributing your application:

1. Test thoroughly on different Windows versions (10, 11)
2. Consider code signing for better security and user trust
3. Include a license and documentation

## Need Help?

If you encounter issues not covered here, please open an issue on the GitHub repository.