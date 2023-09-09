// JavaScript code to fetch and display the schedule image
const imageContainers = document.querySelectorAll('.img-fluid');
  
// Function to fetch and display the schedule image
async function loadScheduleImage(imageId) {
  try {
    const response = await fetch('/generate_schedule_image');
    if (response.ok) {
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const imageElement = document.getElementById(imageId);
      imageElement.src = url;
    }
  } catch (error) {
    console.error('Error loading schedule image:', error);
  }
}

// Load schedule images when the page loads
for (let i = 0; i < imageContainers.length; i++) {
  const imageId = `scheduleImage${i + 1}`;
  loadScheduleImage(imageId);
}