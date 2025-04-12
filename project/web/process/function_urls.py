from django.urls import path
from process import functions

urlpatterns = [
    # path('add_zone/<int:task_id>', functions.add_zone, name='add_zone'), 
    path('add_zone', functions.add_zone, name='add_zone'), 
    path('create', functions.create_solarplant, name='create_solarplant'), 
]