"""
    Updated user interface class with SID/STAR allocation and squawk functionality
"""

# Imports
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from sid_star_allocation import process_excel_file
from extractor import Extractor
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
        self.notebook = ttk.Notebook(self.root)
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
        # Use a frame for the main section
        main_frame = tk.Frame(self.main_page, padx=20, pady=20)
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Add section for DAX file selection
        dax_frame = tk.LabelFrame(main_frame, text="DAX File Selection", padx=10, pady=10)
        dax_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        tk.Button(dax_frame, text="Select DAX Files", command=self.browse_dax).grid(row=0, column=0, padx=5, pady=5)
        self.dax_label = tk.Label(dax_frame, text="No DAX file selected")
        self.dax_label.grid(row=0, column=1, padx=5, pady=5)
        self.squawk_var = tk.BooleanVar()
        tk.Checkbutton(dax_frame, text="Generate Random Squawks", variable=self.squawk_var).grid(
            row=1, column=0, columnspan=2, pady=5, sticky="w"
        )
        
        # Add section for Airspace folder selection
        airspace_frame = tk.LabelFrame(main_frame, text="Airspace Selection", padx=10, pady=10)
        airspace_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)
        tk.Button(airspace_frame, text="Select Airspace Folder", command=self.browse_airspace).grid(row=0, column=0, padx=5, pady=5)
        self.airspace_label = tk.Label(airspace_frame, text="No airspace selected")
        self.airspace_label.grid(row=0, column=1, padx=5, pady=5)
        
        # Add section for file type selection
        file_type_frame = tk.LabelFrame(main_frame, text="File Type Selection", padx=10, pady=10)
        file_type_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)
        self.fsc_var = tk.BooleanVar()
        tk.Checkbutton(file_type_frame, text=".fsc", variable=self.fsc_var).grid(row=0, column=0, padx=5, pady=5)
        self.esc_var = tk.BooleanVar()
        tk.Checkbutton(file_type_frame, text=".esc", variable=self.esc_var).grid(row=0, column=1, padx=5, pady=5)
        
        # Add section for script macros
        macro_frame = tk.LabelFrame(main_frame, text="Script Macros", padx=10, pady=10)
        macro_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)
        self.macro_list = tk.Listbox(macro_frame, height=5)
        self.macro_list.pack(fill="both", expand=True)
        self.immediate_var = tk.BooleanVar()
        tk.Checkbutton(macro_frame, text="ALL CLEAR TAKEOFF IMMEDIATE", variable=self.immediate_var).pack(pady=5, anchor="w")
        
        # Add Generate button
        tk.Button(main_frame, text="Generate", command=self.generate_files).grid(
            row=4, column=0, columnspan=2, pady=10
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

    def browse_airspace(self):
        folder = filedialog.askdirectory()
        if folder:
            self.airspace_path = folder
            self.airspace_label.config(text=os.path.basename(folder))
            self.populate_macro_list(folder)

    def populate_macro_list(self, folder):
        """Populate the macro list with .dsc files from the selected airspace folder"""
        # Clear existing items
        self.macro_list.delete(0, tk.END)
        
        # Walk through the directory and find all .dsc files
        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith('.dsc'):
                    self.macro_list.insert(tk.END, file)

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

        # if self.airspace_path == "":
            # messagebox.showerror("Error", "Please select an airspace folder.")
            # return
        
        # Extract callsigns from th eselected DAX files
        callsigns = []
        for dax_file in self.selected_dax_files:
            callsigns.extend(self.extractor.extract_callsigns(dax_file))
        
        # Generate .fsc if checkbox is ticked
        if self.fsc_var.get():
            fsc_lines = self.extractor.generate_fsc_lines(callsigns)
            self.extractor.write_fsc(fsc_lines, self.selected_dax_files[0])  # Use the first DAX file as output path
        
        # Generate .esc if checkbox is ticked
        if self.esc_var.get():
            checked_items = [self.macro_list.get(i) for i in self.macro_list.curselection()]
            all_clear = self.immediate_var.get()
            self.extractor.generate_esc(self.selected_dax_files[0], all_clear, checked_items)

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
