# Image Tiling

This projects contains a Python script for reducing the number of colors in an image and transforming it into a pixelated version using predefined tile colors. This project uses KMeans clustering to identify dominant colors in the image and maps them to a set of predefined colors.

## Demo

### Step 0 - Original Image
![Original Image](demo_images/step_0.jpg)

### Step 1 - Pixelate image
The image is pixelated to 25×25 pixels by downscaling using the PIL resize function.
![Pixelated Image](demo_images/step_1.jpg)


### Step 2 - Reduce Colors
The image is reduced to 4 colors using KMeans clustering to find the dominant colors in the image. 
![Reduced Colors](demo_images/step_2.jpg)

### Step 3 - Remap Colors
The four found colors are remapped to a set of predefined colors - red, white, black, and gray.
<br> This is accomplished by calculating the Euclidean distances in RGB space between the found and predefined colors.
![Remapped Colors](demo_images/step_3.jpg)

## How to Run

### Option 1 (easiest): Web Interface
Go to [https://anna-st-40.github.io/image_tiling/](https://anna-st-40.github.io/image_tiling/) to use the web interface for this project.

### Option 2: Run locally
To run the Python script and generate your own image locally, simply use `server\pixelator.py`. Make sure to put your own parameters under 
```
if __name__ == "__main__":
```
and save the file to your desired location.

The requirements to run this script are:
```
joblib==1.4.2
numpy==2.2.1
pillow==11.1.0
scikit-learn==1.6.1
scipy==1.15.1
threadpoolctl==3.5.0
```

### Option 3: Call API
You can also send an API request to [https://image-tiling-api.onrender.com/](https://image-tiling-api.onrender.com/), which runs the same Python file on a Flask server. It deletes your image as soon as you receive it.

**Request**
- **Content-Type:** `multipart/form-data`
- **Body Parameters:**
    - `image` (required): The image file to be processed.
    - `tile_colors` (optional): A JSON list of hex color codes to use for the tiles. If not provided, the default colors are used.
    - `pixel_dimensions` (optional): The side length of the final dimension in tiles. Default value is 50.

**Response**

If the request is successful, you will receive the processed image in PNG format.