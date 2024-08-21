import json
from .utils import (
    extract_text, extract_label, extract_property,
    validate_tpl_header, move_to_tool_data_section
)


class TPLReader:
    """Class for reading and parsing Photoshop TPL files."""

    def __init__(self, file_path):
        self.file_path = file_path
        self.tpl_data = {}

    def read_tool(self, file):
        """
        Reads tool data from the TPL file and extracts relevant properties.

        Parameters:
            file (BinaryIO): The file object of the TPL file to be read.

        Returns:
            dict: A dictionary containing the tool data extracted from the file.
        """
        tpl = {}

        while True:
            # Extract the tool name
            tool_name = extract_text(file)
            # Skip 10 bytes (typically padding or non-essential data)
            file.read(10)

            # Extract the tool type
            tool_type = extract_label(file).decode('ascii', errors='ignore')

            # Initialize the tool type in the dictionary if not already present
            if tool_type not in tpl:
                tpl[tool_type] = []

            # Extract the number of properties and their values
            count = int(file.read(4).hex(), 16)
            properties = [extract_property(file) for _ in range(count)]

            # Append the tool data to the dictionary
            tpl[tool_type].append({
                "name": tool_name.split("=")[-1],
                "properties": properties
            })

            # Check if there are more tools to read
            if len(file.read(4)) != 4:
                break
            file.seek(-4, 1)

        return tpl

    def read_tpl(self):
        """
        Reads and parses the TPL file.

        Returns:
            dict: A dictionary containing the parsed TPL data.
        """
        with open(self.file_path, 'rb') as file:
            # Validate the TPL file header and move the cursor to the tool data section
            if not validate_tpl_header(file) or not move_to_tool_data_section(file):
                return {}

            # Extract the tool data
            self.tpl_data = self.read_tool(file)
        return self.tpl_data

    def save_to_json(self, output_file):
        """
        Saves the parsed TPL data to a JSON file.

        Parameters:
            output_file (str): The path to the JSON file where the data will be saved.
        """
        with open(output_file, "w+", encoding="utf-8") as f:
            json.dump(self.tpl_data, f, indent=2)
