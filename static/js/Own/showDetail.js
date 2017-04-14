$(document).ready(function () {
    $('.item_input_count:not([value])').parent().addClass('hide_panel1 new_panel').find('input[type="checkbox"]').addClass('hide_panel1');
    $('div.new_panel').find('label.trash').addClass('hide_panel1');
    $(document).on('click', 'a.bt1', function () {
        $('div.hide_panel1:first').removeClass('hide_panel1').find('.detail_input_delete').addClass('show');
    });
    $(document).on('click', '.detail_input_delete', function () {
        $(this).parent().addClass('hide_panel1');
    });
})
