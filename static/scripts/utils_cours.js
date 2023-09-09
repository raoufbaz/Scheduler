// onClick add button, change label's color and mark it
$(document).ready(function() {
    $(document).on('click', '.btn-add', function() {
    var button = $(this);
    var label = $(this).prev();
    var input = label.prev();

    input.addClass('actif');

    button.text('-');
    button.removeClass().addClass("btn btn-outline-danger btn-remove");

    label.removeClass("bg-light");
    label.css('background-color','#7A6BFF');
    label.css('color', '#f8f9fa');
    
  });
});

// onClick remove button, revert changes
$(document).ready(function() {
    $(document).on('click', '.btn-remove', function() {
      var button = $(this);
      var label = $(this).prev();
      var input = label.prev();

      input.removeClass('actif');

      button.text('+');
      button.removeClass().addClass("btn btn-outline-success btn-add");

      label.addClass("bg-light");
      label.css('background-color','');
      label.css('color','#000');
      
    });
  });


// ajax main form submission
$(document).ready(function () {
    $("#agendas").submit(function (event) {
      
      // fetch courses list 
      var raw_list = $(".actif");
      var courses = [];
      raw_list.each(function( index ) {
        var courseObj = {
          course_id: $( this ).attr('id'),
          program_id: $( this ).attr('name')
      }
      courses.push(courseObj);
      });

      //get semester id
      var semester = $("input[name='semester']").val();
      
      //serialize data
      let formData = {
        courses: JSON.stringify(courses),
        semester: JSON.stringify(semester),
    };
        $.ajax({
            type: "GET",
            url: "/agendas",
            data: formData,
            success: function (response) {
              alert("success! check browser console for object");
              console.log(response);
            },
            error: function (xhr) {
              if(xhr.status == 400)
                alert(xhr.responseJSON);
            }
        });
        event.preventDefault();
    });
});