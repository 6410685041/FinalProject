from django.urls import path
from process import functions

urlpatterns = [
    # path('add_zone/<int:task_id>', functions.add_zone, name='add_zone'), 
    path('add_zone', functions.add_zone, name='add_zone'), 
    path('create', functions.create_solarplant, name='create_solarplant'),
    path('upload_task', functions.upload_task, name='upload_task'),
    # path('submit_task', functions.submit_task, name='submit_task'),
]