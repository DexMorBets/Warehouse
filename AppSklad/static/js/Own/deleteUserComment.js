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
            pk = $(this).closest('.row').find('span.hide_panel').text()
            $.ajax({
                    type: 'POST',
                    url: pk + '/comment/delete/',
                    data: {
                        pk: pk,
                        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
                    },
                    success: function() {
                    },
                });
        })
    });
});