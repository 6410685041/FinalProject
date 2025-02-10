from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from allauth.account.views import SignupView

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'account/login.html')

    return render(request, "home.html")
    # return render(request, "process/submit_task.html")

class CustomSignupView(SignupView):
    template_name = "account/signup.html"