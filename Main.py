from kivymd.app import MDApp
import os
import time
import datetime
import csv
import json
import requests
import threading
import queue
import CoreLocation
import Foundation
import folium
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from threading import Thread

# Define the constants

# The name of the app
APP_NAME = "Memory Lane"

# The name of the database file
DATABASE_FILE = "memory_lane.db"

# The name of the CSV file that stores the GPS data
CSV_FILE = "gps_data.csv"

# The name of the JSON file that stores the machine learning model
MODEL_FILE = "model.json"

# The number of seconds between each GPS update
GPS_UPDATE_INTERVAL = 60

# The number of seconds between each machine learning model update
MODEL_UPDATE_INTERVAL = 600

# The maximum number of GPS points to store in memory
MAX_GPS_POINTS = 1000

# The maximum number of machine learning model updates to store in memory
MAX_MODEL_UPDATES = 100

# The queue that stores the GPS data
GPS_DATA_QUEUE = queue.Queue()

# The queue that stores the machine learning model updates
MODEL_UPDATE_QUEUE = queue.Queue()

# The thread that reads the GPS data from the device
GPS_READER_THREAD = None

# The thread that updates the machine learning model
MODEL_UPDATER_THREAD = None

# Request location permissions from the user
response = input("This app requires access to your location. Do you give permission? (Y/N): ")
if response.upper() != "Y":
    print("Location permission denied. Exiting the app.")
    exit()
# This code will prompt the user to enter "Y" or "N" to indicate whether they give permission for the app to access their location. If the user enters "N" or anything other than "Y", the code will print a message and exit the app. If the user enters "Y", the app will continue to run and access the GPS data from the device.

# Define the functions

# Modified the read_gps_data function to use the Core Location framework:
# Create a location manager object
location_manager = CoreLocation.CLLocationManager()

# The function that reads the GPS data from the device
def read_gps_data():
    # Request permission from the user to access their location data
    location_manager.requestWhenInUseAuthorization()
    # Start receiving location updates
    location_manager.startUpdatingLocation()
    while True:
        # Get the current location
        location = location_manager.location
        # Get the latitude and longitude of the current location
        latitude = location.coordinate.latitude
        longitude = location.coordinate.longitude
        # Add the GPS point to the queue
        GPS_DATA_QUEUE.put((latitude, longitude))
        # Sleep for the GPS update interval
        time.sleep(GPS_UPDATE_INTERVAL)
        
# Todo Need to impelement Instead of using a CSV file to store GPS data, you can use CoreData, which is an Apple framework for managing persistent storage of data on iOS. From point 2.

# Todo Need to impelement Instead of using JSON serialization to store the machine learning model From point 3.

# The function that updates the machine learning model
def update_model():
    # Open the model file
    with open(MODEL_FILE, "r") as jsonfile:
        # Load the model from the JSON file
        model = json.load(jsonfile)
        # Iterate over the GPS points in the queue
        while not GPS_DATA_QUEUE.empty():
            # Get the next GPS point from the queue
            latitude, longitude = GPS_DATA_QUEUE.get()
            # Add the GPS point to the model
            model.add_point((latitude, longitude))
            # Update the model
            model.update()
            # Save the model to the file
            with open(MODEL_FILE, "w") as jsonfile:
                json.dump(model, jsonfile)
                
# Added error handling to the app to prevent crashes and provide a better user experience. You can add error handling to the app to handle situations such as network errors, GPS data retrieval errors, and machine learning model update errors.               
def update_model():
    # Open the model file
    try:
        with open(MODEL_FILE, "r") as jsonfile:
            # Load the model from the JSON file
            model = json.load(jsonfile)
    except Exception as e:
        print("Error loading model file:", e)
        return

    # Iterate over the GPS points in the queue
    while not GPS_DATA_QUEUE.empty():
        try:
            # Get the next GPS point from the queue
            latitude, longitude = GPS_DATA_QUEUE.get()
        except queue.Empty:
            # Queue is empty, skip this iteration
            continue

        try:
            # Add the GPS point to the model
            model.add_point((latitude, longitude))
            # Update the model
            model.update()
        except Exception as e:
            print("Error updating model:", e)
            continue

        try:
            # Save the model to the file
            with open(MODEL_FILE, "w") as jsonfile:
                json.dump(model, jsonfile)
        except Exception as e:
            print("Error saving model file:", e)
            continue


# The function that starts the GPS reader thread
def start_gps_reader_thread():
    # Create a thread that reads the GPS data from the device
    global GPS_READER_THREAD
    GPS_READER_THREAD = threading.Thread(target=read_gps_data)
    GPS_READER_THREAD.start()

# The function that starts the model updater thread
def start_model_updater_thread():
    # Create a thread that updates the machine learning model
    global MODEL_UPDATER_THREAD
    MODEL_UPDATER_THREAD = threading.Thread(target=update_model)
    MODEL_UPDATER_THREAD.start()

# User Interface To make the app more user-friendly, it can add a user interface that displays the GPS data in a map view, allows the user to start and stop the GPS updates, and displays the machine learning model results in a graphical format.

# Create a global variable to hold the GPS data
gps_data = []

