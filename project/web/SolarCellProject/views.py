from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from allauth.account.views import SignupView

def home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("account_login"))

    return render(request, "home.html")
    # return render(request, "process/submit_task.html")

class CustomSignupView(SignupView):
    template_name = "account/signup.html"