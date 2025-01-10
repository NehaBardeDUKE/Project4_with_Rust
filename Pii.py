import os
import json
import csv

# Function to recursively get all JSON files in a directory
def get_json_files(directory):
    json_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    return json_files

# Function to extract function_name values where pii is True
def extract_function_names(json_files):
    function_names = []
    for file_path in json_files:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                # Assuming each JSON file is a dictionary
                if isinstance(data, dict):
                    function_name = data.get("function_name")
                    pii = data.get("pii")
                    if pii is True and function_name:
                        function_names.append(function_name)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    return function_names

# Function to save the extracted function names to a CSV
def save_to_csv(function_names, output_file):
    with open(output_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["function_name"])
        for name in function_names:
            writer.writerow([name])

# Main script
if __name__ == "__main__":
    # Replace 'your_directory' with your target directory
    directory = "your_directory"
    output_csv = "output.csv"

    json_files = get_json_files(directory)
    function_names = extract_function_names(json_files)
    save_to_csv(function_names, output_csv)

    print(f"CSV file saved as {output_csv}")
