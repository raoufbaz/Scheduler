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
    
   
    console.log(label.text());
  });
});

// onClick remove button, change label's color
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
      
      console.log(label.text());
    });
  });

// ajax submission
$(document).ready(function () {
    $("#agendas").submit(function (event) {
      
      // fetch courses list 
      var raw_list = $(".actif");
      var courses = [];
      raw_list.each(function( index ) {
      courses.push($( this ).attr('id'));
      });

      let formData = {
        courses: JSON.stringify(courses)
    };
        $.ajax({
            type: "GET",
            url: "/agendas",
            data: formData,
            success: function (response) {
              alert("success" + response);
            },
            error: function (xhr) {
                alert("error : " + xhr);
            }
        });
        event.preventDefault();
    });
});