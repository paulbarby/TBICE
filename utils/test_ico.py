from PIL import Image
import os

# Test ICO saving functionality
def test_ico_save():
    # Create a test image
    img = Image.new('RGB', (64, 64), color=(255, 0, 0))
    
    # Try saving as ICO
    try:
        # Use path relative to project root
        output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                 'tmp', 'test_icons', 'test_icon.ico')
        
        # Convert to RGBA (as our code does)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
            
        # Save as ICO with explicit sizes parameter
        img.save(output_path, format='ICO', sizes=[(img.width, img.height)])
        
        print(f"Saved ICO file to {output_path}")
        print(f"File exists: {os.path.exists(output_path)}")
        print(f"File size: {os.path.getsize(output_path)} bytes")
        
        # Try to load it back to verify
        loaded = Image.open(output_path)
        print(f"Loaded ICO: Size={loaded.size}, Mode={loaded.mode}")
        
    except Exception as e:
        print(f"Error saving ICO: {e}")
        
if __name__ == "__main__":
    test_ico_save()