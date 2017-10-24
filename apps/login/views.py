from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages
import bcrypt
from django.contrib.messages import error


# Create your views here.

def index(request):
    return render(request,'login/index.html')


def create(request):
    errors= User.objects.validate_registration(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            error(request, message, extra_tags=field)
        return redirect('/')
    else:
        user = User.objects.valid_user(request.POST)
        request.session['user_id'] = user.id
        messages.success(request, "registered")
        return redirect ('/success')



def login(request):
    errors= User.objects.validate_login(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            error(request, message, extra_tags=field)
        return redirect('/')
    else:
        user = User.objects.valid_login(request.POST)
        request.session['user_id'] = user.id
        messages.success(request, "Logged in")
        return redirect('/success')



def success(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'login/success.html', context)