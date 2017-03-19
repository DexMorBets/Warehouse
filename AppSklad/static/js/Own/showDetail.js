$(document).ready(function () {
    $('.item_input_count:not([value])').parent().addClass('hide_panel new_panel').find('input[type="checkbox"]').addClass('hide_panel');
    $('div.new_panel').find('label.trash').addClass('hide_panel');
    $(document).on('click', 'a.bt1', function () {
        $('div.hide_panel:first').removeClass('hide_panel').find('.detail_input_delete').addClass('show');
    });
    $(document).on('click', '.detail_input_delete', function () {
        $(this).parent().addClass('hide_panel');
    });
})
