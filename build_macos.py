#!/usr/bin/env python3
"""
Build script for creating a macOS application bundle of TBICE (The Most Basic Image Converter Ever).
This script uses PyInstaller to bundle the application into a .app file.
"""

import os
import sys
import subprocess
import shutil
import platform
from datetime import datetime

# Application info
APP_NAME = "TBICE"
APP_VERSION = "1.0.0"
MAIN_SCRIPT = "main.py"  # Update this to your main script name

def log(message):
    """Print a timestamped log message."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def check_macos():
    """Check if we're running on macOS."""
    if platform.system() != "Darwin":
        log("Error: This script should be run on macOS.")
        sys.exit(1)
    
    log(f"Running on macOS {platform.mac_ver()[0]}")

def install_dependencies():
    """Install required Python dependencies."""
    log("Installing dependencies...")
    
    # Install PyInstaller if not already installed
    try:
        import PyInstaller
        log("PyInstaller is already installed.")
    except ImportError:
        log("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "pyinstaller"])
        log("PyInstaller installed successfully.")
    
    # Install application dependencies from requirements.txt
    if os.path.exists("requirements.txt"):
        log("Installing application dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "-r", "requirements.txt"])
        log("Application dependencies installed successfully.")
    else:
        log("Warning: requirements.txt not found. Ensuring core dependencies are installed...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "PyQt6", "Pillow", "sqlite3"])

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

def create_icns():
    """Create an .icns file from the app icon."""
    log("Creating .icns file for macOS...")
    
    # Check if the icon exists
    icon_path = os.path.join("assets", "app-icon.png")
    if not os.path.exists(icon_path):
        log("Warning: Icon file not found. Using default icon.")
        return None
    
    # Create temporary iconset directory
    iconset_dir = "AppIcon.iconset"
    os.makedirs(iconset_dir, exist_ok=True)
    
    # Generate icon in various sizes
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    for size in sizes:
        subprocess.check_call([
            "sips", "-z", str(size), str(size), icon_path, 
            "--out", f"{iconset_dir}/icon_{size}x{size}.png"
        ])
        
        # Also create 2x versions
        if size < 512:
            subprocess.check_call([
                "sips", "-z", str(size*2), str(size*2), icon_path, 
                "--out", f"{iconset_dir}/icon_{size}x{size}@2x.png"
            ])
    
    # Convert the iconset to .icns
    icns_path = os.path.join("assets", "AppIcon.icns")
    subprocess.check_call(["iconutil", "-c", "icns", iconset_dir, "-o", icns_path])
    
    # Clean up
    shutil.rmtree(iconset_dir)
    
    log(f"Created .icns file at {icns_path}")
    return icns_path

def create_app_bundle():
    """Create the macOS .app bundle using PyInstaller."""
    log("Creating macOS app bundle...")
    
    # Check if the main script exists
    if not os.path.exists(MAIN_SCRIPT):
        log(f"Error: Main script {MAIN_SCRIPT} not found!")
        available_py_files = [f for f in os.listdir() if f.endswith('.py')]
        log(f"Available Python files: {available_py_files}")
        return False
    
    # Get icon path
    icon_path = os.path.join("assets", "AppIcon.icns")
    if not os.path.exists(icon_path):
        icon_path = create_icns()
    
    # Build command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", APP_NAME,
        "--windowed",
        "--clean",
        "--noconfirm",
        "--onedir",
    ]
    
    # Add icon if available
    if icon_path and os.path.exists(icon_path):
        cmd.extend(["--icon", icon_path])
    
    # Add data files
    cmd.extend([
        "--add-data", f"assets{os.pathsep}assets",
    ])
    
    # Add Info.plist settings
    cmd.extend([
        "--osx-bundle-identifier", "com.example.tbice",
    ])
    
    # Add the main script
    cmd.append(MAIN_SCRIPT)
    
    # Execute PyInstaller
    log("Running PyInstaller with the following command:")
    log(" ".join(cmd))
    
    try:
        subprocess.check_call(cmd)
        log("App bundle built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        log(f"Error building app bundle: {e}")
        return False

def create_dmg():
    """Create a .dmg installer from the .app bundle."""
    log("Creating DMG installer...")
    
    app_path = os.path.join("dist", f"{APP_NAME}.app")
    if not os.path.exists(app_path):
        log("Error: App bundle not found. Cannot create DMG.")
        return False
    
    # Check if create-dmg is installed
    try:
        subprocess.check_call(["which", "create-dmg"], stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        log("create-dmg not found. Installing using homebrew...")
        try:
            subprocess.check_call(["brew", "install", "create-dmg"])
        except subprocess.CalledProcessError:
            log("Error: Could not install create-dmg. Is homebrew installed?")
            log("You can manually create a DMG by dragging the .app to Disk Utility.")
            return False
    
    # Create the DMG
    dmg_path = os.path.join("dist", f"{APP_NAME}-{APP_VERSION}.dmg")
    try:
        subprocess.check_call([
            "create-dmg",
            "--volname", f"{APP_NAME} Installer",
            "--volicon", os.path.join("assets", "AppIcon.icns"),
            "--window-pos", "200", "100",
            "--window-size", "800", "400",
            "--icon-size", "100",
            "--icon", f"{APP_NAME}.app", "200", "200",
            "--hide-extension", f"{APP_NAME}.app",
            "--app-drop-link", "600", "200",
            dmg_path,
            app_path
        ])
        log(f"DMG installer created at {dmg_path}")
        return True
    except subprocess.CalledProcessError as e:
        log(f"Error creating DMG: {e}")
        log("You can manually create a DMG by dragging the .app to Disk Utility.")
        return False

def main():
    """Main build process."""
    start_time = datetime.now()
    log(f"Starting macOS build process for {APP_NAME} v{APP_VERSION}")
    
    # Check if we're on macOS
    check_macos()
    
    # Make sure we're in the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    log(f"Working directory: {os.getcwd()}")
    
    # Install dependencies
    install_dependencies()
    
    # Clean old build files
    clean_build_dir()
    
    # Create the app bundle
    success = create_app_bundle()
    
    # Create a DMG installer
    if success:
        create_dmg()
    
    # Calculate elapsed time
    elapsed_time = datetime.now() - start_time
    minutes, seconds = divmod(elapsed_time.total_seconds(), 60)
    
    if success:
        log(f"Build completed successfully in {int(minutes)}m {int(seconds)}s!")
        log(f"App bundle available at: dist/{APP_NAME}.app")
    else:
        log("Build failed!")

if __name__ == "__main__":
    main()