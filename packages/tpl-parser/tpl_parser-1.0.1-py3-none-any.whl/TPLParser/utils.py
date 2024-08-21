import struct


def extract_label(file):
    """
    Reads a label from the TPL file.

    A label is typically a string with a specified length or a fixed 4-byte identifier.

    Parameters:
        file (BinaryIO): The file object of the TPL file to be read.

    Returns:
        bytes: The label read from the file, which may be a string of variable length or a fixed 4-byte identifier.
    """
    # Read the first 4 bytes to determine the length of the label
    label_length = int(file.read(4).hex(), 16)

    # If the length is zero, read and return the next 4 bytes as the label (fixed identifier)
    if label_length == 0:
        return file.read(4)

    # Otherwise, read and return the number of bytes specified by label_length
    return file.read(label_length)


def extract_property(file):
    """
    Extracts a property from the TPL file.

    This function extracts the label (name) of a property and, if the label is not 'null',
    it extracts and returns the property's value.

    Parameters:
        file (BinaryIO): The file object of the TPL file to be read.

    Returns:
        dict: A dictionary representing the property with its name and value, 
              or an empty dictionary if the label is 'null'.
    """
    # Extract the label (name) of the property
    property_name = extract_label(file)

    # If the property name is not 'null', extract and return the property value
    if property_name != b'null':
        return extract_property_value(file, property_name)

    # If the property name is 'null', return an empty dictionary
    return {}


def extract_property_value(file, property_name):
    """
    Extracts the value of a property based on its type.

    This function reads the property type from the file and then extracts the property's value
    using the appropriate method based on the type.

    Parameters:
        file (BinaryIO): The file object of the TPL file to be read.
        property_name (bytes): The name of the property whose value is to be extracted.

    Returns:
        dict: A dictionary containing the property's name, type, and extracted value.
    """
    # Read the next 4 bytes to determine the property's type
    property_type = file.read(4).decode('ascii', errors='ignore')

    # Extract the property's value based on its type
    property_value = extract_os_type_value(file, property_name.decode('ascii', errors='ignore').strip(), property_type)

    # Return a dictionary with the property's name, type, and value
    return {
        property_value['name']: {
            'type': property_value['os_type'],
            'value': property_value['value']
        }
    }


def extract_os_type_value(file, property_name, property_type):
    """
    Extracts data from the TPL file based on the property's type (os_type).

    Parameters:
        file (BinaryIO): The file object of the TPL file to be read.
        property_name (bytes): The name of the property being extracted.
        property_type (str): The type of the property (os_type).

    Returns:
        dict: A dictionary containing the property's name, type, and extracted value, 
              or None if the type is not recognized or handled.
    """
    type_handlers = {
        'Objc': lambda f: extract_object_class(f, property_name),
        'VlLs': extract_list,
        'doub': extract_double,
        'UntF': extract_unit_float,
        'TEXT': extract_text,
        'enum': extract_enum,
        'long': extract_integer,
        'comp': extract_large_integer,
        'bool': extract_boolean,
    }

    # Check if the property type has a corresponding handler function
    if property_type in type_handlers:
        return {
            'name': property_name,
            'os_type': property_type,
            'value': type_handlers[property_type](file)
        }

    # Handle specific types that are not fully processed
    if property_type in {'type', 'GlbC', 'obj ', 'alis', 'tdta'}:
        return None

    # Handle unknown os_type by attempting to read until a known placeholder is found
    name_found = extract_until_placeholder(
        file,
        property_name + property_type
    )
    new_property_name = name_found[0]
    new_property_type = name_found[1]

    # Recursively call the function with the new name and type
    return extract_os_type_value(file, new_property_name, new_property_type)


def extract_until_placeholder(file, prefix=''):
    """
    Extracts text from the file until one of the predefined placeholders is found.

    This function reads one character at a time, appending to a prefix, and checks for the occurrence
    of any placeholder from a predefined list of placeholders.

    Parameters:
        file (BinaryIO): The file object to read from.
        prefix (str, optional): A prefix to start with when searching for the placeholder.

    Returns:
        list: A list containing the extracted text before the placeholder and the placeholder itself.
    """
    extracted_text = prefix

    # Predefined list of placeholders to search for in the text
    placeholders = ['GlbO', 'Objc', 'VlLs', 'dou', 'UntF', 'TEXT', 'enum', 'long', 'comp', 'bool', 'type', 'GlbC', 'obj ', 'alis', 'tdta']

    while True:
        # Read the next byte from the file and decode it to ASCII, ignoring errors
        extracted_text += file.read(1).decode('ascii', errors='ignore')

        # Check if any of the placeholders match the end of the extracted text
        if any(extracted_text.endswith(placeholder) for placeholder in placeholders):
            placeholder_length = len(placeholders[0])
            return [
                extracted_text[:-placeholder_length],
                extracted_text[-placeholder_length:]
            ]


