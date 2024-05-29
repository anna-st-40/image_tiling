from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist

tile_colors = [
    (255,   0,   0), # Red
    (  0,   0,   0), # Black
    (128, 128, 128), # Gray
    (255, 255, 255)  # White
]


def reduce_image_colors(image: Image, n_colors=4):
    """
    Reduces the number of colors in an image to n_colors.
    This method uses KMeans clustering to find the dominant colors in the image.

    Returns a tuple of the image and the colors used.
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
    return (new_image, [tuple(l) for l in new_colors.tolist()])

def remap_colors(found_colors: list[tuple], specified_colors: list[tuple]) -> dict:
    """
    Generates a map between the found colors and the closest specified colors.
    """
    # Calculate distances between each found color and each specified color
    distances = cdist(found_colors, specified_colors, metric='euclidean')
    
    # Find the closest found color for each specified color
    closest_indices = np.argmin(distances, axis=0)

    # Map the found colors to specified colors
    final_mapping = {}
    j = 0
    for i in closest_indices:
        final_mapping[found_colors[i]] = specified_colors[j]
        j += 1

    # Return the final mapping
    return final_mapping

def apply_color_remapping(image: Image, color_mapping: dict) -> Image:
    """
    Apply the color remapping to the image.
    """
    # Convert image data to a numpy array
    image_data = np.array(image)
    original_shape = image_data.shape
    pixels = image_data.reshape(-1, 3)

    # Apply the color mapping
    new_pixels = np.array([color_mapping[tuple(pixel)] for pixel in pixels])
    new_image_data = new_pixels.reshape(original_shape)

    # Create a new image from the mapped color data
    new_image = Image.fromarray(new_image_data.astype('uint8'))

    return new_image


def tile_image(image_path, tile_colors, pixel_dimensions=50):
    # Open the image
    org_image = Image.open(image_path)

    # Pixelate (downscale) the image
    pixelated = org_image.resize((pixel_dimensions,pixel_dimensions))
    
    # Reduce image colors
    reduced, found_colors = reduce_image_colors(pixelated, n_colors=len(tile_colors))

    # Remap image colors
    color_map = remap_colors(found_colors, tile_colors)
    remapped = apply_color_remapping(reduced, color_map)

    # Upscale the image back
    upscaled = remapped.resize(org_image.size,Image.NEAREST)

    # Show the image
    upscaled.show()

tile_image("test_image_1.jpg", tile_colors, 25)