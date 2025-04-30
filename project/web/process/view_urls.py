from django.urls import path
from . import views

urlpatterns = [
    path('Upload', views.upload_view, name='upload_view'),
    path('SolarPlant', views.solarplant_view, name='solarplant_view'),
    path('SolarPlant/Create', views.create_solarplant_view, name='create_solarplant_view'),
    path('Task', views.task_view, name='task_view'),
    path('Task/Submit_task/<int:task_id>', views.submit_view, name='submit_view'),
]
