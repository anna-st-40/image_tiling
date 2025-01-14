# pylint: disable=missing-module-docstring
# pylint: disable=broad-exception-caught

import json
import os
import sys
from io import BytesIO

from flask import Flask, request, send_file
from flask_cors import CORS

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from server.pixelator import tile_image


app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

default_tile_colors = (
    '#FF0000',  # Red
    '#000000',  # Black
    '#808080',  # Gray
    '#FFFFFF',  # White
)


@app.route("/", methods=["POST"])
def process_image():
    """Route for processing an image and returning the tiled version."""

    if "image" not in request.files:
        return {"error": "No image file provided"}, 400

    image_file = request.files["image"]

    # Get optional parameters from the request
    tile_colors = request.form.get(
        "tile_colors", json.dumps(default_tile_colors), type=str)
    try:
        if tile_colors:
            tile_colors = validate_tile_colors(tile_colors)
            tile_colors = [hex_to_rgb(color[1:]) for color in tile_colors]
    except ValueError as e:
        return {"error": str(e)}, 400

    pixel_dimensions = request.form.get("pixel_dimensions", 50, type=int)

    # Save the uploaded file
    input_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
    image_file.save(input_path)

    try:
        # Process the image
        processed_image = tile_image(input_path, tile_colors, pixel_dimensions)

        # Save the processed image to an in-memory buffer
        buffer = BytesIO()
        processed_image.save(buffer, format="PNG")
        buffer.seek(0)

        # Clean up the input file
        os.remove(input_path)

        return send_file(buffer, mimetype="image/png")

    except Exception as e:
        return {"error": str(e)}, 500


def hex_to_rgb(hex_color: str) -> tuple:
    """Convert a hex color code to an RGB tuple.

    Args:
        hex_color (str): A hex color code without the octothorpe (e.g., "FF0000").

    Returns:
        tuple: An RGB tuple (e.g., (255, 0, 0)).
    """
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def validate_tile_colors(tile_colors):
    """Validate the tile_colors parameter.

    Args:
        tile_colors (str): A JSON string representing a list of hex color codes.

    Returns:
        list: A list of validated hex color codes.

    Raises:
        ValueError: If the tile_colors format is invalid.
    """
    try:
        colors = json.loads(tile_colors)
        if not all(isinstance(color, str)
                   and color.startswith("#")
                   and len(color) in [7, 4] for color in colors):
            raise ValueError("Invalid hex color format")
        for color in colors:
            if not all(char in "0123456789ABCDEFabcdef" for char in color[1:]):
                raise ValueError("Invalid hex color format")
        return colors
    except (json.JSONDecodeError, ValueError) as exc:
        raise ValueError(
            "tile_colors must be a valid JSON list of hex color codes (e.g., ['#FF0000', '#00FF00'])") from exc


if __name__ == "__main__":
    app.run(debug=True)
