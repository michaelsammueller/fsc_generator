"""
    Contains the user interface class
"""

# Imports
import tkinter as tk
from tkinter import filedialog, messagebox
import os

# UI Class
class UserInterface:
    def __init__(self, extractor):
        self.root = tk.Tk()
        self.root.title("HackerPrep")
        self.extractor = extractor
        self.selected_dax_files = []
        self.airspace_path = ""

        self.create_widgets()
    
    def create_widgets(self):
        # DAX file selection
        self.dax_button = tk.Button(self.root, text="DAX", command=self.browse_dax)
        self.dax_button.grid(row=0, column=0, padx=10, pady=10)
        self.dax_label = tk.Label(self.root, text="No DAX file selected")
        self.dax_label.grid(row=0, column=1, padx=10, pady=10)

        # Airspace selection
        self.airspace_button = tk.Button(self.root, text="Airspace", command=self.browse_airspace)
        self.airspace_button.grid(row=1, column=0, padx=10, pady=10)
        self.airspace_label = tk.Label(self.root, text="No airspace selected")
        self.airspace_label.grid(row=1, column=1, padx=10, pady=10)

        # File type label
        self.file_type_label = tk.Label(self.root, text="File type:")
        self.file_type_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        # File type checkboxes
        self.fsc_var = tk.BooleanVar()
        self.fsc_check = tk.Checkbutton(self.root, text=".fsc", variable=self.fsc_var)
        self.fsc_check.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.esc_var = tk.BooleanVar()
        self.esc_check = tk.Checkbutton(self.root, text=".esc", variable=self.esc_var)
        self.esc_check.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        # Script macros label
        self.script_macros_label = tk.Label(self.root, text="Script Macros:")
        self.script_macros_label.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # ALL CLEAR TAKE OFF IMMEDIATE checkbox
        self.all_clear_var = tk.BooleanVar()
        self.all_clear_check = tk.Checkbutton(self.root, text="ALL CLEAR TAKE OFF IMMEDIATE", variable=self.all_clear_var)
        self.all_clear_check.grid(row=3, column=1, columnspan=2, padx=10, pady=5, sticky="w")

        # Checked list box for .dsc files
        self.dsc_listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE)
        self.dsc_listbox.grid(row=4, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Generate button
        self.generate_button = tk.Button(self.root, text="Generate", command=self.generate_files)
        self.generate_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # Configure grid
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
    
    def browse_dax(self):
        files = filedialog.askopenfilenames(filetypes=[("DAX files", "*.dax")])
        if files:
            self.selected_dax_files = files[:200]  # Limit to 200 files
            self.update_dax_label()

    def update_dax_label(self):
        count = len(self.selected_dax_files)
        if count == 0:
            self.dax_label.config(text="No DAX file selected")
        elif count == 1:
            self.dax_label.config(text="1 DAX file selected")
        else:
            self.dax_label.config(text=f"{count} DAX files selected")
    
    def browse_airspace(self):
        folder = filedialog.askdirectory()
        if folder:
            self.airspace_path = folder
            self.airspace_label.config(text=f"Selected: {os.path.basename(folder)}")
            self.load_dsc_files()
    
    def load_dsc_files(self):
        self.dsc_listbox.delete(0, tk.END)
        if os.path.exists(self.airspace_path):
            dsc_files = [f for f in os.listdir(self.airspace_path) if f.endswith('.dsc')]
            for file in dsc_files:
                self.dsc_listbox.insert(tk.END, file)
        else:
            messagebox.showerror("Error", f"Directory not found: {self.airspace_path}")
    
    def generate_files(self):
        if not self.selected_dax_files:
            messagebox.showerror("Error", "Please select at least one DAX file.")
            return
    
        for dax_file in self.selected_dax_files:
            if self.fsc_var.get():
                callsigns = self.extractor.extract_callsigns(dax_file)
                fsc_lines = self.extractor.generate_fsc_lines(callsigns)
                self.extractor.write_fsc(fsc_lines, dax_file)
            
            if self.esc_var.get():
                checked_items = [self.dsc_listbox.get(idx) for idx in self.dsc_listbox.curselection()]
                self.extractor.generate_esc(dax_file, self.all_clear_var.get(), checked_items)
        
        messagebox.showinfo("Success", "Files generated successfully.")
    
    def run(self):
        self.root.mainloop()