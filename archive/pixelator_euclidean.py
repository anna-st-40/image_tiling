"""
(Anna Stefaniv 2024-05-29 14:58)

This script is able to pixelate any image into a given number of n×n pixels (default 50×50)
and make it only use a specific list of colors 
by calculating the shortest Euclidean distance in RGB space for each pixel.

This was an intermediary step to building a full script to tile an image into only given colors,
and this idea was scrapped due to the resulting image being ugly.
"""

from PIL import Image, ImageEnhance
import numpy as np


def find_closest_color(pixel: list, colors: list[list]):
    """
    Find the closest color from the predefined colors using Euclidean distance.
    """
    colors = np.array(colors)
    distances = np.sqrt(np.sum((colors - pixel) ** 2, axis=1))
    closest_color_index = np.argmin(distances)
    return colors[closest_color_index]


def increase_saturation(image, factor=3):
    """
    Increase the saturation of an image by a given factor.
    """
    enhancer = ImageEnhance.Color(image)
    enhanced_image = enhancer.enhance(factor)
    return enhanced_image


def reduce_image_to_specified_colors(image: Image, specified_colors: list[list]):
    """
    Reduce the image colors to the specified four colors.
    """
    image = image.convert("RGB")

    # Increase saturation
    image = increase_saturation(image)

    # Convert image data to a numpy array
    image_data = np.array(image)
    original_shape = image_data.shape

    # Flatten the image array for easier processing
    flattened_image_data = image_data.reshape(-1, 3)

    # Map each pixel to the closest specified color
    reduced_colors_data = np.array(
        [find_closest_color(pixel, specified_colors) for pixel in flattened_image_data]
    )

    # Reshape the reduced colors data to the original image shape
    reduced_image_data = reduced_colors_data.reshape(original_shape)

    # Create a new image from the reduced color data
    new_image = Image.fromarray(reduced_image_data.astype("uint8"))

    # Return the new image
    return new_image


def tile_image(image_path, specified_colors: list[list], pixel_dimensions=50):

    # Open the image
    org_image = Image.open(image_path)

    # Pixelate (downscale) the image
    pixelated = org_image.resize((pixel_dimensions, pixel_dimensions))

    # Reduce image colors
    reduced = reduce_image_to_specified_colors(pixelated, specified_colors)

    # Upscale the image back
    upscaled = reduced.resize(org_image.size, Image.NEAREST)

    # Show the image
    upscaled.show()


specified_colors = [
    [255, 0, 0],  # Red
    [0, 0, 0],  # Black
    [128, 128, 128],  # Gray
    [255, 255, 255],  # White
]

tile_image("test_image_1.jpg", specified_colors, pixel_dimensions=50)
