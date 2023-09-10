// JavaScript code to fetch and display the schedule images
console.log(combinations)
// Function to fetch and display the schedule images
async function loadScheduleImages() {
  try {
    const response = await fetch('/generate_schedule_images', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ combinations }),
    });

    if (response.ok) {
      const imagesData = await response.json();
      const images = imagesData.images;

      // Loop through the images and display them in the corresponding containers
      images.forEach((imageBase64, index) => {
        const imageElement = document.createElement('img');
        imageElement.src = `data:image/png;base64,${imageBase64}`;
        imageElement.className = 'img-fluid';

        // Create a new div container for each image
        const imageContainer = document.createElement('div');
        imageContainer.className = 'img-container';
        imageContainer.appendChild(imageElement);

        // Append the image container to the schedulesList div
        const schedulesList = document.getElementById('schedulesList');
        schedulesList.appendChild(imageContainer);
      });
    } else {
      console.error('Error loading schedule images:', response.statusText);
    }
  } catch (error) {
    console.error('Error loading schedule images:', error);
  }
}

// Ensure the DOM is ready before loading schedule images
document.addEventListener('DOMContentLoaded', function () {
  loadScheduleImages();
});