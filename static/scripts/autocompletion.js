var programInput = document.getElementById("program_title");
var dropdownMenu = document.getElementById("dropdown-menu");
var programId = document.getElementById("program_id");


programInput.addEventListener("input", function() {
  var inputText = programInput.value;

  if (inputText.length >= 3) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/autocomplete?input_text=" + inputText, true);
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        var suggestions = JSON.parse(xhr.responseText);

        // Populate the dropdown menu
        dropdownMenu.innerHTML = "";
        for (var i = 0; i < suggestions.length; i++) {
          var option = document.createElement("a");
          option.className = "dropdown-item";
          option.href = "#";
          option.value=suggestions[i].code;
          option.innerText = suggestions[i].code + ' - '+ suggestions[i].title;
          

          // Add event listener to suggestions
          option.addEventListener("click", function() {
            programInput.value = this.innerText;
            dropdownMenu.style.display = "none";
            programId.value = this.value;
          });

          dropdownMenu.appendChild(option);
        }

        if (suggestions.length > 0) {
          // Show the dropdown menu if there are suggestions
          dropdownMenu.style.display = "block";
        } else {
          // Hide the dropdown menu if there are no suggestions
          dropdownMenu.style.display = "none";
        }
      }
    };
    xhr.send();
  } else {
    // Hide the dropdown menu if the input length is less than 3
    dropdownMenu.style.display = "none";
  }
});

// Close the dropdown menu when clicking outside of it
window.addEventListener("click", function(event) {
  if (!programInput.contains(event.target)) {
    dropdownMenu.style.display = "none";
  }
});

// Close the dropdown menu when clicking outside of it
window.addEventListener("click", function(event) {
  if (!programInput.contains(event.target)) {
    dropdownMenu.style.display = "none";
  }
});

