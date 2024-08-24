import os

# Suppress TensorFlow and gRPC logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logs (errors only)
os.environ['GRPC_VERBOSITY'] = 'ERROR'    # Suppress gRPC logs
os.environ['GRPC_TRACE'] = ''             # Disable gRPC tracing

# Now import the rest of your libraries
import shutil
import json
import requests
from dotenv import load_dotenv
from gemini import generate

import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)

import logging
logging.getLogger('tensorflow').setLevel(logging.ERROR)
logging.getLogger('grpc').setLevel(logging.ERROR)

load_dotenv()

# Path for disk space and cleanup functions
path = "C:\\"

def greetings():
    print("Welcome to Stella!")
    greets = input("How was your day? ")
    if "how about yours" in greets.lower():
        print("I'm an AI, so I don't have days, but I'm here to help you!")
    else:
        print(generate(greets) + "\n\n")


def weather():
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    API_KEY = os.getenv("WEATHER_API_KEY")
    CITY = "Tunis, TN"  # Ensure the city name is formatted correctly

    def kelvin_to_celsius(kelvin):
        return kelvin - 273.15

    url = f"{BASE_URL}q={CITY}&appid={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        temp_kelvin = data['main']['temp']
        description = data['weather'][0]['description']
        temp_celsius = kelvin_to_celsius(temp_kelvin)
        print(f"Temperature in Celsius: {temp_celsius:.0f}°C")
        print(f"Description: {description}")
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
    except KeyError:
        print("Error parsing weather data.")
    


def cleanup_desktop():
    desktop_path = r"C:\Users\karlx\Desktop"

    files = [os.path.join(desktop_path, f) for f in os.listdir(desktop_path) if os.path.isfile(os.path.join(desktop_path, f))]

    i = 1
    destinationdir = os.path.join(desktop_path, "Garbage")
    original_destinationdir = destinationdir
    while os.path.exists(destinationdir):
        destinationdir = f"{original_destinationdir}_{i}"
        i += 1

    try:
        os.makedirs(destinationdir)
        print(f"Directory created: {destinationdir}")
    except Exception as e:
        print(f"Failed to create directory: {e}")
        return

    original_paths = {}

    for x in files:
        try:
            new_path = os.path.join(destinationdir, os.path.basename(x))
            shutil.move(x, new_path)
            original_paths[new_path] = x
            print(f"Moved {x} to {destinationdir}")
        except Exception as e:
            print(f"Failed to move {x}: {e}")

    undo_file = os.path.join(destinationdir, "undo.json")
    with open(undo_file, 'w') as f:
        json.dump(original_paths, f)

    print("Desktop cleanup complete!")
    print(f"Undo information saved to {undo_file}")



def undo_cleanup():
    desktop_path = r"C:\Users\karlx\Desktop"
    garbage_folder = os.path.join(desktop_path, "Garbage")
    undo_file = os.path.join(garbage_folder, "undo.json")

    if not os.path.exists(undo_file):
        print("Undo file not found.")
        return

    with open(undo_file, 'r') as f:
        original_paths = json.load(f)

    for new_path, original_path in original_paths.items():
        try:
            shutil.move(new_path, original_path)
            print(f"Moved {new_path} back to {original_path}")
        except Exception as e:
            print(f"Failed to undo move for {new_path}: {e}")

    print("Undo complete!")



def view_space(path):
    total, used, free = shutil.disk_usage(path)
    print(f"Total: {total // (2**30)} GB")
    print(f"Used: {used // (2**30)} GB")
    print(f"Free: {free // (2**30)} GB")




def Stella():
    print("\n\nWhat would you like to do?")
    print("1. Clean up the desktop")
    print("2. Undo the last cleanup")
    print("3. View Space")
    print("4. Check Weather")  # Added weather option
    print("5. Exit")
    try:
        choice = input("Enter your choice: ")
        match choice:
            case "1":
                cleanup_desktop()
            case "2":
                undo_cleanup()
            case "3":
                view_space(path) # <--- dont touch the parameter, it works
            case "4":
                weather()  # Added weather function call
            case "5":
                print("Goodbye!")
                exit()
            case _:
                print("Invalid choice. Please try again.")
    except KeyboardInterrupt:
        print("Goodbye!")
        exit()
    except ValueError:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    greetings()
    Stella()  # Call Stella to start the menu
