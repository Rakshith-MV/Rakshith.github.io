from flask import Flask, render_template, send_file, jsonify
from PIL import Image
import os
import io
import random

app = Flask(__name__)

# Add global state to track flipped tiles
flipped_tiles = set()

# Ensure the tiles directory exists
if not os.path.exists('static/tiles'):
    os.makedirs('static/tiles')

def split_image(image_path):
    """Split the image into 9 equal parts"""
    with Image.open(image_path) as img:
        # Get the width and height of the image
        width, height = img.size
        
        # Calculate the width and height of each tile
        tile_width = width // 3
        tile_height = height // 3
        
        # Split the image into 9 parts and save them
        for i in range(3):
            for j in range(3):
                left = j * tile_width
                top = i * tile_height
                right = left + tile_width
                bottom = top + tile_height
                
                # Crop the image and save the tile
                tile = img.crop((left, top, right, bottom))
                tile.save(f'static/tiles/tile_{i}_{j}.png')

@app.route('/')
def index():
    # Reset flipped tiles when the game starts
    global flipped_tiles
    flipped_tiles.clear()
    split_image('static/image.jpg')
    return render_template('index.html')

@app.route('/flip_random')
def flip_random():
    global flipped_tiles
    # Get all possible tile coordinates
    all_tiles = [(i, j) for i in range(3) for j in range(3)]
    # Remove already flipped tiles
    unflipped = [tile for tile in all_tiles if tile not in flipped_tiles]
    
    if not unflipped:
        return jsonify({'success': False, 'message': 'All tiles are flipped'})
    
    # Choose a random unflipped tile
    i, j = random.choice(unflipped)
    flipped_tiles.add((i, j))
    
    return jsonify({
        'success': True,
        'tile': f'tile_{i}_{j}.png'
    })

if __name__ == '__main__':
    app.run(debug=True)
