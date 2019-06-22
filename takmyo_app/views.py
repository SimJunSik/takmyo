from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import *
import requests
from .serializers import *

# Create your views here.
def index(request) :

    user = request.user

    if user.is_authenticated :

        notifications_count = user.receive_notifications.filter(is_checked=False).count()

        # print(notifications_count)

        context = { 'user' : user , 'notifications_count' : notifications_count }

        return render(request, 'takmyo_app/index.html', context)

    elif user.is_anonymous :

        return render(request, 'takmyo_app/index.html')

def join(request) :
    
    if request.method == 'GET' :

        return render(request, 'takmyo_app/join.html')

    if request.method == 'POST' :

        user_id = request.POST['user_id']
        user_pw = request.POST['user_pw']
        user_gender = request.POST['user_gender']
        user_postcode = request.POST['user_postcode']
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
                user_postcode,
                user_address,
                user_detail_address,
                user_extra_address,
                user_phone,
                user_check_phone)

        User = get_user_model()
        new_user = User.objects.create_user(
            username = user_id,
            password = user_pw,
            gender = user_gender,
            postcode = user_postcode,
            address = user_address,
            detail_address = user_detail_address,
            extra_address = user_extra_address,
            phone = user_phone,
            check_phone = user_check_phone
        )

        print(user_address, user_detail_address)

        address = user_address + user_detail_address
        api_key = "AIzaSyDyFSiU__Yph4023Zgl_Ptc-WNuEQ6jTGU"
        api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
        api_response_dict = api_response.json()

        # print(api_response_dict)

        if api_response_dict['status'] == 'OK':
            latitude = api_response_dict['results'][0]['geometry']['location']['lat']
            longitude = api_response_dict['results'][0]['geometry']['location']['lng']
            print('Latitude:', latitude)
            print('Longitude:', longitude)

            new_user.lat = latitude
            new_user.lng = longitude
            new_user.save()

        print(new_user)

        return redirect('/login/')

@csrf_exempt
def my_login(request) :

    if request.method == 'GET' :

        return render(request, 'takmyo_app/login.html')

    elif request.method == 'POST' :

        user_id = request.POST['user_id']
        user_pw = request.POST['user_pw']

        user = authenticate(username = user_id, password = user_pw)

        if user is not None :
            login(request, user)
            result = { "result" : "success" }

        else :

            result = { "result" : "failed" }

        return JsonResponse(result)


def check_id_duplicate(request, user_id) :

    User = get_user_model()

    try :
        user = User.objects.get(username = user_id)

        result = { "result" : "failed" }

    except :

        result = { "result" : "success"}

    print(result)

    return JsonResponse(result)  


def notification(request) :

    user = request.user

    if user.is_authenticated :

        notifications = user.receive_notifications.all()

        context = { 'user' : user , 'notifications' : notifications }

        return render(request, 'takmyo_app/notification.html', context)

    else :

        return redirect('/login/')


def delete_checked_notification(request) :

    user = request.user

    try :
        checked_notifications = user.receive_notifications.filter(is_checked=True).delete()
        result = { 'result' : 'success' }

    except :
        result = { 'result' : 'failed' }

    return JsonResponse(result)

def delete_all_notification(request) :

    user = request.user

    try :
        notifications = user.receive_notifications.all().delete()
        result = { 'result' : 'success' }

    except :
        result = { 'result' : 'failed' }

    return JsonResponse(result)

def check_notification(request, notification_id) :

    user = request.user

    try :
        checked_notification = Notification.objects.get(id=notification_id, receiver=user)
        print(checked_notification)
        checked_notification.is_checked = True
        checked_notification.save()
        result = { 'result' : 'success' }

    except :
        result = { 'result' : 'failed' }

    return JsonResponse(result)


def catsitter_mode(request) :

    return render(request, 'takmyo_app/catsitter_mode.html')

def modify_myinfo(request) :

    user = request.user

    if user.is_authenticated :

        if request.method == 'GET' :

            context = { 'user' : user }

            return render(request, 'takmyo_app/modify_myinfo.html', context)

        elif request.method == 'POST' :

            # user_id = request.POST['user_id']
            user_new_pw = request.POST.get('user_new_pw','')
            user_gender = request.POST['user_gender']
            user_postcode = request.POST['user_postcode']
            user_address = request.POST['user_address']
            user_detail_address = request.POST['user_detail_address']
            user_extra_address = request.POST.get('user_extra_address','')
            user_phone = request.POST['user_phone']
            if request.POST.get('user_check_phone','unchecked') == 'checked' :
                user_check_phone = True
            else :
                user_check_phone = False

            User = get_user_model()

            updated_user = User.objects.get(id = user.id)
            print(updated_user, user_new_pw)
            
            if user_new_pw != '' :
                updated_user.set_password(user_new_pw)
                
            updated_user.gender = user_gender
            updated_user.postcode = user_postcode
            updated_user.address = user_address
            updated_user.detail_address = user_detail_address
            updated_user.extra_address = user_extra_address
            updated_user.phone = user_phone
            updated_user.check_phone = user_check_phone

            updated_user.save()

            login(request, updated_user)

            return redirect('/main/')
    
    else :

        return redirect('/login/')

@csrf_exempt
def check_current_pw(request) :

    user = request.user

    current_pw_input = request.POST['current_pw_input']

    valid_user = authenticate(username = user.username, password = current_pw_input)

    if valid_user is not None :
        result = { "result" : "success" }

    else :
        result = { "result" : "failed" }

    return JsonResponse(result)


def mypage(request) :

    user = request.user

    if user.is_authenticated :

        context = { 'user' : user }

        return render(request, 'takmyo_app/mypage.html', context)
    
    else :

        return redirect('/login/')

def my_logout(request) :

    logout(request)

    return redirect('/main/')


def search_catsitter(request) :

    user = request.user

    User = get_user_model()

    catsitters = User.objects.filter(is_catsitter=True)

    context = { 'user' : user , 'catsitters' : catsitters }

    return render(request, 'takmyo_app/search_catsitter.html', context)
    








from django.db.models import Q

def test(request) :

    User = get_user_model()

    users = User.objects.filter(~Q(lat=0.0,lng=0.0))

    context = { 'users' : users }

    return render(request, 'takmyo_app/test.html', context)

def get_user_list(request) :

    User = get_user_model()

    users = User.objects.filter(~Q(lat=0.0,lng=0.0))

    if users :

        serializer = UserSerializer(users, many=True)

        result = { "result" : "success" , "users" : serializer.data }
    
    else :

        result = { "result" : "failed" }

    return JsonResponse(result)


