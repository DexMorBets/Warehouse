$(document).ready( function() {
    zz = 1600;
    $( 'select' ).each( function () {
        $(this).dropdown({
            setzindex : zz,
            gutter: 0,
        });
            zz = zz - 100;
    });
});