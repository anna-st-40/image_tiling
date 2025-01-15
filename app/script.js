const uploadArea = document.getElementById('image-upload');
const fileInput = document.getElementById('file-input');
const previewContainer = document.getElementById('image-display-1');
const tiledContainer = document.getElementById('image-display-2');
const previewImage = document.getElementById('image-preview');
const tiledImage = document.getElementById('image-tiled');
const generateButton = document.getElementById('generate-image');
const colors = document.querySelectorAll('.color');
const pixelSize = document.getElementById('pixel-size-value');

// Utility function to prevent default browser behavior
function preventDefaults(e) {
  e.preventDefault();
  e.stopPropagation();
}

// Preventing default browser behavior when dragging a file over the container
uploadArea.addEventListener('dragover', preventDefaults);
uploadArea.addEventListener('dragenter', preventDefaults);
uploadArea.addEventListener('dragleave', preventDefaults);


// Handling clicking the area to upload files
uploadArea.addEventListener('click', () => {
  fileInput.click();
});
fileInput.addEventListener('change', () => {
  const file = fileInput.files[0];
  if (file) {
    handleFile(file);
  }
});

// Handling dropping files into the area
uploadArea.addEventListener('drop', dropHandler);
function dropHandler(e) {
  // Prevent default behavior (Prevent file from being opened)
  e.preventDefault();

  // Getting the list of dragged files
  const files = e.dataTransfer.files;

  if (files.length) {
    // Assigning the files to the hidden input
    fileInput.files = files;

    // Processing the files for previews
    handleFile(files[0]);
  }
}

// Helper functions for handling file uploads
function handleFile(file) {
  // Initializing the FileReader API and reading the file
  const reader = new FileReader();
  reader.readAsDataURL(file);

  // Once the file has been loaded, fire the processing
  reader.onloadend = function (e) {

    if (isValidFileType(file)) {
      uploadArea.style.display = 'none';
      previewImage.src = e.target.result;
      previewContainer.style.display = 'block';
    }
  };
}
function isValidFileType(file) {
  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
  return allowedTypes.includes(file.type);
}



const apiURL = "https://image-tiling-api.onrender.com/";

// Event listener for the "Generate" button click
generateButton.addEventListener("click", async () => {
  const imageFile = fileInput.files[0];

  if (!imageFile) {
    alert("Please select an image file first!");
    return;
  }

  // Create a FormData object to hold the file and data
  const formData = new FormData();
  formData.append("image", imageFile)

  const tileColors = JSON.stringify(Array.from(colors, color => color.value));
  const pixelDimensions = parseInt(pixelSize.textContent, 10);
  formData.append("tile_colors", tileColors);
  formData.append("pixel_dimensions", pixelDimensions);

  try {
    // Send the POST request using fetch
    const response = await fetch(apiURL, {
      method: "POST",
      body: formData,
    });

    // Check the response
    if (response.ok) {
      const image = await response.blob();

      // Create a URL for the returned image
      const processedImageUrl = URL.createObjectURL(image);

      // Display the processed image
      previewContainer.style.display = 'none';
      tiledImage.src = processedImageUrl;
      tiledContainer.style.display = 'block';
      
      console.log("Image processed successfully.");
    } else {
      const error = await response.json();
      console.error("Error:", response.status, error);
      alert(`Error: ${response.status} - ${error.message}`);
    }
  } catch (error) {
    console.error("Error:", error);
    // alert("An unexpected error occurred.");
  }
});

// Get the file input element and the button

// // Event listener for when the user clicks the 'Generate Image' button
// generateButton.addEventListener("click", function () {
//     // Get the selected file from the input
//     const imageFile = fileInput.files[0];

//     if (imageFile) {
//         // Get the color values from the color inputs
//         const tileColors = [
//             document.getElementById("color1").value,
//             document.getElementById("color2").value,
//             document.getElementById("color3").value,
//             document.getElementById("color4").value
//         ];

//         // Get the pixel dimensions from the 'pixel-size-value' element
//         const pixelDimensions = parseInt(document.getElementById('pixel-size-value').textContent, 10);

//         // Create a FormData object to hold the image file
//         const formData = new FormData();

//         // Add the image file to the FormData object
//         formData.append("image", imageFile);

//         // Add the optional parameters to the FormData object
//         formData.append("tile_colors", JSON.stringify(tileColors));
//         formData.append("pixel_dimensions", pixelDimensions);

//         // Send the POST request using fetch
//         fetch(url, {
//             method: "POST",
//             body: formData
//         })
//             .then(response => response.blob())  // Handle the response as a Blob (image)
//             .then(blob => {
//                 if (blob.size > 0) {
//                     // Create an object URL for the Blob to be used as the image source
//                     const imageURL = URL.createObjectURL(blob);

//                     // Create a new image element
//                     const image = new Image();
//                     image.src = imageURL;

//                     // Wait for the image to load, then draw it on the canvas
//                     image.onload = function () {
//                         // Set the canvas size to match the image size
//                         canvas.width = image.width;
//                         canvas.height = image.height;

//                         // Draw the image onto the canvas
//                         ctx.drawImage(image, 0, 0);
//                         console.log("Image processed and displayed on the canvas.");
//                     };
//                 } else {
//                     console.log("Error: Image processing failed.");
//                 }
//             })
//             .catch(error => {
//                 console.log("Error:", error);
//             });
//     } else {
//         console.log("No file selected.");
//     }
// });
