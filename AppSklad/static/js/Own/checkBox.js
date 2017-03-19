$(document).ready(function () {
    $(document).on('click', '.check_image', function () {
        if ($(this).attr('src') == "/static/img/check_off.png") {
            $(this).attr("src", "/static/img/check_on.png").children().toggleClass('hidden_detail');
            $('.avatar_div').fadeOut("slow");
        } else {
            $(this).attr("src", "/static/img/check_off.png").children().toggleClass('hidden_detail');
            $('.avatar_div').fadeIn("slow");
        }
    });
})

