#!/bin/bash
# Build script for macOS app bundle and DMG installer

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}===== TBICE - macOS Build Script =====${NC}"
echo -e "${GREEN}The Most Basic Image Converter Ever${NC}"
echo

# Check if running on macOS
if [[ $(uname) != "Darwin" ]]; then
    echo -e "${RED}Error: This script must be run on macOS.${NC}"
    echo "Please transfer this project to a Mac and run this script there."
    exit 1
fi

# Check for Python installation
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed.${NC}"
    echo "Please install Python 3 from https://www.python.org/downloads/"
    echo "or use 'brew install python3' if you have Homebrew installed."
    exit 1
fi

# Check for pip
if ! python3 -m pip --version &> /dev/null; then
    echo -e "${YELLOW}Warning: pip is not installed. Attempting to install...${NC}"
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py --user
    rm get-pip.py
fi

# Install requirements
echo -e "${GREEN}Installing required packages...${NC}"
python3 -m pip install --user -U pip
python3 -m pip install --user pyinstaller pillow pyqt6

# Check if we have a requirements.txt file and install dependencies
if [ -f "requirements.txt" ]; then
    echo -e "${GREEN}Installing project dependencies from requirements.txt...${NC}"
    python3 -m pip install --user -r requirements.txt
fi

# Run the Python build script
echo -e "${GREEN}Running build script...${NC}"
python3 build_macos.py

# Check if build was successful
if [ -d "dist/TBICE.app" ]; then
    echo
    echo -e "${GREEN}=====================================================${NC}"
    echo -e "${GREEN}Build successful!${NC}"
    echo
    echo -e "The application has been built to: ${YELLOW}dist/TBICE.app${NC}"
    
    # Check if DMG was created
    if [ -f "dist/TBICE-1.0.0.dmg" ]; then
        echo -e "DMG installer created at: ${YELLOW}dist/TBICE-1.0.0.dmg${NC}"
    else
        echo -e "${YELLOW}Note: DMG installer was not created.${NC}"
        echo "You can manually create a DMG using Disk Utility."
    fi
    
    echo
    echo -e "${GREEN}To run the application:${NC}"
    echo "1. Navigate to the dist folder"
    echo "2. Double-click TBICE.app"
    echo -e "${GREEN}=====================================================${NC}"
else
    echo
    echo -e "${RED}Build failed. Please check the output above for errors.${NC}"
fi