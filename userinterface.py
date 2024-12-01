"""
    Updated user interface class with SID/STAR allocation and squawk functionality
"""

# Imports
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from sid_star_allocation import process_excel_file
from squawk import process_dax_file

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
        # Create Notebook for Tabs
        self.notebook = tk.ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        # Tab 1 - Main Page
        self.main_page = tk.Frame(self.notebook)
        self.notebook.add(self.main_page, text="Main")

        # Tab 2 - SID/STAR Allocation
        self.sid_star_page = tk.Frame(self.notebook)
        self.notebook.add(self.sid_star_page, text="SID/STAR Allocation")

        # Widgets for Main Page
        self.create_main_page_widgets()

        # Widgets for SID/STAR Page
        self.create_sid_star_page_widgets()

        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

    def create_main_page_widgets(self):
        # DAX file selection
        tk.Button(self.main_page, text="DAX", command=self.browse_dax).grid(row=0, column=0, padx=10, pady=10)
        self.dax_label = tk.Label(self.main_page, text="No DAX file selected")
        self.dax_label.grid(row=0, column=1, padx=10, pady=10)

        # Squawk generation checkbox
        self.squawk_var = tk.BooleanVar()
        tk.Checkbutton(self.main_page, text="Generate Random Squawks", variable=self.squawk_var).grid(
            row=1, column=0, padx=10, pady=10
        )

        # Generate button
        tk.Button(self.main_page, text="Generate", command=self.generate_files).grid(
            row=2, column=0, columnspan=2, padx=10, pady=10
        )

    def create_sid_star_page_widgets(self):
        # File selection for SID/STAR Allocation
        tk.Button(self.sid_star_page, text="Select Excel File", command=self.browse_sid_star_file).grid(
            row=0, column=0, padx=10, pady=10
        )
        self.sid_star_label = tk.Label(self.sid_star_page, text="No Excel file selected")
        self.sid_star_label.grid(row=0, column=1, padx=10, pady=10)

        # Process button
        tk.Button(self.sid_star_page, text="Process", command=self.process_sid_star_file).grid(
            row=1, column=0, columnspan=2, padx=10, pady=10
        )

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

    def generate_files(self):
        if not self.selected_dax_files:
            messagebox.showerror("Error", "Please select at least one DAX file.")
            return

        for dax_file in self.selected_dax_files:
            if self.squawk_var.get():
                process_dax_file(dax_file)

        messagebox.showinfo("Success", "Files processed successfully.")

    def browse_sid_star_file(self):
        file = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file:
            self.sid_star_file_path = file
            self.sid_star_label.config(text=f"Selected: {os.path.basename(file)}")

    def process_sid_star_file(self):
        if hasattr(self, "sid_star_file_path"):
            process_excel_file(self.sid_star_file_path)
            messagebox.showinfo("Success", "SID/STAR Allocation processed successfully.")
        else:
            messagebox.showerror("Error", "Please select an Excel file.")

    def run(self):
        self.root.mainloop()
