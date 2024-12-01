import pandas as pd

# Load the Excel file
file_path = 'STAR_ALLOCATION.xlsx'
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
            time = row['TIME']
            star = row['STAR']
            rwy = row['RWY']
            
            # Format the time to "HHMMSS" format
            formatted_time = pd.to_datetime(time).strftime('%H%M%S')
            
            # Generate the lines
            output_lines.append(f"+{formatted_time} {ident} ARRIVAL RUNWAY {rwy}")
            output_lines.append(f"+{formatted_time} {ident} STAR {star}")
    
    # Add a footer to separate sheets visually
    output_lines.append(f"--- END OF SHEET: {sheet} ---\n")

# Save the results to a text file for further use
output_file_path = 'scripts.txt'
with open(output_file_path, 'w') as file:
    for line in output_lines:
        file.write(line + '\n')

print(f"Lines have been generated and saved to {output_file_path}")