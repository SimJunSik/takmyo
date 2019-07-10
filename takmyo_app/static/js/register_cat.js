const open_menu = () =>{
    $(".menu").stop().animate({
        'right' : '0%'
    });
}

const close_menu = () =>{
    $(".menu").stop().animate({
        'right' : '-100%'
    });
}

function readURL(input) {
    if(input.files && input.files[0]){
        var reader= new FileReader();

        reader.onload= function(e){
            // console.log(input.id);
            const idx = input.id.split("_")[1];
            $("#cat_profile_" + idx).attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}

$(".content-form-item-imageInput").change(function(){
    readURL(this);
});

$(document).ready(function(){
    $("#prev_button").hide();
    $("#next_button").hide();

    // $("#cat_name_1").attr("required", true);
    // $("#cat_age_1").attr("required", true);
});

const prev = () => {
    let current_index = $(".content-formWrapper").data('currentIndex');
    current_index = parseFloat(current_index);
    current_index -= 1;
    console.log(current_index);
    $(".content-formWrapper").data('currentIndex', current_index);
    if(current_index == 1){
        $("#prev_button").hide();
    }
    else{
        $("#prev_button").show();
    }

    const left_value = 89 * (current_index-1);
    console.log(left_value);

    $(".content-form-itemListWrapper").stop().animate({
        'left' : "-" + String(left_value) + 'vw'
    },100);

    $("#next_button").show();
}

const next = () => {
    let current_index = $(".content-formWrapper").data('currentIndex');
    let total_index = $(".content-formWrapper").data("totalIndex");
    current_index += 1;
    console.log(current_index);
    $(".content-formWrapper").data('currentIndex', current_index);
    if(current_index >= total_index){
        $("#next_button").hide();
    }

    const left_value = 89 * (current_index-1);
    console.log(left_value);

    $(".content-form-itemListWrapper").stop().animate({
        'left' : '-' + String(left_value) + 'vw'
    },100);

    $("#prev_button").show();
}

const add = () => {
    let current_index = $(".content-formWrapper").data('currentIndex');
    let total_index = $(".content-formWrapper").data("totalIndex");
    total_index += 1;

    if(total_index == 5){
        $("#add_button").hide();
    }
    if(current_index < total_index){
        $("#next_button").show();
    }
    $(".content-formWrapper").data("totalIndex", total_index);
    total_index = $(".content-formWrapper").data("totalIndex");
    console.log(total_index);

    // $("#cat_name_" + total_index).attr("required", true);
    // $("#cat_age_" + total_index).attr("required", true);
}

const check_submit = () => {
    const names = $("input[name=cat_name]");
    const ages = $("input[name=cat_age]");
    let current_index = $(".content-formWrapper").data('currentIndex');
    let total_index = $(".content-formWrapper").data("totalIndex");
    console.log("TOTAL",total_index);

    for(var i=0;i<total_index;i++){
        const name_text = $(names[i]).val();
        const age_text = $(ages[i]).val();
        console.log(name_text, age_text);

        const idx_value = 89 * i;
        if(name_text == '' || age_text == ''){
            console.log(i, idx_value);
        
            $(".content-form-itemListWrapper").stop().animate({
                'left' : '-' + String(idx_value) + 'vw'
            },100);

            let current_index = $(".content-formWrapper").data('currentIndex');
            
            if(i+1 < current_index){
                current_index = current_index - (i);
            }
            else if(i+1 > current_index){
                current_index = current_index + (i);
            }

            console.log("current", current_index);

            $(".content-formWrapper").data('currentIndex', current_index);

            if(i == 0){
                $("#prev_button").hide();
                if(total_index >= 2){
                    $("#next_button").show();
                }
            }

            if(i+1 == total_index){
                $("#next_button").hide();
                $("#prev_button").show();
            }

            setTimeout(function(){
                if(name_text == ''){
                    $(names[i]).focus();
                }
                else if(age_text == ''){
                    $(ages[i]).focus();
                }
            },200);

            return false;
        }
    }

    alert("등록이 완료되었습니다.");

    return true;
}