# Author: Tobechi Onubogu 
#
# ECE 4514: Cleaning Jailbroken Output

import os


def reverse_substitution(text):
    reverse_map = {
        '@': 'a',
        '$': 's', '5': 's',
        '3': 'e',
        '1': 'i',
        '0': 'o',
        '9': 'g'
    }
    result = []
    for char in text:
        lower = char.lower()
        result.append(reverse_map.get(lower, lower))
    return "".join(result)

# GUYSSSS PUT NAME HERE
input_file = "Test1Unfiltered.txt"  
output_file = "output.txt"

try:
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        print(f"Current directory: {os.getcwd()}")
        print("Files in current directory:")
        for file in os.listdir("."):
            print(f"  {file}")
    else:
        # Read the file
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()
        print(f"Successfully read {input_file} ({len(text)} characters)")
        
        # Clean the text
        cleaned = reverse_substitution(text)
        print(f"Text cleaned")
        
        # Write the output
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(cleaned)
        print(f"Successfully wrote {output_file}")
        
        # Verify the output file was created
        if os.path.exists(output_file):
            output_size = os.path.getsize(output_file)
            print(f"Output file confirmed: {output_size} bytes")
            
            # Show a preview
            print("\nFirst 100 characters of cleaned text:")
            print(cleaned[:100] + "..." if len(cleaned) > 100 else cleaned)
        else:
            print("Output file was not created!")

except FileNotFoundError:
    print(f"Could not find {input_file}")
except PermissionError:
    print(f" Permission denied - can't read/write files")
except Exception as e:
    print(f" Unexpected error: {e}")
