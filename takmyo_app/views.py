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

                updated_user.lat = latitude
                updated_user.lng = longitude
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

    if request.method == 'GET' :

        if user.is_authenticated :

            request.session['select_address'] = user.address

        else :

            request.session['select_address'] = 'unknown'

        request.session['select_place'] = 'visit'
        request.session['select_havePet'] = 'unknown'
        request.session['day'] = 'both'
        request.session['time'] = 'both'
        request.session['gender'] = 'both'
        request.session['pill'] = 'both'

        catsitters = Catsitter.objects.filter(activation=True)

        context = { 'user' : user , 'catsitters' : catsitters }

        return render(request, 'takmyo_app/search_catsitter.html', context)

    elif request.method == 'POST' : 

        select_address_value = request.POST.get('user_address', 'unknown')
        select_place_value = request.POST.get('select_place','unknown')
        select_havePet_value = request.POST.get('select_havePet','unknown')
        select_day = request.POST.get('day','unknown')
        select_time = request.POST.get('time','unknown')
        select_gender = request.POST.get('gender','unknown')
        select_pill = request.POST.get('pill','unknown')

        if select_havePet_value == 'yes' :
            select_havePet_value = True
        elif select_havePet_value == 'no' :
            select_havePet_value = False
            
        if select_pill == 'possible' :
            select_pill = True

        print(select_address_value, select_place_value, select_havePet_value, select_day, select_time, select_gender, select_pill)

        if select_place_value == 'both' :
            catsitters = Catsitter.objects.filter(activation=True)
        else :
            catsitters = Catsitter.objects.filter(
                available_place = select_place_value
            ) | Catsitter.objects.filter(
                available_place = 'both'
            )

        print(catsitters)

        if select_havePet_value != 'unknown' :
            if select_havePet_value != 'both' :
                catsitters = catsitters.filter(
                    have_pet = select_havePet_value
                )

        if select_day != 'both' :
            catsitters = catsitters.filter(
                available_day = select_day
            ) | catsitters.filter(
                available_day = 'both'
            )

        if select_time != 'both' :
            if select_day == 'weekday' :
                catsitters = catsitters.filter(
                    available_weekday_time = select_time
                ) | catsitters.filter(
                    available_weekday_time = 'both'
                )
            elif select_day == 'weekend' :
                catsitters = catsitters.filter(
                    available_weekend_time = select_time
                ) | catsitters.filter(
                    available_weekday_time = 'both'
                )
            else :
                catsitters = catsitters.filter(
                    available_weekday_time = select_time
                ) | catsitters.filter(
                    available_weekend_time = select_time
                ) | catsitters.filter(
                    available_weekday_time = 'both'
                ) | catsitters.filter(
                    available_weekend_time = 'both'
                )

        if select_gender != 'both' :
            catsitters = catsitters.filter(
                user__gender = select_gender
            )

        if select_pill != 'both' :
            catsitters = catsitters.filter(
                available_pill = select_pill
            )

        # if select_place_value == 'both' :
        #     if select_havePet_value == 'unknown' :
        #         if select_day == 'both' :
        #             if select_time == 'both' :
        #                 if select_gender == 'both' :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
                                    
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_pill = select_pill
        #                         )
        #                 else :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             user__gender = select_gender
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         )
        #             else :
        #                 if select_gender == 'both' :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_weekday_time = select_time
        #                         ) | Catsitter.objects.filter(
        #                             available_weekend_time = select_time
        #                         ) | Catsitter.objects.filter(
        #                             available_weekend_time = 'both'
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_weekday_time = select_time,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             available_weekend_time = select_time,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             available_weekend_time = 'both',
        #                             available_pill = select_pill
        #                         )
        #                 else :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             user__gender = select_gender,
        #                             available_weekday_time = select_time
        #                         ) | Catsitter.objects.filter(
        #                             user__gender = select_gender,
        #                             available_weekend_time = select_time
        #                         ) | Catsitter.objects.filter(
        #                             user__gender = select_gender,
        #                             available_weekend_time = 'both'
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             user__gender = select_gender,
        #                             available_weekday_time = select_time,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             user__gender = select_gender,
        #                             available_weekend_time = select_time,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             user__gender = select_gender,
        #                             available_weekend_time = 'both',
        #                             available_pill = select_pill
        #                         )
        #         else :
        #             if select_time == 'both' :
        #                 if select_gender == 'both' :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_day = select_day
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_day = select_day,
        #                             available_pill = select_pill
        #                         )
        #                 else :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_day = select_day,
        #                             user__gender = select_gender
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_day = select_day,
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         )
        #             else :
        #                 if select_gender == 'both' :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_day = select_day,
        #                             available_weekday_time = select_time
        #                         ) | Catsitter.objects.filter(
        #                             available_day = select_day,
        #                             available_weekend_time = select_time
        #                         ) | Catsitter.objects.filter(
        #                             available_day = select_day,
        #                             available_weekend_time = 'both'
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_day = select_day,
        #                             available_weekday_time = select_time,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             available_day = select_day,
        #                             available_weekend_time = select_time,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             available_day = select_day,
        #                             available_weekend_time = 'both',
        #                             available_pill = select_pill
        #                         )
        #                 else :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_day = select_day,
        #                             available_weekday_time = select_time,
        #                             user__gender = select_gender
        #                         ) | Catsitter.objects.filter(
        #                             available_day = select_day,
        #                             available_weekend_time = select_time,
        #                             user__gender = select_gender
        #                         ) | Catsitter.objects.filter(
        #                             available_day = select_day,
        #                             available_weekend_time = 'both',
        #                             user__gender = select_gender
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_day = select_day,
        #                             available_weekday_time = select_time,
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             available_day = select_day,
        #                             available_weekend_time = select_time,
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             available_day = select_day,
        #                             available_weekend_time = 'both',
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         )
        #     else :
        #         if select_day == 'both' :
        #             if select_time == 'both' :
        #                 if select_gender == 'both' :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             have_pet = select_havePet_value
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_pill = select_pill
        #                         )
        #                 else :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             user__gender = select_gender
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         )
        #             else :
        #                 if select_gender == 'both' :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_weekday_time = select_time
        #                         ) | Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_weekend_time = select_time
        #                         ) | Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_weekend_time = 'both'
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_weekday_time = select_time,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_weekend_time = select_time,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_weekend_time = 'both',
        #                             available_pill = select_pill
        #                         )
        #                 else :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_weekday_time = select_time,
        #                             user__gender = select_gender
        #                         ) | Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_weekend_time = select_time,
        #                             user__gender = select_gender
        #                         ) | Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_weekend_time = 'both',
        #                             user__gender = select_gender
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_weekday_time = select_time,
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_weekend_time = select_time,
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_weekend_time = 'both',
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         )
        #         else :
        #             if select_time == 'both' :
        #                 if select_gender == 'both' :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_day = select_day
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_day = select_day,
        #                             available_pill = select_pill
        #                         )
        #                 else :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_day = select_day,
        #                             user__gender = select_gender
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_day = select_day,
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         )
        #             else :
        #                 if select_gender == 'both' :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_day = select_day,
        #                             available_weekday_time = select_time
        #                         ) | Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_day = select_day,
        #                             available_weekend_time = select_time
        #                         ) | Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_day = select_day,
        #                             available_weekend_time = 'both'
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_day = select_day,
        #                             available_weekday_time = select_time,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_day = select_day,
        #                             available_weekend_time = select_time,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_day = select_day,
        #                             available_weekend_time = 'both',
        #                             available_pill = select_pill
        #                         )
        #                 else :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_day = select_day,
        #                             available_weekday_time = select_time,
        #                             user__gender = select_gender
        #                         ) | Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_day = select_day,
        #                             available_weekend_time = select_time,
        #                             user__gender = select_gender
        #                         ) | Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_day = select_day,
        #                             available_weekend_time = 'both',
        #                             user__gender = select_gender
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_day = select_day,
        #                             available_weekday_time = select_time,
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_day = select_day,
        #                             available_weekend_time = select_time,
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             have_pet = select_havePet_value,
        #                             available_day = select_day,
        #                             available_weekend_time = 'both',
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         )
        # else :
        #     if select_havePet_value == 'unknown' :
        #         if select_day == 'both' :
        #             if select_time == 'both' :
        #                 if select_gender == 'both' :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_pill = select_pill
        #                         )
        #                 else :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             user__gender = select_gender
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         )
        #             else :
        #                 if select_gender == 'both' :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_weekday_time = select_time
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_weekend_time = select_time
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_weekend_time = 'both'
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_weekday_time = select_time,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_weekend_time = select_time,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_weekend_time = 'both',
        #                             available_pill = select_pill
        #                         )
        #                 else :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_weekday_time = select_time,
        #                             user__gender = select_gender
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_weekend_time = select_time,
        #                             user__gender = select_gender
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_weekend_time = 'both',
        #                             user__gender = select_gender
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_weekday_time = select_time,
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_weekend_time = select_time,
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_weekend_time = 'both',
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         )
        #         else :
        #             if select_time == 'both' :
        #                 if select_gender == 'both' :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             available_pill = select_pill
        #                         )
        #                 else :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             user__gender = select_gender
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         )
        #             else :
        #                 if select_gender == 'both' :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             available_weekday_time = select_time
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             available_weekend_time = select_time
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             available_weekend_time = 'both'
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             available_weekday_time = select_time,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             available_weekend_time = select_time,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             available_weekend_time = 'both',
        #                             available_pill = select_pill
        #                         )
        #                 else :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             available_weekday_time = select_time,
        #                             user__gender = select_gender
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             available_weekend_time = select_time,
        #                             user__gender = select_gender
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             available_weekend_time = 'both',
        #                             user__gender = select_gender
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             available_weekday_time = select_time,
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             available_weekend_time = select_time,
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             available_weekend_time = 'both',
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         )
        #     else :
        #         if select_day == 'both' :
        #             if select_time == 'both' :
        #                 if select_gender == 'both' :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             have_pet = select_havePet_value
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             have_pet = select_havePet_value,
        #                             available_pill = select_pill
        #                         )
        #                 else :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             have_pet = select_havePet_value,
        #                             user__gender = select_gender
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             have_pet = select_havePet_value,
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         )
        #             else :
        #                 if select_gender == 'both' :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             have_pet = select_havePet_value,
        #                             available_weekday_time = select_time
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             have_pet = select_havePet_value,
        #                             available_weekend_time = select_time
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             have_pet = select_havePet_value,
        #                             available_weekend_time = 'both'
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             have_pet = select_havePet_value,
        #                             available_weekday_time = select_time,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             have_pet = select_havePet_value,
        #                             available_weekend_time = select_time,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             have_pet = select_havePet_value,
        #                             available_weekend_time = 'both',
        #                             available_pill = select_pill
        #                         )
        #                 else :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             have_pet = select_havePet_value,
        #                             available_weekday_time = select_time,
        #                             user__gender = select_gender
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             have_pet = select_havePet_value,
        #                             available_weekend_time = select_time,
        #                             user__gender = select_gender
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             have_pet = select_havePet_value,
        #                             available_weekend_time = 'both',
        #                             user__gender = select_gender
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             have_pet = select_havePet_value,
        #                             available_weekday_time = select_time,
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             have_pet = select_havePet_value,
        #                             available_weekend_time = select_time,
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             have_pet = select_havePet_value,
        #                             available_weekend_time = 'both',
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         )
        #         else :
        #             if select_time == 'both' :
        #                 if select_gender == 'both' :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             have_pet = select_havePet_value
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             have_pet = select_havePet_value,
        #                             available_pill = select_pill
        #                         )
        #                 else :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             have_pet = select_havePet_value,
        #                             user__gender = select_gender
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             have_pet = select_havePet_value,
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         )
        #             else :
        #                 if select_gender == 'both' :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             have_pet = select_havePet_value,
        #                             available_weekday_time = select_time
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             have_pet = select_havePet_value,
        #                             available_weekend_time = select_time
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             have_pet = select_havePet_value,
        #                             available_weekend_time = 'both'
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             have_pet = select_havePet_value,
        #                             available_weekday_time = select_time,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             have_pet = select_havePet_value,
        #                             available_weekend_time = select_time,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             have_pet = select_havePet_value,
        #                             available_weekend_time = 'both',
        #                             available_pill = select_pill
        #                         )
        #                 else :
        #                     if select_pill == 'both' :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             have_pet = select_havePet_value,
        #                             available_weekday_time = select_time,
        #                             user__gender = select_gender
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             have_pet = select_havePet_value,
        #                             available_weekend_time = select_time,
        #                             user__gender = select_gender
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             have_pet = select_havePet_value,
        #                             available_weekend_time = 'both',
        #                             user__gender = select_gender
        #                         )
        #                     else :
        #                         catsitters = Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             have_pet = select_havePet_value,
        #                             available_weekday_time = select_time,
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             have_pet = select_havePet_value,
        #                             available_weekend_time = select_time,
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         ) | Catsitter.objects.filter(
        #                             available_place = select_place_value,
        #                             available_day = select_day,
        #                             have_pet = select_havePet_value,
        #                             available_weekend_time = 'both',
        #                             user__gender = select_gender,
        #                             available_pill = select_pill
        #                         )


        print(catsitters)

        print(select_address_value, select_place_value, select_havePet_value, select_day, select_time, select_gender, select_pill)
        
        if select_havePet_value == True :
            select_havePet_value = 'yes'
        elif select_havePet_value == False :
            select_havePet_value = 'no'
        
        if select_pill == True :
            select_pill = 'possible'

        request.session['select_address'] = select_address_value
        request.session['select_place'] = select_place_value
        request.session['select_havePet'] = select_havePet_value
        request.session['day'] = select_day
        request.session['time'] = select_time
        request.session['gender'] = select_gender
        request.session['pill'] = select_pill

        context = { 'user' : user , 
                    'catsitters' : catsitters , 
                    'select_place_value' : select_place_value ,
                    'select_havePet_value' : select_havePet_value,
                    'select_day' : select_day,
                    'select_time' : select_time,
                    'select_gender' : select_gender,
                    'select_pill' : select_pill
                }

        return render(request, 'takmyo_app/search_catsitter.html', context)
    
def get_user_list_by_distance(request) :

    select_address = request.session['select_address']
    select_place_value = request.session['select_place']
    select_havePet_value = request.session['select_havePet']
    select_day = request.session['day']
    select_time = request.session['time']
    select_gender = request.session['gender']
    select_pill = request.session['pill']
    if select_pill == 'possible' :
        select_pill = True

    print(select_address, select_place_value, select_havePet_value, select_day, select_time, select_gender, select_pill)


    if select_place_value == 'both' :
            catsitters = Catsitter.objects.filter(activation=True)
    else :
        catsitters = Catsitter.objects.filter(
            available_place = select_place_value
        )

    print(catsitters)

    if select_havePet_value != 'unknown' :
        catsitters = catsitters.filter(
            have_pet = select_havePet_value
        )

    if select_day != 'both' :
        catsitters = catsitters.filter(
            available_day = select_day
        ) | catsitters.filter(
            available_day = 'both'
        )

    if select_time != 'both' :
        if select_day == 'weekday' :
            catsitters = catsitters.filter(
                available_weekday_time = select_time
            ) | catsitters.filter(
                available_weekday_time = 'both'
            )
        elif select_day == 'weekend' :
            catsitters = catsitters.filter(
                available_weekend_time = select_time
            ) | catsitters.filter(
                available_weekday_time = 'both'
            )
        else :
            catsitters = catsitters.filter(
                available_weekday_time = select_time
            ) | catsitters.filter(
                available_weekend_time = select_time
            ) | catsitters.filter(
                available_weekday_time = 'both'
            )

    if select_gender != 'both' :
        catsitters = catsitters.filter(
            user__gender = select_gender
        )

    if select_pill != 'both' :
        catsitters = catsitters.filter(
            available_pill = select_pill
        )

    print(catsitters)

    serializer = CatsitterSerializer(catsitters, many=True)

    address = select_address
    api_key = "AIzaSyDyFSiU__Yph4023Zgl_Ptc-WNuEQ6jTGU"
    api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
    api_response_dict = api_response.json()

    # print(api_response_dict)

    if api_response_dict['status'] == 'OK':
        latitude = api_response_dict['results'][0]['geometry']['location']['lat']
        longitude = api_response_dict['results'][0]['geometry']['location']['lng']
        print('Latitude:', latitude)
        print('Longitude:', longitude)

        result = { "result" : "success" , 'catsitters' : serializer.data , 'lat' : latitude , 'lng' : longitude }

    else :

        result = { "result" : "success" , 'catsitters' : serializer.data , 'lat' : 0.0 , 'lng' : 0.0 }

    return JsonResponse(result)

def get_user_list_by_rate(request) :

    select_address = request.session['select_address']
    select_place_value = request.session['select_place']
    select_havePet_value = request.session['select_havePet']
    select_day = request.session['day']
    select_time = request.session['time']
    select_gender = request.session['gender']
    select_pill = request.session['pill']
    if select_pill == 'possible' :
        select_pill = True

    print(select_address, select_place_value, select_havePet_value, select_day, select_time, select_gender, select_pill)


    if select_place_value == 'both' :
            catsitters = Catsitter.objects.filter(activation=True)
    else :
        catsitters = Catsitter.objects.filter(
            available_place = select_place_value
        )

    if select_havePet_value != 'unknown' :
        catsitters = catsitters.filter(
            have_pet = select_havePet_value
        )

    if select_day != 'both' :
        catsitters = catsitters.filter(
            available_day = select_day
        ) | catsitters.filter(
            available_day = 'both'
        )

    if select_time != 'both' :
        if select_day == 'weekday' :
            catsitters = catsitters.filter(
                available_weekday_time = select_time
            ) | catsitters.filter(
                available_weekday_time = 'both'
            )
        elif select_day == 'weekend' :
            catsitters = catsitters.filter(
                available_weekend_time = select_time
            ) | catsitters.filter(
                available_weekday_time = 'both'
            )
        else :
            catsitters = catsitters.filter(
                available_weekday_time = select_time
            ) | catsitters.filter(
                available_weekend_time = select_time
            ) | catsitters.filter(
                available_weekday_time = 'both'
            )

    if select_gender != 'both' :
        catsitters = catsitters.filter(
            user__gender = select_gender
        )

    if select_pill != 'both' :
        catsitters = catsitters.filter(
            available_pill = select_pill
        )

    catsitters = catsitters.order_by('-rate')

    serializer = CatsitterSerializer(catsitters, many=True)

    address = select_address
    api_key = "AIzaSyDyFSiU__Yph4023Zgl_Ptc-WNuEQ6jTGU"
    api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
    api_response_dict = api_response.json()

    # print(api_response_dict)

    if api_response_dict['status'] == 'OK':
        latitude = api_response_dict['results'][0]['geometry']['location']['lat']
        longitude = api_response_dict['results'][0]['geometry']['location']['lng']
        print('Latitude:', latitude)
        print('Longitude:', longitude)

        result = { "result" : "success" , 'catsitters' : serializer.data , 'lat' : latitude , 'lng' : longitude }

    else :

        result = { "result" : "success" , 'catsitters' : serializer.data , 'lat' : 0.0 , 'lng' : 0.0 }

    return JsonResponse(result)




# from django.db.models import Q

# def test(request) :

#     User = get_user_model()

#     users = User.objects.filter(~Q(lat=0.0,lng=0.0))

#     context = { 'users' : users }

#     return render(request, 'takmyo_app/test.html', context)

# def get_user_list(request) :

#     User = get_user_model()

#     users = User.objects.filter(~Q(lat=0.0,lng=0.0))

#     if users :

#         serializer = UserSerializer(users, many=True)

#         result = { "result" : "success" , "users" : serializer.data }
    
#     else :

#         result = { "result" : "failed" }

#     return JsonResponse(result)


