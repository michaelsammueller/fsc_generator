"""
    Contains the user interface class
"""

# Imports
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# UI Class
class UserInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.file_path = tk.StringVar()  # Holds path of selected file
        self.root.title("FSC Converter")  # Set window title

    def create_widgets(self):
        """Creates widgets for GUI"""
        # Create an entry field to display the selected file path
        file_label = tk.Label(self.root, text="Selected DAX file:")
        file_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        file_entry = tk.Entry(self.root, textvariable=self.file_path, state='readonly')
        file_entry.grid(row=0, column=1, padx=10, pady=10)

        # Create a "Browse" button to open the file dialog
        browse_button = tk.Button(self.root, text="Browse", command=self.browse_file)
        browse_button.grid(row=1, column=0, padx=10, pady=10)

        # Create a "Generate" button to generate the .fsc file
        generate_button = tk.Button(self.root, text = "Generate FSC", command=self.generate_fsc)
        generate_button.grid(row=1, column=1, padx=10, pady=10)
        # Save the "Generate" button in an instance variable to control its state
        self.generate_button = generate_button
    
    def browse_file(self):
        # Open file dialog to select the .dax file
        path = filedialog.askopenfilename(filetypes=[("DAX files", "*.dax")])
        # Update the file path in the entry field
        if path:
            self.file_path.set(path)
            self.generate_button['state'] = 'normal'  # Enable the generate button
    
    def generate_fsc(self):
        path = self.file_path.get() # Gets file path from entry field
        if path:
            try:
                callsigns = self.__extractor.extract_callsigns(path)
                script_lines = self.__extractor.generate_fsc(callsigns)
                # Write to file
                self.__extractor.write_fsc(script_lines, path)
                messagebox.showinfo("Success", "FSC file generated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while generating the FSC file: {e}")    
        else:
            messagebox.showerror("Error", "Please select a DAX file first.")

    def connect_extractor(self, extractor):
        """Connects extractor to user interface"""
        self.__extractor = extractor

    def run(self):
        self.create_widgets()
        self.root.mainloop()