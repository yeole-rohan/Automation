var $ = jQuery.noConflict();

$(document).ready(function(){
    $("#goverment").attr("disabled", !this.checked);
    $("#id_choose_goverment").click(function() {
        $("#goverment").attr("disabled", !this.checked);
    });
    $("#public").attr("disabled", !this.checked);
    $("#id_choose_local").click(function() {
        $("#public").attr("disabled", !this.checked);
    });
    
 
    // $('#goverment').on('click', function(){
    //     $gov = document.getElementById('gov').value
    //     console.log($gov)
    //     console.log($('#gov').attr("href"))
    //     $.ajax({
    //         url:$('#gov').attr("href"),
    //         data:{
    //             'gov': document.getElementById('gov').value,
    //         },
    //         type:'POST',
    //         dataType: 'json',
    //         success: function (res, status) {
    //             if (res['status'] == 'ok') {
    //                 console.log(status)
    //             }
    //         },
    //         error: function (res) {
    //             console.log(res.status);
    //         }
    //     })
    // })
}( jQuery ) );