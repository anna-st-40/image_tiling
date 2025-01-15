const uploadArea = document.getElementById('image-upload');
const fileInput = document.getElementById('file-input');
const previewContainer = document.getElementById('image-display-1');
const tiledContainer = document.getElementById('image-display-2');
const previewImage = document.getElementById('image-preview');
const tiledImage = document.getElementById('image-tiled');

const generateButton = document.getElementById('generate-image');
const downloadButton = document.getElementById('download-image');
const resetButton = document.getElementById('reset-image');

const downloadLink = document.getElementById('download-link');

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

  // Update the button text and style to indicate processing
  generateButton.innerHTML = "Generating...";
  generateButton.style.cursor = "wait";
  generateButton.addEventListener("mouseover", disableHover);
  function disableHover() {
    generateButton.style.backgroundColor = "#027AFF";
  }

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
      
      // Update buttons and log success
      generateButton.innerHTML = "Regenerate Image";
      generateButton.style.cursor = "pointer";
      generateButton.removeEventListener("mouseover", disableHover);
      downloadButton.style.display = 'inline-block';
      resetButton.style.display = 'inline-block';

      console.log("Image processed successfully.");
    } else {
      const error = await response.json();
      console.error("Error:", response.status, error);
      alert(`Error: ${response.status} - ${error.message}`);
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An unexpected error occurred.");
  }
});

// Event listener for the Download" button click
downloadButton.addEventListener("click", () => {
  downloadLink.href = tiledImage.src;
  downloadLink.click();
});

// Event listener for the "Reset" button click
resetButton.addEventListener("click", () => {
  uploadArea.style.display = 'flex';
  previewContainer.style.display = 'none';
  tiledContainer.style.display = 'none';
  fileInput.value = '';
  tiledImage.src = '';
  generateButton.innerHTML = "Generate Image";
  generateButton.style.cursor = "pointer";
  downloadButton.style.display = 'none';
  resetButton.style.display = 'none';
});