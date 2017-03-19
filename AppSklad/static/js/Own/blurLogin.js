$(document).ready(function(){
    $('input').focus(function () {
            $(this).parent().css('border-color', '#1596a5');
            $('.body').css('filter', 'blur(5px)');
        }).blur(function () {
            $(this).parent().css('border-color', '#c3c3c3');
            $('.body').css('filter', '');
        });
});
