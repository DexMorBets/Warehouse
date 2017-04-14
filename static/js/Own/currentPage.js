$(document).ready(function () {
    var page = $('#page').text();
    if (page == "1") {
        $(".details_li").css('border-bottom','5px solid #ffa500')
    } else if (page == "2"){
        $(".goods_li").css('border-bottom','5px solid #ffa500')
    } else if (page == "3"){
        $(".plan_li").css('border-bottom','5px solid #ffa500')
    } else if (page == "4"){
        $(".header_avatar_img").css({'border':'3px solid #ffa500','width':'46px','height':'46px','margin-top':'11px'})
    };
});
