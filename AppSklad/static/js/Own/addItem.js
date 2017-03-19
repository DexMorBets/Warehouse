$(document).ready(function () {
    $('.main').hover(function () {
        $(this).find($('.category_add')).animate({width:'toggle'},350);
        $(this).find($('.category_add')).mouseenter(function () {
            $(this).find($('.category_add_text')).html("<span class='glyphicon glyphicon-plus'></span>");
        }).mouseleave(function () {
            $(this).find($('.category_add_text')).html('Добавить')
        });
        $(this).find($('.category_add')).click(function () {
            category = $(this).siblings('.nov_ob2').find('.items_title').text();
            loc = category + '/newitem/';
            location.href = loc;
        })
    });
});
