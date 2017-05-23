$(document).ready(function () {
    $('.span-comment-delete').click(function () {
        $(this).parent().find($('.comment_delete')).animate({width:'toggle'},350);
        $(this).parent().find($('.comment_delete')).mouseenter(function () {
            $(this).find($('.category_delete_text')).html('<i class="fa fa-trash-o" aria-hidden="true"></i>');
        }).mouseleave(function () {
            $(this).find($('.category_delete_text')).html('Удалить')
        });
        $(this).parent().find($('.comment_delete')).click(function () {
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
