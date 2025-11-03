import json
import os

# --- Configuration Loading ---
try:
    # Get the absolute path to the directory containing this file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Join it with the config file name
    config_path = os.path.join(base_dir, 'config.json')

    with open(config_path, 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    print("Error: config.json not found. Make sure it's in the same directory as consts.py.")
    data = {}
except json.JSONDecodeError:
    print("Error: config.json is not valid JSON.")
    data = {}

# --- Game Settings ---
back_color = data.get('back_color', [255, 255, 255])
fruit_color = data.get('fruit_color', [255, 0, 0])
block_color = data.get('block_color', [139, 69, 19])
cell_size = data.get('cell_size', 30)
block_cells = data.get('block_cells', [])
table_size = data.get('table_size', 20)
height = data.get('height', 800)
width = data.get('width', 800)
snakes = data.get('snakes', [])
sx = data.get('sx', 30)
sy = data.get('sy', 50)

