from django.shortcuts import render

# Create your views here.
def index(request) :

    return render(request, 'takmyo_app/index.html')

def join(request) :

    return render(request, 'takmyo_app/join.html')