$(document).ready(function () {

  $('#email').blur(function () {
    var email = $('#email').val();
    if (IsEmail(email) == false) {
      $('#register').attr('disabled', true);
      $('#popover-email').removeClass('hide');
    } else {
      $('#popover-email').addClass('hide');
    }
  });

  $('#password1').keyup(function () {
    var password = $('#password1').val();
    if (Boolean(checkStrength(password)) == false) {
      $('#register').attr('disabled', true);
    } else {
      $('#register').attr('disabled', false);
    }
  });


  $('#password2').keyup(function () {
    console.log("p1 p2: ", $('#password1').val(), $('#password2').val(), $('#password1').val() !== $('#password2').val())
    if ($('#password1').val() !== $('#password2').val()) {
      $('#popover-cpassword').removeClass('hide');
      $('#register').attr('disabled', true);
    } else {
      $('#popover-cpassword').addClass('hide');
      $('#register').attr('disabled', false);
    }
  });


  $('#id_phone').keyup(function () {
    var _phone = $('#id_phone').val();

    var cleaned_phone = _phone.replace("+966", "");

    var prefixed_phone = "+966" + cleaned_phone;

    $('#id_phone').val(prefixed_phone);

  });


  $('#register').hover(function () {
    if ($('#register').prop('disabled')) {
      $('#register').popover({
        html: true,
        trigger: 'hover',
        placement: 'below',
        offset: 20,
        content: function () {
          return $('#register-popover').html();
        }
      });
    }
  });

  function IsEmail(email) {
    var regex = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    if (!regex.test(email)) {
      return false;
    } else {
      return true;
    }
  }

  function checkStrength(password) {
    var strength = 0;


    //If password contains both lower and uppercase characters, increase strength value.
    if (password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)) {
      strength += 1;
      $('.low-upper-case').addClass('text-success');
      $('.low-upper-case span').removeClass('icon-info').addClass('icon-check');
      $('#popover-password-top').addClass('hide');

    } else {
      $('.low-upper-case').removeClass('text-success');
      $('.low-upper-case span').removeClass('icon-check').addClass('icon-info');
      $('#popover-password-top').removeClass('hide');
    }

    //If it has numbers and characters, increase strength value.
    if (password.match(/([a-zA-Z])/) && password.match(/([0-9])/)) {
      strength += 1;
      $('.one-number').addClass('text-success');
      $('.one-number span').removeClass('icon-info').addClass('icon-check');
      $('#popover-password-top').addClass('hide');

    } else {
      $('.one-number').removeClass('text-success');
      $('.one-number i').addClass('icon-check').removeClass('icon-info');
      $('#popover-password-top').removeClass('hide');
    }

    //If it has one special character, increase strength value.
    if (password.match(/([!,%,&,@,#,$,^,*,?,_,~])/)) {
      strength += 1;
      $('.one-special-char').addClass('text-success');
      $('.one-special-char span').removeClass('icon-info').addClass('icon-check');
      $('#popover-password-top').addClass('hide');

    } else {
      $('.one-special-char').removeClass('text-success');
      $('.one-special-char span').removeClass('icon-check').addClass('icon-info');
      $('#popover-password-top').removeClass('hide');
    }

    if (password.length > 7) {
      strength += 1;
      $('.eight-character').addClass('text-success');
      $('.eight-character span').removeClass('icon-info').addClass('icon-check');
      $('#popover-password-top').addClass('hide');

    } else {
      $('.eight-character').removeClass('text-success');
      $('.eight-character span').removeClass('icon-check').addClass('icon-info');
      $('#popover-password-top').removeClass('hide');
    }




    // If value is less than 2

    if (strength < 2) {
      $('#result').removeClass()
      $('#password-strength').addClass('progress-bar-danger');

      $('#result').addClass('text-danger').text('Very Week');
      $('#password-strength').css('width', '10%');
    } else if (strength == 2) {
      $('#result').addClass('good');
      $('#password-strength').removeClass('progress-bar-danger');
      $('#password-strength').addClass('progress-bar-warning');
      $('#result').addClass('text-warning').text('Week')
      $('#password-strength').css('width', '60%');
      return 'Week'
    } else if (strength == 4) {
      $('#result').removeClass()
      $('#result').addClass('strong');
      $('#password-strength').removeClass('progress-bar-warning');
      $('#password-strength').addClass('progress-bar-success');
      $('#result').addClass('text-success').text('Strength');
      $('#password-strength').css('width', '100%');

      return 'Strong'
    }

  }

});