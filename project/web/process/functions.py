from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
import requests
import json

# create zone
def add_zone(request, task_id):

    return HttpResponseRedirect(reverse("submit_task.html", args=(task.id,)))


@require_http_methods(["POST"])
def create_solarplant(request):
    try:
        # Collect data from POST request
        solarPlant_name = request.POST.get('solarPlant_name')
        location = request.POST.get('location')

        # Data to be sent to the external API
        data = {'solarPlant_name': solarPlant_name, 'location': location}
        
        # URL of the external API
        api_url = 'http://collector:5003/SolarPlant/create'
        
        # Send data to the external API
        response = requests.post(api_url, json=data)
        response_data = response.json()

        request.session['transfer_data'] = response_data

        if response.status_code == 200:
            return HttpResponseRedirect(reverse("solarplant_view"))
        else:
            return HttpResponseRedirect(reverse("create_solarplant_view"))
    except Exception as e:
        return HttpResponseRedirect(reverse("create_solarplant_view"))
