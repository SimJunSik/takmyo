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
    current_index -= 1;
    console.log(current_index);
    $(".content-formWrapper").data('currentIndex', current_index);
    if(current_index == '1'){
        $("#prev_button").hide();
    }
    else{
        $("#prev_button").show();
    }

    $(".content-form-itemListWrapper").animate({
        'left' : '+=40.6vh'
    });

    $("#next_button").show();
}

const next = () => {
    let current_index = $(".content-formWrapper").data('currentIndex');
    let total_index = $(".content-formWrapper").data("totalIndex");
    current_index += 1;
    $(".content-formWrapper").data('currentIndex', current_index);
    if(current_index >= total_index){
        $("#next_button").hide();
    }

    $(".content-form-itemListWrapper").animate({
        'left' : '-=40.6vh'
    });

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
    let total_index = $(".content-formWrapper").data("totalIndex");
    // console.log(names);

    for(var i=0;i<total_index;i++){
        const name_text = $(names[i]).val();
        const age_text = $(ages[i]).val();
        console.log(name_text, age_text);

        const idx_value = 40.6 * i;
        if(name_text == '' || age_text == ''){
            console.log(i, idx_value);
            $(names[i]).focus();
            $(".content-form-itemListWrapper").animate({
                'left' : '-' + String(idx_value) + 'vh'
            });

            return false;
        }
    }

    alert("등록이 완료되었습니다.");

    return true;
}