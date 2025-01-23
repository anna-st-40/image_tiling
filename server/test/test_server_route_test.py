"""Test the server routes."""

from io import BytesIO
import unittest

from server.app import app


class AppTestCase(unittest.TestCase):
    """Test the server routes."""

    def setUp(self):
        app.testing = True
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_process_image_success(self):
        """Test the process_image route with a valid image file."""

        with open("test_image_1.jpg", "rb") as image_file:

            response = self.client.post(
                "/",
                data={
                    "image": (BytesIO(image_file.read()), "test_image_1.jpg"),
                    "tile_colors": '["#FFFFFF", "#000000", "#A52A2A", "#008000"]',
                    "pixel_dimensions": 25,
                },
                content_type="multipart/form-data",
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "image/png")

    def test_process_image_missing_image(self):
        """Test the route when no image file is provided."""
        response = self.client.post(
            "/",
            data={
                "tile_colors": '["#FFFFFF", "#000000", "#A52A2A", "#008000"]',
                "pixel_dimensions": 25,
            },
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "No image file provided")

    def test_process_image_invalid_tile_colors(self):
        """Test the route when invalid tile colors are provided."""

        response = self.client.post("/", data={"image": "test_image_1.jpg"})
        self.assertEqual(response.status_code, 400)

        with open("test_image_1.jpg", "rb") as image_file:

            response = self.client.post(
                "/",
                data={
                    "image": (BytesIO(image_file.read()), "test_image_1.jpg"),
                    "tile_colors": '["#FFGGFF", "#UU0000", "#A52A2A", "#008000"]',
                    "pixel_dimensions": 25,
                },
                content_type="multipart/form-data",
            )

        self.assertEqual(response.status_code, 400)
        self.assertIn(  # codespell:ignore
            "tile_colors must be a valid JSON list", response.json["error"]
        )

    def test_process_image_missing_optional_params(self):
        """Test the route when optional parameters are not provided."""

        with open("test_image_1.jpg", "rb") as image_file:

            response = self.client.post(
                "/",
                data={
                    "image": (BytesIO(image_file.read()), "test_image_1.jpg"),
                },
                content_type="multipart/form-data",
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "image/png")


if __name__ == "__main__":
    unittest.main()
