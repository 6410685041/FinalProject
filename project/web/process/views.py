from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def upload_view(request):
    
    return render(request, "process/submit_task.html")

@login_required
def solarplant_view(request):
    
    return render(request, "process/solarPlant_table.html")

@login_required
def create_solarplant_view(request):
    
    return render(request, "process/create_solarplant.html")
