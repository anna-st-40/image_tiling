# pylint: disable=missing-module-docstring
import os
import unittest
from PIL import Image
import numpy as np

from server import pixelator


class TestImageProcessing(unittest.TestCase):
    """Tests for the image processing functions."""

    def setUp(self):
        self.test_image_path_1 = 'server/test/test_image_1.jpg'
        self.test_image_path_2 = 'server/test/test_image_2.bmp'
        self.result_image_path = 'server/test/result.jpg'

        if not os.path.exists(self.test_image_path_1):
            self.fail(
                f"""Test image {self.test_image_path_1} is missing. 
                Please include it in the test directory.""")

        if not os.path.exists(self.test_image_path_2):
            self.fail(
                f"""Test image {self.test_image_path_2} is missing. 
                Please include it in the test directory.""")

        if not os.path.exists(self.result_image_path):
            self.fail(
                f"""Test image {self.result_image_path} is missing. 
                Please include it in the test directory.""")

    def test_reduce_image_colors(self):
        """Test the color reduction to n colors."""
        with Image.open(self.test_image_path_1) as mock_image:
            reduced_image, colors = pixelator.reduce_image_colors(
                mock_image, n_colors=4)

            # Assert the reduced image has the correct size
            self.assertEqual(reduced_image.size, mock_image.size)

            # Assert the number of colors is correct
            self.assertEqual(len(colors), 4)

            # Assert the colors are unique
            self.assertEqual(len(set(colors)), 4)

            # Assert the colors are correct
            self.assertTrue(all(color in colors for color in [
                            (238, 150, 122), (79, 66, 51), (194, 180, 183), (146, 120, 110)]))

    def test_remap_colors(self):
        """Test the remapping of colors."""
        found_colors = [(250, 0, 0), (0, 0, 0)]
        specified_colors = [(255, 0, 0), (128, 128, 128)]

        color_map = pixelator.remap_colors(found_colors, specified_colors)

        # Assert all found colors are mapped to specified colors
        self.assertTrue(
            all(color in specified_colors for color in color_map.values()))
        self.assertEqual(color_map[(250, 0, 0)], (255, 0, 0))
        self.assertEqual(color_map[(0, 0, 0)], (128, 128, 128))

    def test_apply_color_remapping(self):
        """Test applying the color remapping to an image."""
        with Image.open(self.test_image_path_2) as mock_image:

            # Simulate a remapping where all pixels are mapped to black
            color_mapping = {
                (34, 177, 76): (0, 0, 0),
                (63, 72, 204): (0, 0, 0),
                (237, 28, 36): (0, 0, 0),
                (255, 255, 255): (0, 0, 0)
            }

            remapped_image = pixelator.apply_color_remapping(
                mock_image, color_mapping)
            remapped_data = np.array(remapped_image)

            # Assert all pixels are remapped correctly to black
            self.assertTrue(np.all(remapped_data == [0, 0, 0]))

    def test_tile_image(self):
        """Test the full tiling process."""

        result_image = pixelator.tile_image(
            self.test_image_path_1, pixel_dimensions=25)

        # Make sure it ran without errors
        self.assertIsNotNone(result_image)


if __name__ == '__main__':
    unittest.main()
