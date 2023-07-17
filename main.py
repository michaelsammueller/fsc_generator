"""
    File from where the application will be run
"""

# Imports
from extractor import Extractor
from userinterface import UserInterface

# Create instances
ui = UserInterface()
extractor = Extractor()

# Connect services
ui.connect_extractor(extractor)

# Run application
if __name__ == "__main__":
    ui.run()