$(document).ready(function(){
    $('textarea').focus(function () {
            $('.body').add(".border_style").add(".hr").add(".comment_not").add(".comment_published").add(".arrows_mar").add(".arrows").css('filter', 'blur(5px)');
        }).blur(function () {
            $('.body').add(".border_style").add(".hr").add(".comment_not").add(".comment_published").add(".arrows_mar").add(".arrows").css('filter', '');
        });
});
