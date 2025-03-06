from PIL import Image
import os

def test_ico_save():
    try:
        # Create a test image
        img = Image.new('RGB', (64, 64), color=(255, 0, 0))
        
        # Create directory if it doesn't exist
        os.makedirs('tmp/test_icons', exist_ok=True)
        
        # Output path
        output_path = 'tmp/test_icons/test_icon.ico'
        
        # Convert to RGBA
        img = img.convert('RGBA')
        
        # Save as ICO - try without sizes parameter first
        print("Trying without sizes parameter...")
        try:
            img.save(output_path, format='ICO')
            print(f"Success! File exists: {os.path.exists(output_path)}, Size: {os.path.getsize(output_path)} bytes")
        except Exception as e:
            print(f"Failed: {e}")
        
        # Try with sizes parameter
        print("\nTrying with sizes parameter...")
        try:
            img.save(output_path, format='ICO', sizes=[(img.width, img.height)])
            print(f"Success! File exists: {os.path.exists(output_path)}, Size: {os.path.getsize(output_path)} bytes")
        except Exception as e:
            print(f"Failed: {e}")
        
        # Try with alternative formats
        print("\nTrying different format strings...")
        alt_formats = ['ico', 'ICO', 'ICON', 'icon']
        for fmt in alt_formats:
            try:
                test_path = f'tmp/test_icons/test_{fmt}.ico'
                img.save(test_path, format=fmt)
                print(f"Format '{fmt}' works! File exists: {os.path.exists(test_path)}, Size: {os.path.getsize(test_path)} bytes")
            except Exception as e:
                print(f"Format '{fmt}' failed: {e}")
        
    except Exception as e:
        print(f"General error: {e}")

if __name__ == "__main__":
    test_ico_save()