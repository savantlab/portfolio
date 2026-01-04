#!/usr/bin/env python3
"""
Resize and crop project images to a standard 16:9 aspect ratio.
Usage: python resize_project_images.py
"""
import os
from PIL import Image

# Target aspect ratio (16:9)
TARGET_RATIO = 16 / 9
TARGET_WIDTH = 1600  # Standard width for web
TARGET_HEIGHT = int(TARGET_WIDTH / TARGET_RATIO)  # 900

IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'static', 'images')

def resize_and_crop(image_path, output_path=None):
    """
    Resize and crop image to target aspect ratio.
    Center crops if needed, then resizes to target dimensions.
    """
    if output_path is None:
        output_path = image_path
    
    with Image.open(image_path) as img:
        # Get current dimensions
        width, height = img.size
        current_ratio = width / height
        
        print(f"Processing: {os.path.basename(image_path)}")
        print(f"  Original: {width}x{height} (ratio: {current_ratio:.2f})")
        
        # Calculate crop box to achieve target ratio
        if current_ratio > TARGET_RATIO:
            # Image is too wide, crop width
            new_width = int(height * TARGET_RATIO)
            left = (width - new_width) // 2
            right = left + new_width
            crop_box = (left, 0, right, height)
        else:
            # Image is too tall, crop height
            new_height = int(width / TARGET_RATIO)
            top = (height - new_height) // 2
            bottom = top + new_height
            crop_box = (0, top, width, bottom)
        
        # Crop to target ratio
        img_cropped = img.crop(crop_box)
        
        # Resize to target dimensions
        img_resized = img_cropped.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
        
        # Save
        img_resized.save(output_path, 'PNG', optimize=True)
        print(f"  Saved: {TARGET_WIDTH}x{TARGET_HEIGHT} (ratio: {TARGET_RATIO:.2f})")

def main():
    """Process all project images in the static/images directory."""
    # Project image files (excluding parallel-2.png which is not a project)
    project_images = [
        'mental-rotation-research.png',
        'savantlab.png',
        'taxbudget.png',
        'portfolio.png'
    ]
    
    print(f"Target dimensions: {TARGET_WIDTH}x{TARGET_HEIGHT} (16:9 ratio)")
    print("=" * 60)
    
    for filename in project_images:
        filepath = os.path.join(IMAGES_DIR, filename)
        if os.path.exists(filepath):
            resize_and_crop(filepath)
            print()
        else:
            print(f"Warning: {filename} not found")
            print()
    
    print("=" * 60)
    print("Processing complete!")

if __name__ == '__main__':
    main()
