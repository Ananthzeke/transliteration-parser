from datasets import load_from_disk
import json
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
    # Example usage
    input_file_path = '/data/umashankar/transliteration/aksharantar_arrow/tam'
    output_file_path = '/data/umashankar/transliteration/tam.json'
    with open('data/corrected_tamil_transliterated_dict.json','r') as f:
        data=json.load(f)
    json_to_jsonl(data,'data/new_tam.json')
    # ds=load_from_disk(input_file_path)
    # result = ds_to_json(ds, output_file_path)
    # print(result)
