$(document).ready(function () {
    $('.comment').hover(function () {
        $(this).find($('.comment_send')).animate({width:'toggle'},350);
        $(this).find($('.category_delete')).mouseenter(function () {
            $(this).find($('.category_delete_text')).html("<span class='glyphicon glyphicon-trash'></span>");
        }).mouseleave(function () {
            $(this).find($('.category_delete_text')).html('Удалить ?')
        });
        $(this).find($('.category_delete')).click(function () {
            $(this).closest('.row').fadeOut('slow');

            $.ajax({
                    type: 'POST',
                    url: 'category/delete/',
                    data: {
                        title: $(this).closest('.row').find($('p.items_title')).text(),
                        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
                    },
                    success: function() {
                    },
                });
        })
    });
});
