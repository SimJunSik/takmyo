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

var is_animating = false;

$(document).ready(function() {
    var start_position = 0;
    var move_position = 0;

    $(document).bind('touchstart', function(e) {

        // console.log("터치가 시작되었어요.");

        var event = e.originalEvent;

        // console.log(event.touches[0].screenX,event.touches[0].screenY);

        start_position = event.touches[0].screenY;

        // e.preventDefault();
    });

    $(document).bind('touchmove', function(e) {

        var event = e.originalEvent;

        // console.log('touch 이벤트 중입니다.'); 

        //console.log(event.touches[0].screenX,event.touches[0].screenY);

        move_position = event.touches[0].screenY;

        if((move_position - start_position) > 0){
            if(is_animating == false){
                is_animating = true;
                // console.log('down');
                // $('html, body')
                // .stop()
                // .animate({
                //     scrollTop: 0
                // }, 500);

                $(".content")
                .stop()
                .animate({
                    'top' : "0%"
                },500);

                $("#div-index-circle2").css({
                    'background-color' : 'gray',
                    'opacity' : '0.5'
                });
                $("#div-index-circle1").css({
                    'background-color' : 'black',
                    'opacity' : '1'
                });

                setTimeout(function(){
                    is_animating = false;
                },600);
            }
        }
        else {
            if(is_animating == false){
                is_animating = true;
                // console.log('up');
                // $('html, body')
                // .stop()
                // .animate({
                //     scrollTop: $(".content2").offset().top
                // }, 500);

                $(".content")
                .stop()
                .animate({
                    'top' : "-100%"
                },500);

                $("#div-index-circle1").css({
                    'background-color' : 'gray',
                    'opacity' : '0.5'
                });
                $("#div-index-circle2").css({
                    'background-color' : 'black',
                    'opacity' : '1'
                });

                setTimeout(function(){
                    is_animating = false;
                },600);
            }
        }

        // event.preventDefault();

    });

    $(document).bind('touchend', function(e) {

        // console.log("터치이벤트가 종료되었어"); 

        // e.preventDefault();

    });

});



// var f = 0;
// $(window).scroll(function() {
//     var scroll = $(window).scrollTop();
//     console.log("!!!");

//     if(scroll > position && f == 0) {
//         console.log('scrollDown');
//         f = 1;
//         $('html, body')
//         .animate({
//             scrollTop: $(".content2").offset().top
//         }, 500);
//         $("#div-index-circle1").css({
//             'background-color' : 'gray',
//             'opacity' : '0.5'
//         });
//         $("#div-index-circle2").css({
//             'background-color' : 'black',
//             'opacity' : '1'
//         });
//         setTimeout(function(){
//             f = 0;
//         },1000);
//     } 
//     else if(scroll <= position && f == 0) {
//         console.log('scrollUp');
//         f = 1;
//         $('html, body')
//         .animate({
//             scrollTop: 0
//         }, 500);
//         $("#div-index-circle2").css({
//             'background-color' : 'gray',
//             'opacity' : '0.5'
//         });
//         $("#div-index-circle1").css({
//             'background-color' : 'black',
//             'opacity' : '1'
//         });
//         setTimeout(function(){
//             f = 0;
//         },1000);
//     }
//     position = scroll;
// });

