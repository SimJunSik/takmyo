from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

# Create your views here.
def index(request) :

    return render(request, 'takmyo_app/index.html')

def join(request) :
    
    if request.method == 'GET' :

        return render(request, 'takmyo_app/join.html')

    if request.method == 'POST' :

        user_id = request.POST['user_id']
        user_pw = request.POST['user_pw']
        user_gender = request.POST['user_gender']
        user_address = request.POST['user_address']
        user_detail_address = request.POST['user_detail_address']
        user_extra_address = request.POST.get('user_extra_address','')
        user_phone = request.POST['user_phone']
        if request.POST.get('user_check_phone','unchecked') == 'checked' :
            user_check_phone = True
        else :
            user_check_phone = False

        print(user_id,
                user_pw,
                user_gender,
                user_address,
                user_detail_address,
                user_extra_address,
                user_phone,
                user_check_phone)

        User = get_user_model()
        new_user = User.objects.create_user(
            username = user_id,
            password = user_pw,
            address = user_address,
            detail_address = user_detail_address,
            extra_address = user_extra_address,
            phone = user_phone,
            check_phone = user_check_phone
        )

        print(new_user)

        return redirect('/login/')

def my_login(request) :

    return render(request, 'takmyo_app/login.html')

def check_id_duplicate(request, user_id) :

    User = get_user_model()

    try :
        user = User.objects.get(username = user_id)

        result = { "result" : "failed" }

    except :

        result = { "result" : "success"}

    print(result)

    return JsonResponse(result)  