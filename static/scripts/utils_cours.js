// onClick add button, change label's color and mark it
$(document).ready(function () {
  $(document).on("click", ".btn-add", function () {
    var button = $(this);
    var label = $(this).prev();
    var input = label.prev();

    input.addClass("actif");

    button.text("-");
    button.removeClass().addClass("btn btn-outline-danger btn-remove");

    label.removeClass("bg-light");
    label.css("background-color", "#7A6BFF");
    label.css("color", "#f8f9fa");
  });
});

// onClick remove button, revert changes
$(document).ready(function () {
  $(document).on("click", ".btn-remove", function () {
    var button = $(this);
    var label = $(this).prev();
    var input = label.prev();

    input.removeClass("actif");

    button.text("+");
    button.removeClass().addClass("btn btn-outline-success btn-add");

    label.addClass("bg-light");
    label.css("background-color", "");
    label.css("color", "#000");

  });
});

// ajax main form submission
$(document).ready(function () {
  $("#agendas").submit(function (event) {
    // fetch courses list
    var raw_list = $(".actif");
    var courses = [];
    raw_list.each(function () {
      var courseObj = {
        course_id: $(this).attr("id"),
        program_id: $(this).attr("name"),
      };
      courses.push(courseObj);
    });
    if (courses.length ==0 ){
      event.preventDefault();
      alert("Aucun cours selectionné");
      return 0;
    }
    //get semester id
    var semester = $('input[name="semester"]:checked').val();
    
    //get unavailability list
    var raw_unav_list = $(".unavailability");
    var unav_list = [];
    if(raw_list.length > 0){
    raw_unav_list.each(function () {
      var strings = $(this).val().split(","); 
      var unavailabilityObj = {
        day: strings[0],
        start_time: strings[1],
        end_time: strings[2],
      };
      unav_list.push(unavailabilityObj);
    });
  }

   //serialize data
  let formData;
  if(unav_list.length > 0){
   formData = {
      courses: JSON.stringify(courses),
      semester: JSON.stringify(semester),
      unavailability: JSON.stringify(unav_list) 
  }}
  else{
    formData = {
      courses: JSON.stringify(courses),
      semester: JSON.stringify(semester),
    };
  }
   console.log(formData);
   
    $.ajax({
      type: "GET",
      url: "/agendas",
      data: formData,
      success: function (response) {
        // Create a hidden form and submit it with the returned combinations
        var hiddenForm = $("<form>", {
          action: "/schedules",
          method: "POST",
          target: "_blank"
        });
        // Add the program_id as a hidden input field
        $("<input>")
          .attr({
            type: "hidden",
            name: "combinations",
            value: JSON.stringify(response),
          })
          .appendTo(hiddenForm);
        // Append the form to the body and submit it
        hiddenForm.appendTo("body").submit();
      },
      error: function (xhr) {
        if (xhr.status == 400) alert(xhr.responseJSON);
      },
    });
    event.preventDefault();
  });
});

///////////////////////////////////////////////
// SECTION FEATURE "AJOUTER COURS HORS PROGRAMME"

$(document).ready(function () {
  $("#recherche").on("click", function () {
    var SearchInput = $("#SearchInput").val();

    //if string valid
    if (SearchInput.length > 0 && SearchInput.length <= 10) {
      //if exist in page
      var elementExists = $('[id="' + SearchInput.toUpperCase() + '"]').length > 0;
      if (elementExists) {
        alert("Le cours est déja disponible.");
      } else {
        scrapeCourse(SearchInput);
      }
    } else {
      alert("valeur non acceptée");
    }
  });
});


// ajax request to fetch course data
function scrapeCourse(course_id) {
  let formData = {
    course_id: JSON.stringify(course_id),
  };
    $.ajax({
      type: "POST",
      url: "/horsProgramme",
      data: formData,
      success: function (response) {
        var sectionContainer = $("#horsProgContainer");
        var jsonObj = JSON.parse(response); 
        var element = $('<div>', { class: 'col mt-2' });
        var btnGroupDiv = $('<div>', { class: 'btn-group' });
        var minusButton = $('<button>', { type: 'button', class: 'btn btn-outline-danger remove-HP', text: '-' });
        var checkboxInput = $('<input>', { type: 'checkbox', id: course_id.toUpperCase(), class: 'btn-check shadow-lg actif', name: jsonObj.program_id });
        var label = $('<label>', { style: 'width: 120px;', class: 'btn bg-light border border-secondary', for: course_id.toUpperCase(), text: course_id.toUpperCase() });
        // var image = $('<img>', { src: '/static/images/computer.png', width: 15, height: 15, alt: '' });
       
        // label.append(image);
        btnGroupDiv.append(minusButton, checkboxInput, label);
        element.append(btnGroupDiv);
        
        sectionContainer.append(element);// You can perform additional actions or redirection here if needed
      },
      error: function (xhr) {
        if (xhr.status == 400) 
       alert(xhr.responseJSON);
      },
    });
  }
// onClick remove button
$(document).ready(function () {
  $(document).on("click", ".remove-HP", function () {
    $(this).parent().parent().remove();
  });
});

///////////////////////////////////////////////
// SECTION FEATURE "Ajouter indisponibilite"

$(document).ready(function() {
  var startSelect = $("#start_time");
  var endSelect = $("#end_time");
  var day = $("#day");

  // Function to populate the select elements with time options
  function populateTimeSelect(select) {
      for (var hour = 6; hour <= 23; hour++) {
          for (var minute = 0; minute < 60; minute += 30) {
              var displayHour = (hour < 10) ? "0" + hour : hour;
              var displayMinute = (minute === 0) ? "00" : minute;
              var optionValue = displayHour + ":" + displayMinute;
              select.append($("<option></option>")
                  .attr("value", optionValue)
                  .text(optionValue));
          }
      }
  }
  // Populate the select elements with time options
  populateTimeSelect(startSelect);
  populateTimeSelect(endSelect);


   // Add a click event listener to the button
   $("#btnUnav").on("click", function() {
    var selectedStartTime = startSelect.val();
    var selectedEndTime = endSelect.val();

    // Check if a valid option has been selected (not the placeholder)
    if (selectedStartTime && selectedEndTime && day.val()) {
        // Compare the start and end times
        if (selectedStartTime < selectedEndTime) {
            appendUnavailabilityElement(day.val(),selectedStartTime,selectedEndTime);
        } else {
            alert("La valeur de fin doit etre apres le debut.");
        }
    } else {
        alert("Selectionnez une valeur valide.");
    }
});

 // Function to populate the select elements with time options
 function appendUnavailabilityElement(day,start_time,end_time) {
  var sectionContainer = $("#UnavailabilityContainer");
  var element = $('<div>', { class: 'col-12 mt-2' });
  var btngroup = $('<div>', { class: 'btn-group' });
  var input = $('<input>', {type: 'checkbox', class: 'btn-check shadow-lg unavailability', value:day+","+start_time+","+end_time });
  var label = $('<label>', {class: 'btn bg-light border border-secondary', text: day + " : " + start_time + " à " + end_time });
  var minusButton = $('<button>', { type: 'button', class: 'btn btn-outline-danger remove-HP', text: '-' });

  btngroup.append(input, label, minusButton);
  element.append(btngroup);
  
  sectionContainer.append(element);
  }

});
