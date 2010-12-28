$(document).ready(function() {
  // bind contact-us form submit to ajax submit
  $('#contact-us-form').submit(function() {
    var form = $(this);
    var submit_button = form.find('button[name="contact-us-submit"]');
    var submit_results = form.find('.submit-results');

    $.ajax({
      url: form.attr('action'),
      type: 'POST',
      data: form.serialize(),
      dataType: 'json',
      beforeSend: function () {
        form.find('.input-error').empty();
        submit_results.html('<div class="preloader-2"></div>');
        submit_button.attr('disabled', 'disabled');
      },
      error: function () {
        submit_results.html('<p class="error">Request timed-out, please try again.</p>');
      },
      success: function(response){
        if (response.success) {
          submit_results.html('<p class="success">Form was succesfully submitted.</p>');
        }
        else {
          submit_results.empty();
          $.each(response.errors, function(field, error) {
            var input_field = form.find(':input[name="'+field+'"]');
            // if there is no input field which matches field key => add errors to global container
            if (input_field.length === 0) {
              submit_results.append('<p class="error">'+error+'</p>');
            }
            // else insert error into input-errors container next to corresponding input field
            else {
              input_field.siblings('.input-error').html('<p>'+error+'</p>');
            }
          });
        }
      },
      complete: function() {
        submit_button.removeAttr('disabled');
      }
    });

    return false;
  });

});
