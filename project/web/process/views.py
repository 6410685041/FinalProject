from django.shortcuts import render

# Create your views here.
def upload_view(request):
    
    return render(request, "process/submit_task.html")

def solarplant_view(request):
    
    return render(request, "process/solarPlant_table.html")