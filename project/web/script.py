import os
import django
import subprocess

try:
    # Set up Django environment
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SolarCellProject.settings")
    django.setup()
except Exception as e:
    # Handle the exception (e.g., log it)
    print(f"An error occurred: {e}")

from django.core.management import call_command
from user.models import User, SolarPlant
from datetime import datetime
import argparse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model


def run_migrations():
    print("Running migrations...")
    subprocess.run(["python", "manage.py", "makemigrations", "user"])
    # subprocess.run(["python", "manage.py", "makemigrations", "process"])
    call_command("makemigrations")
    call_command("migrate")
    print("Migrations complete.")

def create_superuser():
    username = "admin"
    email = "admin@example.com"
    password = "admin1234"
    solarPlant_name = "default department"
    location = "37.7749,-122.4194"

    solarPlant, created = SolarPlant.objects.get_or_create(
        solarPlant=solarPlant_name,
        defaults={'location': location}  # Create with location if it doesn't exist
    )

    if created:
        print(f'Solar Plant "{solarPlant_name}" created successfully with location {location}.')
    else:
        print(f'Solar Plant "{solarPlant_name}" already exists.')

    # Create the superuser manually, not using call_command
    User = get_user_model()  # Get the custom user model
    try:
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            solarPlant=solarPlant  # Manually set the Solar Plant
        )
        print(f'Superuser "{username}" created successfully.')
    except Exception as e:
        print(f'Error creating superuser: {e}')

    # call_command("createsuperuser", username=username, email=email, department=department, interactive=False)
    # # Set the password for the created superuser
    # user = Profile.objects.get(username=username)
    # user.set_password(password)
    # user.save()
    print("Create super user complete.")

if __name__ == "__main__":
    # Parse command-line arguments
    # parser = argparse.ArgumentParser(description="Script to help doing the things")
    # parser.add_argument("-r", action="store_true", help="Reset")
    # parser.add_argument("-s", action="store_true", help="Setting")
    # parser.add_argument("-a", action="store_true", help="Activate docker")
    # args = parser.parse_args()
    # if args.r:
    #     # with open("reset_list.txt", "r") as file:
    #     #     for to_clear in file.read().split("\n"):
    #     #         subprocess.run(["rm", "-rf", to_clear])
    #     # print("clear file in reset_list DONE!")
    # if args.s:
    run_migrations()
    create_superuser()
    # if args.a:
    #     subprocess.run(["docker", "compose", "down"])
    #     subprocess.run(["docker", "compose", "up", "-d"])