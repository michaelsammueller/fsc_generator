"""
    Contains the extractor class
"""

# Imports
import os

# Extractor Class
class Extractor:

    def extract_callsigns(self, path):
        """Extracts callsigns from a dax file"""
        # Load the file
        with open(path, "r") as file:
            content = file.readlines()

            # Empty list to store callsigns
            callsigns = []

            # Iterate over each line in content
            for line in content:
                # If the line starts with 'FP', extract the string after
                if line.startswith("FP"):
                    # The callsign is the rest of the line, after removing leftover whitespaces
                    callsign = line[3:].strip()
                    callsigns.append(callsign)
        
            return callsigns
    
    def generate_fsc(self, callsigns):
        """Generates .fsc scripts for correlation"""

        # Template
        template_lines = [
            "{callsign} FLIGHTRULES IFR",
            "{callsign} FLIGHTTYPE S",
            "{callsign} RNAV YES",
            "{callsign} 833 YES",
            "{callsign} RVSM YES",
            "{callsign} ICAOOTHER CODE/{code:06d}",
            "{callsign} ICAOOTHER REG/{reg:06d}",
        ]

        # Initialize counters for code and reg
        code_counter = 1
        reg_counter = 2

        # Initialize an empty list to store the generated lines
        generated_lines = []

        # Iterate over each callsign
        for callsign in callsigns:
            # Generate each line for the current callsign
            for template_line in template_lines:
                # Replace the placeholder in the line with the callsign and the counters
                line = template_line.format(callsign=callsign, code=code_counter, reg=reg_counter)
                # Add the line to the list of generated lines
                generated_lines.append(line)
            
            # Increment the counters
            code_counter += 2
            reg_counter += 2
        
        return generated_lines
    
    def write_fsc(self, generated_lines, path):
        """Writes the generated fsc lines to file"""
        # Extract base name
        base_name = os.path.splitext(os.path.basename(path))[0]

        # Get the directory of the original file
        directory = os.path.dirname(path)

        # Construct the ouptut file name
        output_file_name = os.path.join(directory, f"{base_name}.fsc")

        # Write the generated lines to the output file
        with open(output_file_name, "w") as output_file:
            for line in generated_lines:
                output_file.write(line + "\n")