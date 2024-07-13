"""
    File from where the application will be run
"""

# Imports
from extractor import Extractor
from userinterface import UserInterface

def main():
    extractor = Extractor()
    ui = UserInterface(extractor)
    ui.run()

if __name__ == "__main__":
    main()