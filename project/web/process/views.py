from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
import json

# Create your views here.

# for upload task - add files
@login_required
def upload_view(request):
    try:
        # Replace with the full URL if calling an external API
        api_url = "http://collector:5003/SolarPlant/all"
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        data = response.json()  # Parse JSON response
        if isinstance(data, str):
            data = json.loads(data)
        message = request.session.pop('transfer_data', None)
    except requests.RequestException as e:
        data = [e]  # Default to empty list or handle error logging
        return redirect("home")
    
    return render(request, "process/upload_task.html", {
        "solarplants": data,
        "message": message
    })

@login_required
def task_view(request):
    try:
        # Replace with the full URL if calling an external API
        api_url = "http://collector:5003/Task/total"
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        data = response.json()  # Parse JSON response
        if isinstance(data, str):
            data = json.loads(data)
        message = request.session.pop('transfer_data', None)
    except requests.RequestException as e:
        data = [e]  # Default to empty list or handle error logging
        return redirect("home")
    
    return render(request, "process/task_table.html",
                  {"task":data})

# for submit task - add zone
@login_required
def submit_view(request, task_id):
    return render(request, "process/submit_task.html")


@login_required
def solarplant_view(request):
    try:
        # Replace with the full URL if calling an external API
        api_url = "http://collector:5003/SolarPlant/data"
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        data = response.json()  # Parse JSON response
        if isinstance(data, str):
            data = json.loads(data)
        message = request.session.pop('transfer_data', None)
    except requests.RequestException as e:
        data = [e]  # Default to empty list or handle error logging
        print("API Error:", e)

    return render(request, "process/solarPlant_table.html", {
        "solarplants": data,
        "message": message
    })

@login_required
def create_solarplant_view(request):
    return render(request, "process/create_solarplant.html")
