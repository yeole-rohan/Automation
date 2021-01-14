var $ = jQuery.noConflict();

$(document).ready(function(){
    $("#id_UTR_no").attr('placeholder', 'Enter 16 Digit UTR Number');
    $(".razorpay-payment-button").attr('name', 'razorpay');
    $(".razorpay-payment-button").attr('id', 'razorpay');
    $(".razorpay-payment-button").attr('class', 'pay')
    // $("#pay_id").attr("disabled", true);
    $("#id_UTR_no").attr('type', 'number');
    // document.getElementById("pay_id").disabled = true; 
    $('#id_UTR_no').on('input', function() { 
        var a = $(this).val() // get the current value of the input field.
        console.log(a.length);
        if(a.length >= 16){
            $("#pay_id").attr("disabled", false);
        }
    });
    $('.sel-rtgs').on('click', function(){
        $('.pay-type').css('display', 'none');
        $('.utr').css('display', 'block');
    })
}( jQuery ) );