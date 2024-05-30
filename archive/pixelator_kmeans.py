"""
(Anna Stefaniv 2024-05-29 14:55)

This script is able to pixelate any image into a given number of n×n pixels (default 50×50)
and using only a specified number of different colors (default 4).

This algorithm finds which colors to convert to using KMeans clustering.

This was an intermediary step to building a full script to tile an image into only given colors.
"""

from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

def reduce_image_colors(image: Image, n_colors=4) -> Image:
    """
    Reduces the number of colors in an image to n_colors.
    This method uses KMeans clustering to find the dominant colors in the image.
    """
    
    # Convert image data to a numpy array
    org_image = image.convert('RGB')
    image_data = np.array(org_image)
    original_shape = image_data.shape
    pixels = image_data.reshape(-1, 3)

    # Apply KMeans to find clusters (colors)
    kmeans = KMeans(n_clusters=n_colors, random_state=42)
    kmeans.fit(pixels)
    new_colors = kmeans.cluster_centers_.astype(int)
    labels = kmeans.labels_

    # Create new image data with reduced colors
    new_image_data = new_colors[labels].reshape(original_shape)

    # Create a new image from the reduced color data
    new_image = Image.fromarray(new_image_data.astype('uint8'))

    # Return the image
    return new_image

def tile_image(image_path, pixel_dimensions=50, n_colors=4):
    # Open the image
    org_image = Image.open(image_path)

    # Pixelate (downscale) the image
    pixelated = org_image.resize((pixel_dimensions,pixel_dimensions))
    
    # Reduce image colors
    reduced = reduce_image_colors(pixelated, n_colors)

    # Upscale the image back
    upscaled = reduced.resize(org_image.size,Image.NEAREST)

    # Show the image
    upscaled.show()

    # # Save the image
    upscaled.save("test_image_3.png")
    # print(f"Saved reduced color image to {output_path}")



tile_image('test_image_2.jpg', 50)