def extract_object_class(file, name):
    """
    Extracts and processes class (Objc) from the TPL file.

    This function processes a specified number of properties associated with the object class,
    with a special case for the "Grad" object class.

    Parameters:
        file (BinaryIO): The file object of the TPL file to be read.
        name (str): The name of the object class to process.

    Returns:
        list: A list of dictionaries, each representing a property of the object class.
    """
    if name == "Grad":
        # Special case for "Grad" object class: process text and set property count to 4
        extract_text(file)
        property_count = 4
    else:
        # For other object classes, skip 6 bytes, read the label, and determine property count
        file.read(6)
        extract_label(file)
        property_count = int(file.read(4).hex(), 16)

    # Extract the properties based on the determined property count
    properties = [extract_property(file) for _ in range(property_count)]

    return properties


def extract_text(file):
    """
    Extracts and processes text from the TPL file.

    This function reads a length-prefixed text block, handles edge cases where the length is zero,
    and decodes the text into a readable ASCII string.

    Parameters:
        file (BinaryIO): The file object of the TPL file to be read.

    Returns:
        str: The extracted and decoded text string.
    """
    length = int(file.read(4).hex(), 16)

    while length == 0:
        # Seek back 4 bytes and try reading the property again
        file.seek(-4, 1)
        extract_property(file)

        # Re-read the length of the text block
        length = int(file.read(4).hex(), 16)

        if length:
            temp_cursor = file.tell()

            # Read the text block as hex and count null bytes
            text_hex = file.read(length * 2).hex()
            num_zeros = text_hex.count('00')

            # Seek back to the original position
            file.seek(temp_cursor)

            # Break if the number of null bytes indicates an end of the text block
            if num_zeros == length + 1:
                break

            # Reset length to zero to continue the loop
            length = 0

    # Read and decode the final text block
    text_hex = file.read(length * 2).hex()
    return bytes.fromhex(text_hex).decode('ascii', errors='ignore').replace('\x00', '')


def extract_boolean(file):
    """
    Extracts a boolean value from the TPL file.

    This function reads a single byte from the file, converts it to an integer, 
    and then returns its boolean equivalent.

    Parameters:
        file (BinaryIO): The file object of the TPL file to be read.

    Returns:
        bool: The boolean value extracted from the file.
    """
    # Read a single byte, convert it to an integer, and then to a boolean
    return bool(int(file.read(1).hex(), 16))


def extract_enum(file):
    """
    Extracts an enumeration value from the TPL file.

    This function reads the class ID and value of an enum, ensuring a minimum length of 4 bytes,
    and returns them as a dictionary.

    Parameters:
        file (BinaryIO): The file object of the TPL file to be read.

    Returns:
        dict: A dictionary containing the 'classId' and 'value' of the enum, both decoded to ASCII.
    """
    # Read and ensure the class ID length is at least 4 bytes
    class_id_length = int(file.read(4).hex(), 16)
    if class_id_length == 0:
        class_id_length = 4
    class_id = file.read(class_id_length)

    # Read and ensure the value length is at least 4 bytes
    value_length = int(file.read(4).hex(), 16)
    if value_length == 0:
        value_length = 4
    value = file.read(value_length)

    # Return the class ID and value as a dictionary, both decoded to ASCII
    return {
        'classId': class_id.decode('ascii', errors='ignore'),
        'value': value.decode('ascii', errors='ignore')
    }


def extract_double(file):
    """
    Extracts a double-precision floating-point number from the TPL file.

    This function reads 8 bytes from the file and unpacks them as a double-precision
    floating-point number using big-endian format.

    Parameters:
        file (BinaryIO): The file object of the TPL file to be read.

    Returns:
        float: The extracted double-precision floating-point number.
    """
    # Read 8 bytes and unpack them as a double-precision float in big-endian format
    return struct.unpack('>d', file.read(8))[0]


