from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import itertools
from math import inf

tile_colors = [
    (255,   0,   0), # Red
    (  0,   0,   0), # Black
    (128, 128, 128), # Gray
    (255, 255, 255)  # White
] 

def reduce_image_colors(image: Image, n_colors=4) -> tuple[Image, list[tuple]]: # type: ignore
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
    Generates a map between the found colors and the closest specified colors,
    based on the Euclidean distance between the colors.
    """

    # Calculate distances between each found color and each specified color
    distances = cdist(found_colors, specified_colors, metric='euclidean')

    # Generate all permutations of the colors
    items = [i for i in range(len(found_colors))]
    permutations = itertools.permutations(items)
    perm_map = []
    for perm in permutations:
        perm_map.append([(items[i], perm[i]) for i in range(len(items))])

    # Calculate the sum of all distances for each permutation, and find the combination that produces the minimum
    min_distance = [inf, None]
    for map in perm_map:
        total_distance = 0

        for j in range(len(map)):
            total_distance += distances[map[j][0]][map[j][1]]
        
        if total_distance < min_distance[0]:
            min_distance = [total_distance, map]

    # Create a dictionary mapping the found colors to the specified colors
    final_mapping = {found_colors[i[0]] : specified_colors[i[1]] for i in min_distance[1]}
    
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


def tile_image(image_path, tile_colors=tile_colors, pixel_dimensions=50) -> Image:
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
    return upscaled

if __name__ == "__main__":
    tile_image("test_image_1.jpg", tile_colors, 25)