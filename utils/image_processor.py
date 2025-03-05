import os
from datetime import datetime
from typing import Dict, Any, Optional
from PIL import Image, ImageEnhance

class ImageProcessor:
    def __init__(self, profile: Dict[str, Any]):
        self.profile = profile
        
    def process_image(self, source_path_or_img) -> Optional[Image.Image]:
        try:
            # Check if the input is already a PIL Image object or a file path
            if isinstance(source_path_or_img, Image.Image):
                img = source_path_or_img.copy()  # Make a copy to avoid modifying original
                source_path = "memory image"
            else:
                img = Image.open(source_path_or_img)
                source_path = source_path_or_img
            
            # Convert image mode if needed
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGB')
            
            # Handle different resize methods
            resize_width = self.profile.get('resize_width', 0)
            resize_height = self.profile.get('resize_height', 0)
            
            # Resize based on method
            if resize_width == -1:
                # Percentage resize (percentage value stored in height field)
                percentage = resize_height / 100.0
                if percentage != 1.0:  # Only resize if not 100%
                    new_width = int(img.width * percentage)
                    new_height = int(img.height * percentage)
                    img = img.resize((new_width, new_height), Image.LANCZOS)
            elif resize_width > 0 and resize_height > 0:
                # Dimensions resize
                img = img.resize((resize_width, resize_height), Image.LANCZOS)
            
            # Crop
            if all(v > 0 for v in [
                    self.profile['crop_left'], self.profile['crop_top'],
                    self.profile['crop_right'], self.profile['crop_bottom']
                ]):
                img = img.crop((
                    self.profile['crop_left'],
                    self.profile['crop_top'],
                    self.profile['crop_right'],
                    self.profile['crop_bottom']
                ))
            
            # Adjust brightness
            if self.profile['brightness'] != 1.0:
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(self.profile['brightness'])
            
            # Adjust contrast
            if self.profile['contrast'] != 1.0:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(self.profile['contrast'])
            
            # Adjust sharpness
            if self.profile['sharpness'] != 1.0:
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(self.profile['sharpness'])
            
            # Adjust saturation
            if self.profile['saturation'] != 1.0:
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(self.profile['saturation'])
            
            return img
            
        except Exception as e:
            print(f"Error processing image {source_path}: {e}")
            return None
    
    def save_image(self, img: Image.Image, source_path: str, sequence_num: int = 0) -> Optional[str]:
        try:
            # Create destination directory if it doesn't exist
            os.makedirs(self.profile['destination_folder'], exist_ok=True)
            
            # Generate filename based on pattern
            source_filename = os.path.basename(source_path)
            name, _ = os.path.splitext(source_filename)
            
            pattern = self.profile['filename_pattern']
            if not pattern:
                pattern = "{name}"
            
            filename = pattern.format(
                name=name,
                seq=sequence_num,
                date=datetime.now().strftime('%Y%m%d'),
                time=datetime.now().strftime('%H%M%S')
            )
            
            # Add extension based on output format
            output_format = self.profile['output_format'].upper()
            if output_format == 'JPEG':
                output_format = 'JPG'
            
            dest_path = os.path.join(
                self.profile['destination_folder'],
                f"{filename}.{output_format.lower()}"
            )
            
            # Save with appropriate quality settings
            quality = self.profile.get('quality', 85)
            
            if output_format in ('JPG', 'JPEG'):
                img.save(dest_path, format='JPEG', quality=quality)
            elif output_format == 'PNG':
                img.save(dest_path, format='PNG', compress_level=int(10 - quality/10))
            elif output_format == 'WEBP':
                img.save(dest_path, format='WEBP', quality=quality)
            elif output_format == 'ICO':
                # For ICO format, we need to ensure it's in RGBA mode
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                # Ensure image size is appropriate for ICO format
                # ICO works best with standard sizes: 16x16, 32x32, 48x48, 64x64, 128x128
                # Resize to closest standard size if needed
                width, height = img.size
                ico_sizes = [16, 32, 48, 64, 128, 256]
                
                # Find closest standard size
                closest_size = min(ico_sizes, key=lambda x: abs(x - max(width, height)))
                
                # Resize if needed to maintain aspect ratio
                if width != closest_size or height != closest_size:
                    # Calculate new dimensions while preserving aspect ratio
                    if width > height:
                        new_width = closest_size
                        new_height = int(height * closest_size / width)
                    else:
                        new_height = closest_size
                        new_width = int(width * closest_size / height)
                    
                    img = img.resize((new_width, new_height), Image.LANCZOS)
                
                # Try different approaches to save as ICO
                try:
                    # Approach 1: Simple save
                    img.save(dest_path, format='ICO')
                except Exception:
                    try:
                        # Approach 2: With sizes parameter
                        img.save(dest_path, format='ICO', sizes=[(img.width, img.height)])
                    except Exception:
                        # Approach 3: Save as PNG then manually rename
                        png_path = dest_path.replace('.ico', '.png')
                        img.save(png_path, format='PNG')
                        if os.path.exists(png_path):
                            os.rename(png_path, dest_path)
            else:
                img.save(dest_path)
            
            return dest_path
            
        except Exception as e:
            print(f"Error saving image: {e}")
            return None