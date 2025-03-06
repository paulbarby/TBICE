#!/usr/bin/env python3
"""
Build script for creating a Windows executable of the Image Converter application.
This script uses PyInstaller to bundle the application into a standalone .exe file.
"""

import os
import sys
import subprocess
import shutil
import platform
from datetime import datetime

# Application info
APP_NAME = "ImageConverter"
APP_VERSION = "1.0.0"
MAIN_SCRIPT = "main.py"  # Update this to your main script name

def log(message):
    """Print a timestamped log message."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def install_pyinstaller():
    """Install PyInstaller if not already installed."""
    try:
        import PyInstaller
        log("PyInstaller is already installed.")
    except ImportError:
        log("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        log("PyInstaller installed successfully.")

def clean_build_dir():
    """Clean up old build files."""
    log("Cleaning build directories...")
    
    # Directories to remove
    for dir_name in ["build", "dist", f"{APP_NAME}.egg-info"]:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            log(f"Removed {dir_name}/")
    
    # Spec file to remove
    spec_file = f"{APP_NAME}.spec"
    if os.path.exists(spec_file):
        os.remove(spec_file)
        log(f"Removed {spec_file}")

def create_executable():
    """Create the executable using PyInstaller."""
    log("Building executable...")
    
    # Define icon path
    icon_path = os.path.join("assets", "app-icon.ico")
    if not os.path.exists(icon_path):
        log("Warning: Icon file not found. Using default icon.")
        icon_path = None
    
    # Check if the main script exists
    if not os.path.exists(MAIN_SCRIPT):
        log(f"Error: Main script {MAIN_SCRIPT} not found!")
        available_py_files = [f for f in os.listdir() if f.endswith('.py')]
        log(f"Available Python files: {available_py_files}")
        return False
    
    # Build command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", APP_NAME,
        "--onefile",
        "--windowed",
        "--clean",
        "--noconfirm",
    ]
    
    # Add icon if available
    if icon_path:
        cmd.extend(["--icon", icon_path])
    
    # Add data files
    cmd.extend([
        "--add-data", f"assets{os.pathsep}assets",
    ])
    
    # Add the main script
    cmd.append(MAIN_SCRIPT)
    
    # Execute PyInstaller
    log("Running PyInstaller with the following command:")
    log(" ".join(cmd))
    
    try:
        subprocess.check_call(cmd)
        log("Executable built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        log(f"Error building executable: {e}")
        return False

def create_installer():
    """Create an installer using NSIS (Windows only)."""
    if platform.system() != "Windows":
        log("Installer creation is only supported on Windows.")
        return
    
    # This would be implemented if we had NSIS installed
    log("Note: Installer creation requires NSIS to be installed.")
    log("You can manually create an installer using the executable in the dist/ folder.")

def main():
    """Main build process."""
    start_time = datetime.now()
    log(f"Starting build process for {APP_NAME} v{APP_VERSION}")
    
    # Make sure we're in the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    log(f"Working directory: {os.getcwd()}")
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Clean old build files
    clean_build_dir()
    
    # Create executable
    success = create_executable()
    
    # Create installer (Windows only)
    if success and platform.system() == "Windows":
        create_installer()
    
    # Calculate elapsed time
    elapsed_time = datetime.now() - start_time
    minutes, seconds = divmod(elapsed_time.total_seconds(), 60)
    
    if success:
        log(f"Build completed successfully in {int(minutes)}m {int(seconds)}s!")
        log(f"Executable available at: dist/{APP_NAME}.exe")
    else:
        log("Build failed!")

if __name__ == "__main__":
    main()