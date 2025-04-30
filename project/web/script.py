import os
import django
import subprocess
from dateutil import parser

from dotenv import load_dotenv
load_dotenv()

try:
    # Set up Django environment
    google_cid = os.getenv("GOOGLE_CID")
    google_csecrets = os.getenv("GOOGLE_CSECRETS")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SolarCellProject.settings")
    django.setup()
except Exception as e:
    # Handle the exception (e.g., log it)
    print(f"An error occurred: {e}")

from django.core.management import call_command
from user.models import User, SolarPlant
from process.models import Task
from datetime import datetime
import argparse
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
import pytz


def run_migrations():
    print("Running migrations...")
    subprocess.run(["python", "manage.py", "makemigrations", "user"])
    subprocess.run(["python", "manage.py", "makemigrations", "process"])
    call_command("makemigrations")
    call_command("migrate")
    print("Migrations complete.")

def create_superuser(solarplant):
    username = "admin"
    email = "admin@example.com"
    password = "admin1234"

    # Create the superuser manually, not using call_command
    User = get_user_model()  # Get the custom user model
    
    # Check if a superuser already exists
    if not User.objects.filter(is_superuser=True).exists():
        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                solarPlant=solarplant  # Manually set the Solar Plant
            )
            print(f'Superuser "{username}" created successfully.')
        except Exception as e:
            print(f'Error creating superuser: {e}')
    else:
        print("A superuser already exists.")
        user = User.objects.get(username="admin")

    print("Create super user complete.")
    return user

def create_SolarPlant():
    solarPlant_name = "default department"
    location = "37.7749,-122.4194"

    solarPlant, created = SolarPlant.objects.get_or_create(
        solarPlant_name=solarPlant_name,  # Corrected field name
        defaults={'location': location}  # Create with location if it doesn't exist
    )

    if created:
        print(f'Solar Plant "{solarPlant_name}" created successfully with location {location}.')
    else:
        print(f'Solar Plant "{solarPlant_name}" already exists.')

    return solarPlant

def create_task(user, solarplant):
    weather = "Sunny"
    collected_time = parser.isoparse("2025-04-22T08:05:43.364Z")
    upload_time = datetime.now(pytz.timezone("Asia/Bangkok"))
    temperature = 25.5

    task, created = Task.objects.get_or_create(
        collected_time = collected_time,
        upload_time = upload_time,
        weather = weather,
        temperature = temperature,
        owner = user,
        solarPlant = solarplant,
        video = 'static/video/1.mp4'
    )

    if created:
        print(f'video task created successfully.')
    else:
        print(f'this video task already exists.')

    task, created = Task.objects.get_or_create(
        collected_time = collected_time,
        upload_time = upload_time,
        weather = weather,
        temperature = temperature,
        owner = user,
        solarPlant = solarplant,
        file = 'static/file/file1.mp4'
    )

    if created:
        print(f'image task created successfully.')
    else:
        print(f'this image task already exists.')


def create_initial_data(
    google_cid,
    google_csecrets
):
    print("Creating initial data...")
    # Create some initial data
    try:
        site = Site.objects.get(id=1)
        # If site with ID 1 exists, update its attributes
        site.name = "127.0.0.1"
        site.domain = "127.0.0.1"
        site.save()
    except ObjectDoesNotExist:
        # If site with ID 1 doesn't exist, create a new one
        site = Site.objects.create(id=1, name="127.0.0.1", domain="127.0.0.1")

    google, created = SocialApp.objects.get_or_create(
                            provider="google",
                            defaults={'name': "Google", 'client_id': google_cid, 'secret': google_csecrets}
                        )
    if not created:
        google.name = "Google"
        google.client_id = google_cid
        google.secret = google_csecrets
        google.save()
    google.sites.set([site])

    solarplant = create_SolarPlant()
    user = create_superuser(solarplant)
    create_task(user, solarplant)


if __name__ == "__main__":
    # Parse command-line arguments
    arg_parser = argparse.ArgumentParser(description="Script to help doing the things")
    arg_parser.add_argument("-r", action="store_true", help="Reset")
    arg_parser.add_argument("-m", action="store_true", help="Migrate")
    arg_parser.add_argument("-c", action="store_true", help="Social Account")
    arg_parser.add_argument("-a", action="store_true", help="Activate docker")
    args = arg_parser.parse_args()
    # if args.r:
    #     with open("reset_list.txt", "r") as file:
    #         for to_clear in file.read().split("\n"):
    #             subprocess.run(["rm", "-rf", to_clear])
    #     print("clear file in reset_list DONE!")
    if args.m:
        run_migrations()
    if args.c:
        create_initial_data(
            google_cid,
            google_csecrets
        )
    if args.a:
        call_command('runserver', '0.0.0.0:8000')