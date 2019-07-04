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
    let review_comment = $("#review_comment_input").val();
    const state = $(".content-info-review-write_form").data('state');

    if(review_comment == ''){
        review_comment = ' ';
    }
    console.log(time_rate, kindness_rate, achievement_rate, review_comment, state);

    if(state == 'register'){
        fetch('./register_review/' + time_rate + '/' + 
                                kindness_rate + '/' + 
                                achievement_rate + '/' + 
                                review_comment + '/')
        .then(e => e.json())
        .then(e => {
            console.log(e);
            if(e.result == 'success'){
                alert("리뷰 등록이 완료되었습니다.");
                location.reload(true);
            }
            else if(e.result == 'create review failed'){
                alert("리뷰 등록에 실패했습니다.");
            }
            else if(e.result == 'anonymous_user'){
                alert("로그인 해주세요.");
            }
            else if(e.result == 'already registered'){
                alert("이미 리뷰를 등록하셨습니다.");
            }
            else if(e.result == 'not recognized'){
                alert("신청서가 수락되어야 리뷰를 등록할 수 있습니다.");
            }
            else if(e.result == 'not applied'){
                alert("탁묘를 신청한 켓티만 리뷰를 등록할 수 있습니다.");
            }
        });
    }
    else if(state == 'modify'){
        const review_id = $('.content-info-review-write_form').data('reviewId');

        fetch('./modify_review/' + review_id + '/' +
                                time_rate + '/' + 
                                kindness_rate + '/' + 
                                achievement_rate + '/' + 
                                review_comment + '/')
        .then(e => e.json())
        .then(e => {
            console.log(e);
            if(e.result == 'modify review success'){
                alert("리뷰 수정이 완료되었습니다.");
                location.reload(true);
            }
            else if(e.result == 'modify review failed'){
                alert("리뷰 수정에 실패했습니다.");
            }
        });
    }
}

const open_delete_review = (review_id) => {
    console.log(review_id);

    wrapWindowByMask();
    $(".delete_review_Wrapper").fadeIn(200);

    $(".delete_review_Wrapper").data('reviewId', review_id);
}

const delete_review = () => {
    const review_id = $(".delete_review_Wrapper").data('reviewId');
    
    console.log(review_id);

    fetch('./delete_review/' + review_id + '/')
    .then(e => e.json())
    .then(e => {
        console.log(e.result);
        if(e.result == "delete review success"){
            alert("리뷰 삭제가 완료되었습니다.");
            location.reload(true);
        }
        else if(e.result == "delete review failed"){
            alert("리뷰 삭제를 실패했습니다.");
        }
    });
}

const open_modify_review = (div) => {
    const review_id = $(div).data('reviewId');
    const content = $(div).data('content');
    const time_rate = $(div).data('time_rate');
    const kindness_rate = $(div).data('kindness_rate');
    const achievement_rate = $(div).data('achievement_rate');

    $(".content-info-review-write_form").data('state', 'modify');
    $(".content-info-review-write_form").data('reviewId', review_id);
    $("#rateYo_time").rateYo('rating', time_rate);
    $("#rateYo_kindness").rateYo('rating', kindness_rate);
    $("#rateYo_achievement").rateYo('rating', achievement_rate);
    $("#review_comment_input").val(content);

    wrapWindowByMask();
    $(".register_review_Wrapper").fadeIn(200);
    
    console.log(review_id, content, time_rate, kindness_rate, achievement_rate);
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

        $(".content-info-review-write_form").data('state', 'register');
        $("#rateYo_time").rateYo('rating', 0);
        $("#rateYo_kindness").rateYo('rating', 0);
        $("#rateYo_achievement").rateYo('rating', 0);
        $("#review_comment_input").val('');

        wrapWindowByMask();
        $(".register_review_Wrapper").fadeIn(200);
    });

    //닫기 버튼을 눌렀을 때
    $(".content-info-review-write-closeImage").click(function(e){
        e.preventDefault();  
        $('#mask, .register_review_Wrapper').hide(); 
    });
    $("#delete_review_cancel_button").click(function(e){
        e.preventDefault();
        $("#mask, .delete_review_Wrapper").hide();
    });

    //검은 막을 눌렀을 때
    $('#mask').click(function () {  
        $(this).hide();  
        $(".register_review_Wrapper").hide();
        $(".delete_review_Wrapper").hide();
    });      
});