# Create a function to update the GPS data
def update_gps_data():
    # Clear the current GPS data
    global gps_data
    gps_data = []
    # Read the GPS data from the CSV file
    with open("gps_data.csv", "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            latitude = float(row[0])
            longitude = float(row[1])
            gps_data.append((latitude, longitude))
    # Update the map view
    update_map_view()

# Create a function to update the map view
def update_map_view():
    # Create a map centered on the first GPS point
    if gps_data:
        map_center = gps_data[0]
    else:
        map_center = (0, 0)
    my_map = folium.Map(location=map_center, zoom_start=15)
    # Add markers for each GPS point
    for gps_point in gps_data:
        folium.Marker(location=gps_point).add_to(my_map)
    # Display the map
    my_map.save("map.html")
    webbrowser.open("map.html")

# Create a function to start the GPS updates
def start_gps_updates():
    # Start the GPS reader thread
    global GPS_READER_THREAD
    GPS_READER_THREAD = threading.Thread(target=read_gps_data)
    GPS_READER_THREAD.start()

# Create a function to stop the GPS updates
def stop_gps_updates():
    # Stop the GPS reader thread
    global GPS_READER_THREAD
    if GPS_READER_THREAD:
        GPS_READER_THREAD.stop()
        GPS_READER_THREAD = None

# Create the main window
root = Tk()
root.title("Memory Lane")

# Create a frame for the GPS updates
gps_frame = ttk.LabelFrame(root, text="GPS Updates")
gps_frame.pack(padx=10, pady=10)

# Create a button to start the GPS updates
start_button = ttk.Button(gps_frame, text="Start Updates", command=start_gps_updates)
start_button.pack(side=LEFT, padx=5, pady=5)

# Create a button to stop the GPS updates
stop_button = ttk.Button(gps_frame, text="Stop Updates", command=stop_gps_updates)
stop_button.pack(side=LEFT, padx=5, pady=5)

# Create a button to update the GPS data
update_button = ttk.Button(gps_frame, text="Update Data", command=update_gps_data)
update_button.pack(side=LEFT, padx=5, pady=5)

# Create a frame for the machine learning model results
model_frame = ttk.LabelFrame(root, text="Model Results")
model_frame.pack(padx=10, pady=10)

# Create a label for the model results
model_label = ttk.Label(model_frame, text="Model results will be displayed here")
model_label.pack(padx=10, pady=10)

# Start the main loop
root.mainloop()

# The above code uses the folium library to create a map view of the GPS data and displays it in a separate HTML file. It also provides buttons to start and stop the GPS updates, as well as update the GPS data and display the machine learning model results in a label. Note that you will need to import the required libraries (folium, tkinter, csv, threading, webbrowser) at the beginning of the code.

# This will  adjusts the GPS update interval based on the user's activity level to optimize battery level:
# Set the desired accuracy for the location updates
desiredAccuracy = CoreLocation.kCLLocationAccuracyBestForNavigation

# Initialize the location manager
locationManager = CoreLocation.CLLocationManager()
locationManager.desiredAccuracy = desiredAccuracy

# Start monitoring the user's activity level
locationManager.activityType = CoreLocation.CLActivityTypeFitness

# Define the update interval based on the user's activity level
if locationManager.activityType == CoreLocation.CLActivityTypeFitness:
    updateInterval = 5  # seconds
else:
    updateInterval = 60  # seconds

# Set the update interval for the location updates
locationManager.distanceFilter = CoreLocation.kCLDistanceFilterNone
locationManager.desiredAccuracy = desiredAccuracy
locationManager.pausesLocationUpdatesAutomatically = False
locationManager.allowsBackgroundLocationUpdates = True
locationManager.activityType = CoreLocation.CLActivityTypeFitness
locationManager.showsBackgroundLocationIndicator = True
locationManager.startUpdatingLocation()

# Define a function to adjust the update interval based on the user's activity level
def adjustUpdateInterval():
    if locationManager.activityType == CoreLocation.CLActivityTypeFitness:
        updateInterval = 5  # seconds
    else:
        updateInterval = 60  # seconds
    locationManager.distanceFilter = CoreLocation.kCLDistanceFilterNone
    locationManager.desiredAccuracy = desiredAccuracy
    locationManager.activityType = CoreLocation.CLActivityTypeFitness
    locationManager.showsBackgroundLocationIndicator = True
    locationManager.allowDeferredLocationUpdates(untilTraveled=CoreLocation.CLLocationDistanceMax, timeout=30)
    locationManager.disallowDeferredLocationUpdates()
    locationManager.startUpdatingLocation()

# Schedule the function to be called periodically to adjust the update interval
timer = Foundation.NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(60, self, "adjustUpdateInterval", None, True)

class Main_App(MDApp):
    # The main function
    def main():
        # Start the GPS reader thread
        start_gps_reader_thread()
        # Start the model updater thread
        start_model_updater_thread()
        # Enter the main loop
        while True:
            # Sleep for the GPS update interval
            time.sleep(GPS_UPDATE_INTERVAL)
            # Get the next GPS point from the queue
            latitude, longitude = GPS_DATA_QUEUE.get()
            # Print the GPS point
            print("Latitude:", latitude, "Longitude:", longitude)
                        
if __name__ == "__main__":
    Main_App().run()
