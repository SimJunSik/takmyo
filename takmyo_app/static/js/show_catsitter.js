const open_menu = () =>{
    $(".menu").animate({
        'right' : '0%'
    });
}

const close_menu = () =>{
    $(".menu").animate({
        'right' : '-100%'
    });
}

const click_tab = (tab) =>{
    const category = tab.id.split('_')[1];
    console.log(category);

    $(".content-info-tab-itemWrapper").css({
        'color' : 'gray'
    });

    $(tab).css({
        'color' : 'black'
    });

    
    $(".content-info-bodyWrapper").css({
        'display' : 'none'
    });

    $("#body_" + category).css({
        'display' : 'block'
    });
}

const toggle_writing_review = () => {
    const is_open = $(".content-info-review-write_form").data("isOpen");
    console.log(is_open);

    if(!is_open) {
        $(".content-info-review-write_form").css({
            'display' : 'block'
        });
        $(".content-info-review-write_form").data("isOpen", true);
        $(".content-info-review_writeButton").hide();
    }
    else {
        $(".content-info-review-write_form").css({
            'display' : 'none'
        });
        $(".content-info-review-write_form").data("isOpen", false);
        $(".content-info-review_writeButton").show();
    }
}

$(function () {
 
    $("#rateYo_time, #rateYo_kindness, #rateYo_achievement").rateYo({
      normalFill: "#A0A0A0"
    });
   
});

const register_review = () => {
    const time_rate = $("#rateYo_time").rateYo("option", "rating");
    const kindness_rate = $("#rateYo_kindness").rateYo("option", "rating");
    const achievement_rate = $("#rateYo_achievement").rateYo("option", "rating");

    console.log(time_rate, kindness_rate, achievement_rate);
}

function wrapWindowByMask(){
    //화면의 높이와 너비를 구한다.
    var maskHeight = $(document).height();  
    var maskWidth = $(window).width();  
    
    //마스크의 높이와 너비를 화면 것으로 만들어 전체 화면을 채운다.
    $('#mask').css({
        'width':maskWidth,
        'height':maskHeight
    });  
    
    //애니메이션 효과
    $('#mask').fadeIn(200);      
    //$('#mask').fadeTo("fast",0.2);    
}

$(document).ready(function(){
    //검은 막 띄우기
    $('.content-info-review_writeButton').click(function(e){
        e.preventDefault();
        wrapWindowByMask();
        $(".register_review_Wrapper").fadeIn(200);
    });

    //닫기 버튼을 눌렀을 때
    $(".content-info-review-write-closeImage").click(function(e){
        e.preventDefault();  
        $('#mask, .register_review_Wrapper').hide(); 
    })

    //검은 막을 눌렀을 때
    $('#mask').click(function () {  
        $(this).hide();  
        $(".register_review_Wrapper").hide();
    });      
});