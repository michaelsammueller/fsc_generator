import pandas as pd
from tkinter import messagebox
from datetime import datetime, time, timedelta

def process_excel_file(file_path):
    try:
        # Load the Excel file
        excel_file = pd.ExcelFile(file_path)

        # Initialize a list to store results
        output_lines = []

        # Loop over each sheet and process the data
        for sheet in excel_file.sheet_names:
            # Add a header to indicate the beginning of a new sheet
            output_lines.append(f"--- START OF SHEET: {sheet} ---")
            
            # Read the sheet into a DataFrame
            df = excel_file.parse(sheet)
            
            # Ensure required columns exist in the current sheet
            if {'IDENT', 'TIME', 'STAR', 'RWY'}.issubset(df.columns):
                for _, row in df.iterrows():
                    ident = row['IDENT']
                    time_value = row['TIME']
                    star = row['STAR']
                    rwy = row['RWY']
                    
                    # Handle TIME values (either str or datetime.time)
                    if isinstance(time_value, str):
                        try:
                            base_time = datetime.strptime(time_value, '%H:%M:%S')
                        except ValueError:
                            base_time = None
                    elif isinstance(time_value, time):  # Correctly reference datetime.time
                        base_time = datetime.combine(datetime.today(), time_value)
                    else:
                        base_time = None

                    if base_time:
                        formatted_time_1 = base_time.strftime('%H%M%S')
                        formatted_time_2 = (base_time + timedelta(seconds=1)).strftime('%H%M%S')
                    else:
                        formatted_time_1 = "UNKNOWN"
                        formatted_time_2 = "UNKNOWN"

                    # Generate the lines
                    output_lines.append(f"+{formatted_time_1} {ident} ARRIVAL RUNWAY {rwy}")
                    output_lines.append(f"+{formatted_time_2} {ident} STAR {star}")
            
            # Add a footer to separate sheets visually
            output_lines.append(f"--- END OF SHEET: {sheet} ---\n")

        # Save the results to a text file for further use
        output_file_path = 'scripts.txt'
        with open(output_file_path, 'w') as file:
            for line in output_lines:
                file.write(line + '\n')

        # Show a success message
        messagebox.showinfo("Success", f"SID/STAR Allocation processed successfully. Output saved to {output_file_path}")

    except Exception as e:
        # Show an error message in case of failure
        messagebox.showerror("Error", f"An error occurred while processing the file: {str(e)}")
