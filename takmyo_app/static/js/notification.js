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

const delete_checked_notification = () =>{
    fetch('./delete/checked/')
    .then(e => e.json())
    .then(e => {
        console.log(e.result);
        if(e.result == 'success'){
            $(".checked_notification").hide();
        }
        else if(e.result == 'failed'){
            alert("읽은 알림 삭제에 실패했습니다.");
        }
    });
}

const check_notification = (noti) =>{
    const noti_id = noti.id.split("_")[1];
    console.log(noti_id);

    fetch('./check/' + noti_id + '/')
    .then(e => e.json())
    .then(e => {
        console.log(e.result);
        if(e.result == 'success'){
            $("#notification_" + noti_id).addClass('checked_notification');
        }
        else if(e.result == 'failed'){
            alert("읽음 처리에 실패했습니다.");
        }
    }) 
}

const delete_all_notification = () =>{
    fetch('./delete/all/')
    .then(e => e.json())
    .then(e => {
        console.log(e.result);
        if(e.result == 'success'){
            $(".content-notification").hide();
        }
        else if(e.result == 'failed'){
            alert("전체 알림 삭제에 실패했습니다.");
        }
    });
}