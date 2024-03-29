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

const check_id_duplicate = () =>{
    const user_id = $("#idInput").val();

    if(user_id == ''){
        alert("아이디를 입력해주세요.");
        return false;
    }

    fetch('./check_id_duplicate/' + user_id + '/')
    .then(e => e.json())
    .then(e => {
        if(e.result == 'success'){
            console.log("success");
            $("#idInput").data(
                'checkIdDuplicate' , 'success'
            );

            if(check_id_is_valid()){
                $(".content-form-idResult-duplicate_text")
                .css({
                    'color' : 'green'
                })
                .html("사용가능한 아이디입니다.");
            }
            else{
                $(".content-form-idResult-duplicate_text")
                .css({
                    'color' : 'green'
                })
                .html("");
            }
        }
        else if(e.result == 'failed'){
            console.log("failed");
            $("#idInput").data(
                'checkIdDuplicate' , 'failed'
            );

            $(".content-form-idResult-duplicate_text")
            .css({
                'color' : 'red'
            })
            .html("중복된 아이디입니다.");
        }
    });
}


const check_id_is_valid = () =>{
    const user_id = $("#idInput").val();

    const idReg = /^[a-z]+[a-z0-9]{5,}$/g;
    if( !idReg.test(user_id)) {
        return false;
    }
    else {
        return true;
    }
}

$("#idInput").change(function(){
    console.log("!!!!");
    if(check_id_is_valid()){
        console.log("id_valid","success");
        $("#idInput").data(
            'checkIdIsValid' , 'success'
        );

        $(".content-form-idResult-valid_text")
        .css({
            'color' : 'green'
        })
        .html("");
    }
    else{
        console.log("id_valid","failed");
        $("#idInput").data(
            'checkIdIsValid' , 'failed'
        );

        $(".content-form-idResult-valid_text")
        .css({
            'color' : 'red'
        })
        .html("영소문자 + (숫자) 6글자 이상 입력");
    }
});


const check_password_is_same = () => {
    const user_pw = $("#pwInput").val();
    const user_repw = $("#repwInput").val();

    if(user_pw == user_repw){
        return true;
    }
    else if(user_pw != user_repw){
        return false;
    }
}

const check_password_is_valid = () => {
    const user_pw = $("#pwInput").val();
    const user_repw = $("#repwInput").val();

    if(!(/^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$/.test(user_pw))){
        return false;
    }
    else {
        return true;
    }
}

const check_submit_is_valid = () => {
    const id_duplicate = $("#idInput").data('checkIdDuplicate');
    const id_valid = $("#idInput").data('checkIdIsValid');
    const pw_valid = $("#pwInput").data('checkPwValid');

    console.log(id_duplicate, id_valid, pw_valid);

    if(id_duplicate == 'success' && id_valid == 'success' && pw_valid == 'success'){
        return true;
    }
    else {
        alert("ID 혹은 비밀번호를 확인해주세요.");
        return false;
    }
}

$("#pwInput, #repwInput").change(function(){
    // console.log(check_password_is_same(), check_password_is_valid());
    console.log("!!!!");
    if(check_password_is_same() && check_password_is_valid()){
        $("#pwInput").data(
            'checkPwValid' , 'success'
        );

        $(".content-form-pwResultWrapper")
            .css({
                'color' : 'green'
            })
            .html("PASS");
    }
    else {
        $("#pwInput").data(
            'checkPwValid' , 'failed'
        );

        $(".content-form-pwResultWrapper")
            .css({
                'color' : 'red'
            })
            .html("NON-PASS");
    }
});

// 주소 api
// 우편번호 찾기 찾기 화면을 넣을 element

function foldDaumPostcode() {
    var element_wrap = document.getElementById('wrap');
    // iframe을 넣은 element를 안보이게 한다.
    element_wrap.style.display = 'none';
}

function sample3_execDaumPostcode() {
    var element_wrap = document.getElementById('wrap');
    // 현재 scroll 위치를 저장해놓는다.
    var currentScroll = Math.max(document.body.scrollTop, document.documentElement.scrollTop);
    new daum.Postcode({
        oncomplete: function(data) {
            // 검색결과 항목을 클릭했을때 실행할 코드를 작성하는 부분.

            // 각 주소의 노출 규칙에 따라 주소를 조합한다.
            // 내려오는 변수가 값이 없는 경우엔 공백('')값을 가지므로, 이를 참고하여 분기 한다.
            var addr = ''; // 주소 변수
            var extraAddr = ''; // 참고항목 변수

            //사용자가 선택한 주소 타입에 따라 해당 주소 값을 가져온다.
            if (data.userSelectedType === 'R') { // 사용자가 도로명 주소를 선택했을 경우
                addr = data.roadAddress;
            } else { // 사용자가 지번 주소를 선택했을 경우(J)
                addr = data.jibunAddress;
            }

            // 사용자가 선택한 주소가 도로명 타입일때 참고항목을 조합한다.
            if(data.userSelectedType === 'R'){
                // 법정동명이 있을 경우 추가한다. (법정리는 제외)
                // 법정동의 경우 마지막 문자가 "동/로/가"로 끝난다.
                if(data.bname !== '' && /[동|로|가]$/g.test(data.bname)){
                    extraAddr += data.bname;
                }
                // 건물명이 있고, 공동주택일 경우 추가한다.
                if(data.buildingName !== '' && data.apartment === 'Y'){
                    extraAddr += (extraAddr !== '' ? ', ' + data.buildingName : data.buildingName);
                }
                // 표시할 참고항목이 있을 경우, 괄호까지 추가한 최종 문자열을 만든다.
                if(extraAddr !== ''){
                    extraAddr = ' (' + extraAddr + ')';
                }
                // 조합된 참고항목을 해당 필드에 넣는다.
                document.getElementById("sample3_extraAddress").value = extraAddr;
            
            } else {
                document.getElementById("sample3_extraAddress").value = '';
            }

            // 우편번호와 주소 정보를 해당 필드에 넣는다.
            document.getElementById('sample3_postcode').value = data.zonecode;
            document.getElementById("sample3_address").value = addr;
            // 커서를 상세주소 필드로 이동한다.
            document.getElementById("sample3_detailAddress").focus();

            // iframe을 넣은 element를 안보이게 한다.
            // (autoClose:false 기능을 이용한다면, 아래 코드를 제거해야 화면에서 사라지지 않는다.)
            element_wrap.style.display = 'none';

            // 우편번호 찾기 화면이 보이기 이전으로 scroll 위치를 되돌린다.
            document.body.scrollTop = currentScroll;
        },
        // 우편번호 찾기 화면 크기가 조정되었을때 실행할 코드를 작성하는 부분. iframe을 넣은 element의 높이값을 조정한다.
        onresize : function(size) {
            element_wrap.style.width = '100%';
            element_wrap.style.height = '150vw';
        },
        width : '100%',
        height : '101%'
    }).embed(element_wrap);

    // iframe을 넣은 element를 보이게 한다.
    element_wrap.style.display = 'block';
}