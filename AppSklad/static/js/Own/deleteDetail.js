$(document).ready(function () {
    $(document).on('click', '.trash', function () {
        $(this).parent().children().toggleClass('hidden_detail');
        $(this).removeClass('hidden_detail').toggleClass('trash_color');
    });
})

