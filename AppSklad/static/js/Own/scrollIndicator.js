$(document).ready(function(){
    $(window).scroll(function() {
        var wintop = parseInt($(window).scrollTop()), docheight = parseInt($(document).height()),
            winheight = parseInt($(window).height());
        var parentHeight = docheight - winheight;
        var totalScroll = wintop/parentHeight*100;
    $(".KW_progressBar").css("width",totalScroll+"%");
    });
});
