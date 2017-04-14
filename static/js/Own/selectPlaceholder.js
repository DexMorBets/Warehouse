$(document).ready(function () {
    $("select option:first-child").each(function () {
        if($(this).is(':selected')) {
            $(this).html('--Категория--');
            // $(this).parent().addClass('placeholder_select')
        }
    })
    // $('select').focus(function () {
    //     if($(this).filter("option:first-child").is(':selected')) {
    //         $(this).filter('option:first-child').html('');
    //     };
    // })
});
