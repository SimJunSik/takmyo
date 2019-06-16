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

const select_form = () =>{
    $("#select-form").css({
        'background-color' : '#2196F3'
    });
    $("#form-list").css({
        'display' : 'block'
    });

    $("#select-review").css({
        'background-color' : 'snow'
    });
    $("#review-list").css({
        'display' : 'none'
    });
}

const select_review = () =>{
    $("#select-form").css({
        'background-color' : 'snow'
    });
    $("#form-list").css({
        'display' : 'none'
    });

    $("#select-review").css({
        'background-color' : '#2196F3'
    });
    $("#review-list").css({
        'display' : 'block'
    });
}