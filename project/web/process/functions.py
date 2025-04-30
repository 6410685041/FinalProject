from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
import requests
import json
from datetime import datetime, timezone
import pytz
import re
import mimetypes

# create zone
def add_zone(request, task_id):

    return HttpResponseRedirect(reverse("submit_task.html", args=(task.id,)))

def is_valid_coordinate(location):
    pattern = r"^-?\d+(\.\d+)?, ?-?\d+(\.\d+)?$"
    return bool(re.match(pattern, location))

@require_http_methods(["POST"])
def create_solarplant(request):
    try:
        # Collect data from POST request
        solarPlant_name = request.POST.get('solarPlant_name')
        location = request.POST.get('location')

         # check if input is correct
        if not is_valid_coordinate(location) or not solarPlant_name:
            return HttpResponseRedirect(reverse("create_solarplant_view"))
        elif len(solarPlant_name) < 5:
            return HttpResponseRedirect(reverse("create_solarplant_view"))

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

def valid_zipfile(file):
    mime_type, _ = mimetypes.guess_type(file.name)
    return mime_type == 'application/zip'

def valid_videofile(file):
    mime_type, _ = mimetypes.guess_type(file.name)
    return mime_type in ['video/mp4', 'video/mpeg']

@require_http_methods(["POST"])
def upload_task(request):
    try:
        # Collect data from POST request
        solarPlant_id = request.POST.get('solarPlant')
        weather = request.POST.get('weather')
        video = request.FILES.get('video') #can be null
        image = request.FILES.get('image') #can be null
        collected_time_str = request.POST.get('collected_time')
        collected_time = datetime.strptime(collected_time_str, "%Y-%m-%dT%H:%M").replace(tzinfo=timezone.utc)
        temperature = request.POST.get('temperature')
        owner = request.user.id
        upload_time = datetime.now(timezone.utc)

        # check condition input
        if not (video or image) :
            # request.session['transfer_data'] = {'message':'Please input image or video'}
            request.session['transfer_data'] = {'message':str(image)}
            return HttpResponseRedirect(reverse("upload_view"))
        elif not solarPlant_id or not weather or not temperature or not owner or not collected_time:
            request.session['transfer_data'] = {'message':'Please input all field'}
            return HttpResponseRedirect(reverse("upload_view"))
        elif collected_time > upload_time:
            request.session['transfer_data'] = {'message':'The collected date should be today or in the past.'}
            return HttpResponseRedirect(reverse("upload_view"))
        else: # Validate File
            if image and not valid_zipfile(image):
                request.session['transfer_data'] = {'message':'Please make image in zip file'}
                return HttpResponseRedirect(reverse("upload_view"))
            elif video and not valid_videofile(video):
                request.session['transfer_data'] = {'message':'Please select video file'}
                return HttpResponseRedirect(reverse("upload_view"))

        # Data to be sent to the external API
        data = {
                    'task_form': json.dumps({
                        'solarPlant_id': str(solarPlant_id),
                        'weather': weather,
                        'collected_time': collected_time.isoformat(),
                        'upload_time': upload_time.isoformat(),
                        'temperature': temperature,
                        'owner': owner
                    })
                }
        
        files = {}
        if video:
            files['video'] = (video.name, video.file, video.content_type)
        if image:
            files['image'] = (image.name, image.file, image.content_type)

        
        # URL of the external API
        api_url = 'http://collector:5003/Task/upload_task'
        
        # Send data to the external API
        # response = requests.post(api_url, data=data, files=files)
        response = requests.post(api_url, data=data)
        response_data = response.json()

        request.session['transfer_data'] = response_data

        if response.status_code == 200:
            return HttpResponseRedirect(reverse("task_view"))
        else:
            data = str(response)
            return render(request, "process/upload_task.html", {'message':data})
            # return HttpResponseRedirect(reverse("upload_view"))
    except Exception as e:
        error_message = str(e)  # Convert the exception to a string
        request.session['transfer_data'] = {'message': error_message}
        return HttpResponseRedirect(reverse("upload_view"))

# @require_http_methods(["POST"])
# def submit_task(request):
#     try:
#         # Collect data from POST request
#         solarPlant_name = request.POST.get('solarPlant_name')
#         location = request.POST.get('location')

#         # Data to be sent to the external API
#         data = {'solarPlant_name': solarPlant_name, 'location': location}
        
#         # URL of the external API
#         api_url = 'http://collector:5003/SolarPlant/create'
        
#         # Send data to the external API
#         response = requests.post(api_url, json=data)
#         response_data = response.json()

#         request.session['transfer_data'] = response_data

#         if response.status_code == 200:
#             return HttpResponseRedirect(reverse("solarplant_view"))
#         else:
#             return HttpResponseRedirect(reverse("create_solarplant_view"))
#     except Exception as e:
#         return HttpResponseRedirect(reverse("create_solarplant_view"))
