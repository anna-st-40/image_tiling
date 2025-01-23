# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
import unittest

from server.app import hex_to_rgb, validate_tile_colors


class TestHexToRgb(unittest.TestCase):
    """Test the hex_to_rgb function."""

    def test_valid_hex(self):
        self.assertEqual(hex_to_rgb("FFFFFF"), (255, 255, 255))  # White
        self.assertEqual(hex_to_rgb("000000"), (0, 0, 0))  # Black
        self.assertEqual(hex_to_rgb("A52A2A"), (165, 42, 42))  # Brown
        self.assertEqual(hex_to_rgb("008000"), (0, 128, 0))  # Green

    def test_lowercase_hex(self):
        self.assertEqual(hex_to_rgb("ff00ff"), (255, 0, 255))  # Magenta (lowercase)

    def test_invalid_hex(self):
        with self.assertRaises(ValueError):
            hex_to_rgb("GGGGGG")  # Invalid hex digits

        with self.assertRaises(ValueError):
            hex_to_rgb("1234")  # Incomplete hex string


class TestValidateTileColors(unittest.TestCase):
    """Test the validate_tile_colors function."""

    def test_valid_tile_colors(self):
        tile_colors = '["#FF0000", "#00FF00", "#0000FF"]'
        result = validate_tile_colors(tile_colors)
        self.assertEqual(result, ["#FF0000", "#00FF00", "#0000FF"])

    def test_valid_tile_colors_lowercase(self):
        tile_colors = '["#ff0000", "#00ff00", "#0000ff"]'
        result = validate_tile_colors(tile_colors)
        self.assertEqual(result, ["#ff0000", "#00ff00", "#0000ff"])

    def test_valid_short_hex_codes(self):
        tile_colors = '["#F00", "#0F0", "#00F"]'
        result = validate_tile_colors(tile_colors)
        self.assertEqual(result, ["#F00", "#0F0", "#00F"])

    def test_invalid_color_format(self):
        tile_colors = '["FF0000", "#00GG00"]'
        with self.assertRaises(ValueError) as context:
            validate_tile_colors(tile_colors)
        self.assertEqual(
            str(context.exception),
            "tile_colors must be a valid JSON list of hex color codes (e.g., ['#FF0000', '#00FF00'])",
        )

    def test_non_string_elements(self):
        tile_colors = '["#FF0000", 12345]'
        with self.assertRaises(ValueError) as context:
            validate_tile_colors(tile_colors)
        self.assertEqual(
            str(context.exception),
            "tile_colors must be a valid JSON list of hex color codes (e.g., ['#FF0000', '#00FF00'])",
        )

    def test_empty_list(self):
        tile_colors = "[]"
        result = validate_tile_colors(tile_colors)
        self.assertEqual(result, [])

    def test_invalid_json_format(self):
        tile_colors = '"#FF0000, #00FF00"'
        with self.assertRaises(ValueError) as context:
            validate_tile_colors(tile_colors)
        self.assertEqual(
            str(context.exception),
            "tile_colors must be a valid JSON list of hex color codes (e.g., ['#FF0000', '#00FF00'])",
        )

    def test_missing_hash_prefix(self):
        tile_colors = '["FF0000", "00FF00"]'
        with self.assertRaises(ValueError) as context:
            validate_tile_colors(tile_colors)
        self.assertEqual(
            str(context.exception),
            "tile_colors must be a valid JSON list of hex color codes (e.g., ['#FF0000', '#00FF00'])",
        )


if __name__ == "__main__":
    unittest.main()
