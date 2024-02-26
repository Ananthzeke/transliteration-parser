import json
import string

def clean_and_remove_duplicates(input_dict):
    """
    Cleans symbols, punctuation, single quotes, and double quotes from keys and values
    of the input dictionary. Removes key-value pairs where the key is the same as the
    value after cleaning.
    """
    extended_punctuation = string.punctuation + '"' + "'"

    def remove_punctuation(s):
        return s.strip(extended_punctuation)

    cleaned_dict = {}
    for key, value in input_dict.items():
        cleaned_key = remove_punctuation(key)
        cleaned_value = remove_punctuation(value)
        if cleaned_key != cleaned_value:
            cleaned_dict[cleaned_key] = cleaned_value

    return cleaned_dict

def read_json_file_as_dict(file_path):
    """
    Reads a JSON file from the given file path and converts it into a dictionary.
    
    Parameters:
    - file_path: Path to the JSON file to be read.
    
    Returns:
    - A dictionary representation of the JSON content if successful, or an error message if an exception occurs.
    """
    try:
        with open(file_path, 'r') as json_file:
            dict_data = json.load(json_file)
        return dict_data
    except Exception as e:
        return f"Error reading JSON file: {e}"

    
def write_dict_as_json(dict_data, file_path):
    """
    Writes the given dictionary to a file as JSON.
    
    Parameters:
    - dict_data: Dictionary to be written as JSON.
    - file_path: Path to the file where the JSON should be written.
    
    Returns:
    - A success message with the file path, or an error message.
    """
    try:
        with open(file_path, 'w') as json_file:
            json.dump(dict_data, json_file, indent=4,ensure_ascii=False)
        return f"Dictionary successfully written to {file_path}"
    except Exception as e:
        return f"Error writing dictionary to JSON: {e}"


if __name__ == "__main__":
    # Example for cleaning and removing duplicates
    dict_from_json = read_json_file_as_dict('../data/corrected_tamil_transliterated_dict.json')
    cleaned_dict = clean_and_remove_duplicates(dict_from_json)
    write_dict_as_json(cleaned_dict,'../data/cleaned.json')

