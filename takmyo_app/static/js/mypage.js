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

const login = () =>{
    const user_id = $("#idInput").val();
    const user_pw = $("#pwInput").val();

    const formdata = new FormData();
    formdata.append('user_id', user_id);
    formdata.append('user_pw', user_pw);

    fetch('/login/',{
        method : 'POST',
        body : formdata,
    })
    .then(e => e.json())
    .then(e => {
        console.log(e);
        if(e.result == 'success'){
            window.location.href = '/modify_myinfo/';
        }
        else if(e.result == 'failed'){
            alert("아이디 혹은 비밀번호를 확인해주세요.");
        }
    })
}