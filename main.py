#!/usr/bin/env python3
"""
Figment Pixel Color Counter

This script processes a directory of PNG images and calculates the percentage of 
specified target colors in each image. It was originally developed for the tabletop 
game Figment to determine the exact percentage of each color on game cards.

Dependencies:
- Python 3.6+
- Pillow (PIL)
- NumPy
- webcolors
- tqdm

Usage:
1. Set the directory_path to the folder containing your PNG images
2. Set output_csv to your desired output file path
3. Define target_colors with the specific colors you want to track
4. Run the script

The script will:
- Process each PNG file in the specified directory
- Calculate the percentage and pixel count of each target color
- Output the results to a CSV file
"""

import os
import csv
import numpy as np
from PIL import Image
import webcolors
from tqdm import tqdm

def get_color_name(rgb_triplet, target_colors):
    """
    Find the closest color from target_colors to the given RGB triplet.
    
    Args:
        rgb_triplet: A tuple of (R, G, B) values
        target_colors: A dictionary of color_name: rgb_tuple pairs
        
    Returns:
        The name of the closest color
    """
    min_distance = float('inf')
    closest_color = None
    for color_name, target_rgb in target_colors.items():
        # Calculate Euclidean distance in RGB space
        dist = sum([(a - b) ** 2 for a, b in zip(rgb_triplet, target_rgb)])
        if dist < min_distance:
            min_distance = dist
            closest_color = color_name
    return closest_color

def analyze_image_colors(image_path, target_colors):
    """
    Analyze the color distribution in an image, mapping each pixel to the closest target color.
    
    Args:
        image_path: Path to the image file
        target_colors: A dictionary of color_name: rgb_tuple pairs
        
    Returns:
        A tuple of (color_counts, color_percentages) where:
        - color_counts is a dictionary of color_name: pixel_count
        - color_percentages is a dictionary of color_name_percent: percentage_string
    """
    # Open and convert image to RGB format
    img = Image.open(image_path)
    img = img.convert('RGB')
    data = np.array(img)

    # Find all unique colors and their counts
    unique, counts = np.unique(data.reshape(-1, data.shape[-1]), axis=0, return_counts=True)
    unique = [tuple(color) for color in unique]

    # Initialize counters for our target colors
    color_counts = {color: 0 for color in target_colors}
    total_pixels = 0

    # Map each pixel to its closest target color
    for color, count in zip(unique, counts):
        color_name = get_color_name(color, target_colors)
        if color_name in target_colors:
            color_counts[color_name] += count
        total_pixels += count

    # Calculate percentages with six decimal precision
    color_percentages = {color + '_percent': "{:.6f}".format((count / total_pixels)) 
                         for color, count in color_counts.items()}
    return color_counts, color_percentages

def process_directory(directory_path, target_colors, output_csv):
    """
    Process all PNG files in a directory and output color analysis to a CSV file.
    
    Args:
        directory_path: Path to directory containing PNG files
        target_colors: A dictionary of color_name: rgb_tuple pairs
        output_csv: Path to output CSV file
    """
    # Get list of PNG files
    file_list = [f for f in os.listdir(directory_path) if f.lower().endswith('.png')]
    
    # Create CSV file
    with open(output_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        # Create headers for both percentages and raw counts
        headers = ['Filename'] + [color + '_percent' for color in target_colors] + list(target_colors.keys())
        writer.writerow(headers)

        # Process each image with progress bar
        for filename in tqdm(file_list, desc="Processing Images", unit="image"):
            image_path = os.path.join(directory_path, filename)
            color_counts, color_percentages = analyze_image_colors(image_path, target_colors)
            # Create row with filename, percentages, and raw counts
            row = [filename] + [color_percentages.get(color + '_percent', "0.00") for color in target_colors] + [color_counts.get(color, 0) for color in target_colors]
            writer.writerow(row)

# Configuration
# You can modify these values to match your specific needs

# Directory containing PNG files
directory_path = './images/'

# Output CSV file path
output_csv = 'color_analysis.csv'

# Define target colors as {name: RGB tuple}
# These are the colors used in Figment, but you can define your own
target_colors = {
    'hotpink': webcolors.hex_to_rgb('#ff69b4'),   # Pink elements
    'darkcyan': webcolors.hex_to_rgb('#008b8b'),  # Green elements
    'lightgray': webcolors.hex_to_rgb('#d3d3d3'), # Silver elements
    'blue': webcolors.hex_to_rgb('#005DBA'),      # Blue elements
    'white': webcolors.hex_to_rgb('#ffffff')      # Background
}

# Execute the script
if __name__ == "__main__":
    process_directory(directory_path, target_colors, output_csv)
    print(f"Analysis complete! Results saved to {output_csv}")