def extract_unit_float(file):
    """
    Extracts a unit float value from the TPL file.

    This function reads a unit identifier (as a 4-byte ASCII string) and a double-precision
    floating-point value (8 bytes) from the file, then returns them as a dictionary.

    Parameters:
        file (BinaryIO): The file object of the TPL file to be read.

    Returns:
        dict: A dictionary containing the 'unit' (as an ASCII string) and 'value' (as a float).
    """
    # Read the 4-byte unit identifier and decode it to an ASCII string
    unit = file.read(4).decode('ascii', errors='ignore')

    # Read the next 8 bytes and unpack them as a double-precision float in big-endian format
    value = struct.unpack('>d', file.read(8))[0]

    # Return the unit and value as a dictionary
    return {
        'unit': unit,
        'value': value
    }


def extract_integer(file):
    """
    Extracts a 4-byte integer from the TPL file.

    This function reads 4 bytes from the file, interprets them as a hexadecimal string,
    and converts the result to an integer.

    Parameters:
        file (BinaryIO): The file object of the TPL file to be read.

    Returns:
        int: The extracted integer value.
    """
    return int(file.read(4).hex(), 16)


def extract_large_integer(file):
    """
    Extracts an 8-byte large integer from the TPL file.

    This function reads 8 bytes from the file, interprets them as a hexadecimal string,
    and converts the result to a large integer.

    Parameters:
        file (BinaryIO): The file object of the TPL file to be read.

    Returns:
        int: The extracted large integer value.
    """
    return int(file.read(8).hex(), 16)


def extract_list(file):
    """
    Extracts a list of properties from the TPL file.

    This function reads the number of properties (count) from the file,
    then reads and returns each property as a dictionary.

    Parameters:
        file (BinaryIO): The file object of the TPL file to be read.

    Returns:
        list: A list of dictionaries, each representing a property.
    """
    count = int(file.read(4).hex(), 16)
    properties = []
    for i in range(count):
        i_as_bytes = str(i).encode('ascii', errors='ignore')
        properties.append(extract_property_value(file, i_as_bytes)[str(i)])
    return properties


def extract_class(file):
    """
    Extracts a class label from the TPL file.

    This function reads and returns a label, which typically represents a class name or identifier.

    Parameters:
        file (BinaryIO): The file object of the TPL file to be read.

    Returns:
        bytes: The extracted label.
    """
    return extract_label(file)


def validate_tpl_header(file):
    """
    Validates the TPL file header to ensure it is a valid Photoshop TPL file.

    Parameters:
        file (BinaryIO): The file object of the TPL file to be read.

    Returns:
        bool: True if the file header is valid, False otherwise.
    """
    # Read the first 4 bytes of the file and check if it matches the TPL identifier '8BTP'
    header_signature = file.read(4)
    if header_signature.lower() != b'8btp':
        return False  # If it doesn't match, the file is not a valid TPL file

    # Skip the next 8 bytes (typically padding or non-essential data)
    file.read(8)

    # Read the next 4 bytes and check if it matches the Photoshop identifier '8BIM'
    photoshop_signature = file.read(4)
    if photoshop_signature.lower() != b'8bim':
        return False  # If it doesn't match, the file is not a valid Photoshop TPL file
    # Seek back to the old position
    file.seek(0)

    # If both signatures are correct, return True indicating the file is valid
    return True


def move_to_tool_data_section(file):
    """
    Moves the file cursor to the start of the tool data section in the TPL file.

    Parameters:
        file (BinaryIO): The file object of the TPL file to be read.

    Returns:
        bool: True if the cursor was successfully moved, False otherwise.
    """
    # Read the entire file content into memory
    file_content = file.read()
    
    # The signature that indicates the start of the tool data section
    tool_data_signature = "8BIMtptp".encode('ascii')

    # Find the last occurrence of the tool data signature in the file content
    last_occurrence_pos = file_content.rfind(tool_data_signature)

    # If the signature is found, move the file cursor to the start of the tool data section
    if last_occurrence_pos != -1:
        # Move the cursor 8 bytes forward from the signature to the start of the tool data
        file.seek(last_occurrence_pos + 8)

        # Read 8 bytes to potentially position the cursor correctly within the section
        file.read(8)
        return True

    # If the signature is not found, return False indicating failure
    return False
