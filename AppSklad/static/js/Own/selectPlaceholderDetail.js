$(document).ready(function () {
    $("select").last().find("option:first-child").each(function () {
        $(this).html('--Цвет--');
    })
});
