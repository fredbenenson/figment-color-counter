# Figment Pixel Color Counter

A Python tool for calculating the exact percentage of specific colors in images. This tool was developed for the tabletop game [Figment](https://www.cmyk.games/products/figment), where players guess the percentage of different colors on cards featuring abstract designs.

## Background

Figment is a game about visual perception where players try to guess what percentage of a card is covered by four specific colors: pink, green, blue, and silver. To create the game, we needed a precise way to calculate these percentages for scoring.

This tool converts high-resolution PNG images to pixel data, and then maps each pixel to the closest color in our defined palette using Euclidean distance in RGB space. It then calculates the exact percentage of each target color.

## Features

- Process entire directories of PNG images
- Map millions of unique pixel colors to specific target colors
- Calculate precise color percentages to six decimal places
- Handle edge aliasing and color blending
- Output results in CSV format for analysis
- Progress bar for monitoring batch operations

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/figment-pixel-counter.git
cd figment-pixel-counter
```

2. Install dependencies:
```
pip install pillow numpy webcolors tqdm
```

## Usage

1. Place your PNG images in a directory (default is `./images/`)

2. Edit the configuration section of `batch_open_source.py` if needed:
```python
# Directory containing PNG files
directory_path = './images/'

# Output CSV file path
output_csv = 'color_analysis.csv'

# Define target colors as {name: RGB tuple}
target_colors = {
    'hotpink': webcolors.hex_to_rgb('#ff69b4'),  
    'darkcyan': webcolors.hex_to_rgb('#008b8b'),
    'lightgray': webcolors.hex_to_rgb('#d3d3d3'),
    'blue': webcolors.hex_to_rgb('#005DBA'),
    'white': webcolors.hex_to_rgb('#ffffff')
}
```

3. Run the script:
```
python batch_open_source.py
```

4. Review the results in the generated CSV file

## How It Works

The algorithm works through these steps:

1. Load each PNG image and convert to an RGB array
2. Find all unique colors and their pixel counts
3. Map each unique color to its closest target color using Euclidean distance
4. Calculate percentages based on total pixel count
5. Output results to CSV with both percentages and raw pixel counts

## Example Output

The CSV output includes:
- Filename
- Percentage columns for each target color
- Raw pixel count columns for each target color

```
Filename,hotpink_percent,darkcyan_percent,lightgray_percent,blue_percent,white_percent,hotpink,darkcyan,lightgray,blue,white
card001.png,0.331542,0.253896,0.119871,0.294691,0.000000,78412,60034,28337,69687,0
card002.png,0.247105,0.247105,0.228895,0.276895,0.000000,58421,58421,54123,65445,0
...
```

## Customization

You can adjust this tool for your own needs:

- **Different Colors**: Update the `target_colors` dictionary with your own RGB values
- **Different File Types**: Modify the file filtering in `process_directory()` to accept other image formats
- **Precision**: Change the format string in `analyze_image_colors()` to adjust decimal precision

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Created by Fred Benenson for the tabletop game Figment
- Game design by Alex Hague and Fred Benenson
- Special thanks to the Figment playtesting community

## About Figment

Figment is a tabletop party game where you guess the percentage of colors on abstract design cards. The closer your guess, the more points you score!

[Learn more about Figment](https://www.kickstarter.com/projects/elanlee/figment)# figment-color-counter
