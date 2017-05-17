$(document).ready(function () {
    $('.span-comment-delete').click(function () {
        $(this).parent().find($('.comment_delete')).animate({width:'toggle'},350);
        $(this).parent().find($('.comment_delete')).mouseenter(function () {
            $(this).parent().find($('.category_delete_text')).html('<i class="fa fa-trash-o" aria-hidden="true"></i>');
        }).mouseleave(function () {
            $(this).parent().find($('.category_delete_text')).html('Удалить')
        });
        $(this).parent().find($('.comment_delete')).click(function () {
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