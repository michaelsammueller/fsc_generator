import os
import json
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox
from extractor import Extractor
from userinterface import UserInterface

# Path to store the timestamp file in the user's home directory
DATA_FILE = os.path.join(os.path.expanduser("~"), "app_data.json")
LOCKED_MESSAGE = "This application has been locked. Please contact the developer for access."

def initialize_application():
    """Initialize the application by storing the first-use timestamp if not already recorded."""
    if not os.path.exists(DATA_FILE):
        # Store the first-use timestamp
        with open(DATA_FILE, 'w') as file:
            data = {'first_use': datetime.now().isoformat()}
            json.dump(data, file)

def is_application_locked():
    """Check if the application should be locked."""
    if not os.path.exists(DATA_FILE):
        return False  # If the data file does not exist, assume the app is not locked.

    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            first_use = datetime.fromisoformat(data['first_use'])
            # Check if 2 months (60 days) have passed
            if datetime.now() > first_use + timedelta(days=60):
                return True
    except Exception as e:
        print(f"Error reading data file: {e}")
        return True  # Fail-safe: Lock the application if data cannot be read.
    return False

def lock_application():
    """Display the lock message using tkinter and exit the application."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Application Locked", LOCKED_MESSAGE)
    exit()

def main():
    # Initialize the application and check lock status
    initialize_application()
    if is_application_locked():
        lock_application()
    
    # Run the application if not locked
    extractor = Extractor()
    ui = UserInterface(extractor)
    ui.run()

if __name__ == "__main__":
    main()
