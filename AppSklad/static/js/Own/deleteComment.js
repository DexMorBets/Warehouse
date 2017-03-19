$(document).ready(function () {
    $('.comment_published').hover(function () {
        $(this).find($('.comment_delete')).animate({width:'toggle'},350);
        $(this).find($('.comment_delete')).mouseenter(function () {
            $(this).find($('.category_delete_text')).html("<span class='glyphicon glyphicon-trash'></span>");
        }).mouseleave(function () {
            $(this).find($('.category_delete_text')).html('Удалить')
        });
        $(this).find($('.comment_delete')).click(function () {
            $(this).closest('.row').fadeOut('slow');
            $.ajax({
                    type: 'POST',
                    url: 'comment/delete/',
                    data: {
                        pk: $(this).closest('.row').find('span.hide_panel').text(),
                        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
                    },
                    success: function() {
                    },
                });
        })
    });
});
