var $ = jQuery.noConflict();

$(document).ready(function(){
  $("#id_first_name").attr('placeholder', 'First Name');
  $("#id_last_name").attr('placeholder', 'Last Name');
  $("#id_password1").attr('placeholder', 'Password');
  $("#id_password2").attr('placeholder', 'Confirm Password');
  $('#id_username').attr('placeholder', 'User ID');
  $('#id_password').attr('placeholder', 'Enter Password');

}( jQuery ) );