from PIL import Image
from rich.console import Console
from rich.table import Table
from sklearn.cluster import KMeans
import numpy as np
import sys
import os
import re

def get_image_path_from_fehbg():
    fehbg_path = os.path.expanduser("~/.fehbg")
    if not os.path.exists(fehbg_path):
        return None
    
    with open(fehbg_path, 'r') as file:
        content = file.read()

    # Regex to extract the image path from the .fehbg file
    match = re.search(r"--bg-\w+\s+'(.+)'", content)
    if match:
        return match.group(1)
    return None

def get_palette(image_path, num_colors=5):
    # Open the image
    image = Image.open(image_path)
    image = image.convert('RGB')
    
    # Resize image to speed up processing (optional)
    image = image.resize((100, 100))

    # Get colors
    pixels = np.array(image.getdata())
    
    # Apply K-means clustering to find distinct colors
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)
    
    # Get the cluster centers (which are the representative colors)
    colors = kmeans.cluster_centers_.astype(int)
    return [tuple(color) for color in colors]

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def display_palette(colors):
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Color", justify="center")
    table.add_column("Hex Code", justify="center")
    
    for color in colors:
        hex_color = rgb_to_hex(color)
        table.add_row(
            f"[{hex_color}]█" * 5,
            f"[bold]{hex_color}[/bold]"
        )

    console.print(table)

if __name__ == "__main__":
    # Try to use the wallpaper from .fehbg if no argument is provided
    if len(sys.argv) < 2:
        image_path = get_image_path_from_fehbg()
        if image_path is None:
            print("Usage: python color_palette.py <image_path>")
            sys.exit(1)
    else:
        image_path = sys.argv[1]
    
    num_colors = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    colors = get_palette(image_path, num_colors)
    display_palette(colors)

