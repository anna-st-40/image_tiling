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