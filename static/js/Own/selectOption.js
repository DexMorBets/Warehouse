$(document).ready(function () {
    category = $('.category_title').text();
    $('option').filter(function() {
        return category === $(this).text();
    }).attr("selected", "selected");
})
