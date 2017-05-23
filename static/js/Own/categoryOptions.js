$(document).ready(function () {
    $(document).on('tap', 'i.fa-sliders', function () {
        $(this).parent().parent().find($('.category_delete')).add($(this).parent().parent().find($('.category_add'))).animate({width:'toggle'},350);

        $(this).parent().parent().find($('.category_delete')).mouseenter(function () {
            $(this).parent().parent().find($('.category_delete_text')).html('<i class="fa fa-trash-o" aria-hidden="true"></i>');
        }).mouseleave(function () {
            $(this).parent().parent().find($('.category_delete_text')).html('Удалить')
        });

        $(this).parent().parent().find($('.category_delete')).click(function () {
            $(this).closest('.row').fadeOut('slow');
            $.ajax({
                    type: 'POST',
                    url: 'category/delete/',
                    dataType: "json",
                    data: {
                        title: $(this).parent().find('p.items_title').text(),
                        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
                    },
                    success: function(resp) {
                        alert("resp: "+resp);
                    }
                });
        });

        $(this).parent().parent().find($('.category_add')).mouseenter(function () {
            $(this).parent().parent().find($('.category_add_text')).html('<i class="fa fa-plus" aria-hidden="true"></i>');
        }).mouseleave(function () {
            $(this).parent().parent().find($('.category_add_text')).html('Добавить')
        });
        $(this).parent().parent().find($('.category_add')).click(function () {
            category = $(this).parent().find('.items_title').text();
            loc = category + '/newitem/';

            location.href = loc;
        });
    });
});
