// $(document).ready(function() {
//     $('.arrow_coach').click(function () {
//         $('.panel-coaches-hide').slideToggle(500);
//         $('img[alt^="ArrowCoach"]').toggleClass('rotate');
//     });
//     $('.arrow_chair').click(function () {
//         $('.panel-chairs-hide').slideToggle(500);
//         $('img[alt^= "ArrowChair"]').toggleClass('rotate');
//     });
// });

$(document).ready(function() {
    $('.arrow').click(function () {
        $(this).siblings(".hide_panel").slideToggle(500);
        $(this).find('img[alt^="Arrow"]').toggleClass('rotate');
    });
});
