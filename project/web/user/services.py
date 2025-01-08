from .models import User, SolarPlant

# Admin actions
def delete_user(user_id):
    User.objects.filter(id=user_id).delete()

def approve_user(user_id):
    User.objects.filter(id=user_id).update(is_approved=True)

def create_solar(solar_plant_name, location):
    SolarPlant.objects.create(name=solar_plant_name, location=location)

def display_results():
    # return SolarPlant.objects.all()
    pass

# DroneManager actions
def create_task(video_field, solar_plant_id):
    # solar_plant = SolarPlant.objects.get(id=solar_plant_id)
    # Task.objects.create(video=video_field, solar_plant=solar_plant)
    pass

def display_drone_results():

    pass