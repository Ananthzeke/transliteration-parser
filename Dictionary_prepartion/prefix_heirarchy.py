from datasets import load_from_disk
import json
import argparse

def create_prefix_hierarchy(dictionary, prefix_length):
    root = {}
    for word, transliteration in dictionary.items():
            prefix = word[:prefix_length]
            if prefix not in root:
                root[prefix] = {}
            root[prefix][word] = transliteration
    return root


def ds_to_json(ds,prefix=4):
    # Convert to Pandas DataFrame
    df = ds['train'].to_pandas()
    
    # Ensure the columns are named correctly
    if 'native word' not in df.columns or 'english word' not in df.columns:
        raise ValueError("Expected columns 'native word' and 'english word' not found")

    # Convert the DataFrame to a dictionary
    dictionary = df.set_index('native word')['english word'].to_dict()
    dictionary=create_prefix_hierarchy(dictionary,prefix)
    return dictionary
    
    # Convert the dictionary to a JSON string and save to a file
def json_to_jsonl(dictionary,output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for key,value in dictionary.items():
            json.dump({key:value}, f, ensure_ascii=False)
            f.write('\n')
            # f.write('{"' + str(key) + '": "' + str(value) + '"}\n')

    return f"JSON file saved to {output_file_path}"



if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Dictionary preparation for transliteration.')
    parser.add_argument('--path_to_raw_dictionary', type=str, required=True, help='Path to the dictionary  file.')
    parser.add_argument('--path_to_save_processed_dictionary', type=str, required=True, help='Output path  to the dictionary  file.')
    parser.add_argument('--file_type', type=str, required=True,choices=['json','arrow'])
    
    args = parser.parse_args()
    file_type=args.file_type
    input_file_path = args.path_to_raw_dictionary
    output_file_path = args.path_to_save_processed_dictionary
    if file_type=='json':
        with open('data/corrected_tamil_transliterated_dict.json','r') as f:
            data=json.load(f)
        json_to_jsonl(data, output_file_path)
    elif file_type=='arrow':
        ds=load_from_disk(input_file_path)
        data = ds_to_json(ds)
        json_to_jsonl(data, output_file_path)
    else:
        print('Invalid file format')
