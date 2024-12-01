import random

def generate_unique_squawk(existing_codes):
    """
    Generates a unique 4-digit squawk code that does not exist in the provided set.
    """
    while True:
        code = random.randint(1000, 9999)
        if code not in existing_codes:
            existing_codes.add(code)
            return code

def process_dax_file(file_path):
    """
    Processes a .dax file, replacing '9999' in the SA field with a unique random squawk code.
    The input file is overwritten.
    """
    # Read the input file
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Set to store unique squawk codes
    used_codes = set()
    
    # Process the lines
    processed_lines = []
    for line in lines:
        # Check if this line contains the SA field with value 9999
        if line.strip().startswith("SA 9999"):
            # Replace with a unique random squawk code
            squawk_code = generate_unique_squawk(used_codes)
            processed_lines.append(f"SA {squawk_code}\n")
        else:
            # Keep other lines as they are
            processed_lines.append(line)
    
    # Overwrite the input file with the processed content
    with open(file_path, 'w') as file:
        file.writelines(processed_lines)
    
    print(f"File successfully processed and overwritten: {file_path}")


# Example usage:
# Replace 'test.dax' with the path to your .dax file.
file_path = 'test.dax'  # Replace with your actual .dax file path

process_dax_file(file_path)