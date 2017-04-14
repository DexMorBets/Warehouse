$(document).ready(function() {
    $("tr").click(function () {
        $(this).find($("a"))[0].click();
    });
});
