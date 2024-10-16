from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'account/login.html')

    return render(request, "home.html")
