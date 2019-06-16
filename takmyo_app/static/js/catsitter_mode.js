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

const select_receive_form = () =>{
    $("#select_receive_form").css({
        'background-color' : '#2196F3'
    });
    $("#select_send_form").css({
        'background-color' : 'snow'
    });

    $("#receive_form_list").css({
        'display' : 'block'
    });
    $("#send_form_list").css({
        'display' : 'none'
    });
}

const select_send_form = () =>{
    $("#select_receive_form").css({
        'background-color' : 'snow'
    });
    $("#select_send_form").css({
        'background-color' : '#2196F3'
    });

    $("#receive_form_list").css({
        'display' : 'none'
    });
    $("#send_form_list").css({
        'display' : 'block'
    });
}