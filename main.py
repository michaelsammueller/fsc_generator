import os
import json
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox, ttk
from extractor import Extractor
from userinterface import UserInterface
from threading import Thread

# Path to store the timestamp file in the user's home directory
DATA_FILE = os.path.join(os.path.expanduser("~"), "app_data.json")
LOCKED_MESSAGE = "This application has been locked. Please contact the developer for access."

def cleanup_old_versions(progress_callback=None):
    """Run the cleanup process for old versions"""
    from del import process_machines
    
    # Create a temporary progress window
    cleanup_window = tk.Toplevel()
    cleanup_window.title("Cleaning up old versions")
    cleanup_window.geometry("400x150")
    
    # Add progress bar and label
    progress_label = tk.Label(cleanup_window, text="Removing old versions...")
    progress_label.pack(pady=10)
    
    progress_bar = ttk.Progressbar(
        cleanup_window, 
        orient="horizontal", 
        length=300, 
        mode="determinate"
    )
    progress_bar.pack(pady=10)
    
    def on_cleanup_complete():
        cleanup_window.destroy()
        messagebox.showinfo("Cleanup Complete", "Old versions have been removed successfully.")
    
    # Start the cleanup process in a separate thread
    keywords = ["Waker", "Sauerkraut", "HackerPrep", "Hafaza"]
    Thread(
        target=process_machines,
        args=(keywords, progress_bar, progress_label, on_cleanup_complete),
        daemon=True
    ).start()

def initialize_application():
    """Initialize the application and run first-time setup if needed."""
    is_first_run = not os.path.exists(DATA_FILE)
    
    if is_first_run:
        # Run cleanup of old versions
        cleanup_old_versions()
        
        # Store the first-use timestamp
        with open(DATA_FILE, 'w') as file:
            data = {
                'first_use': datetime.now().isoformat(),
                'cleanup_performed': True
            }
            json.dump(data, file)
    
    return is_first_run

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
    app = UserInterface(extractor)
    app.run()

if __name__ == "__main__":
    main()
