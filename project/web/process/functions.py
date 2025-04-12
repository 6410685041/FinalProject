from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse

# create zone
def add_zone(request, task_id):

    return HttpResponseRedirect(reverse("submit_task.html", args=(task.id,)))



def create_solarplant(request):

    return HttpResponseRedirect(reverse("create_solarplant.html"))