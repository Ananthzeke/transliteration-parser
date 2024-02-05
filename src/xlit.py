import os
import json
import glob
from datasets import load_dataset,Dataset
from ai4bharat.transliteration import XlitEngine
from data_prepartion.prefix_heirarchy import ds_to_json


engine =  XlitEngine( beam_width=4, src_script_type = "indic")

def yield_batches_from_file(file_path, batch_size):
    """
    Yields batches of words from a given file where words are separated by newlines.

    :param file_path: Path to the text file.
    :param batch_size: Size of each batch to yield.
    """
    with open(file_path, 'r') as file:
        batch = []  # Initialize an empty list to hold words in the current batch
        for line in file:
            word = line.strip()  # Remove leading/trailing whitespace
            if word:  # Check if the line is not empty
                batch.append(word)
                if len(batch) == batch_size:
                    yield batch
                    batch = []  # Reset the batch list after yielding
        if batch:  # Yield any remaining words as the last batch
            yield batch


def map_transliterate_words(input_path,src_lang,tgt_lang='en',batch_size=64):

    words_map=[]
    batch_gen=yield_batches_from_file(input_path,batch_size)

    for batch in batch_gen:
        transliterated_words=engine.batch_transliterate_words(batch,src_lang,tgt_lang,topk=1)
        words_map.extend(dict(zip(batch,transliterated_words)))

    return words_map


def save_dicts_as_json(file_path, dict_list):

    # Try to open the file at file_path in write mode and save the dict_list as JSON
    try:
        with open(file_path, 'w') as file:
            json.dump(dict_list, file, indent=4,ensure_ascii=False)  
        print(f"File successfully saved at {file_path}")
    except Exception as e:
        print(f"Error saving file: {e}")

def transliterate_using_hugging_face(input_path,src_lang,batch_size,cache_dir):
    
    ds=load_dataset(
        'text',
        data_files={'text':glob.glob(f'{input_path}/*')},
        cache_dir=cache_dir
    )

    #de-dup

    ds=Dataset.from_dict(ds.unique('text'))

    ds=ds.map(
        lambda x: {'transliterated':engine.batch_transliterate_words(
            x['text'],
            src_lang=src_lang,
            tgt_lang='en',
            topk=1
        )},
        batched=True,
        batch_size=batch_size
    )

    return ds

if __name__=='__main__':
    input_path=...
    src_lang=...
    batch_size=...
    cache_dir=...
    output_path=...
    file_name=...
    os.makedirs(output_path,exist_ok=True)

    if using_hugging_face:

        ds=transliterate_using_hugging_face(
            input_path,
            src_lang,
            batch_size,
            cache_dir
        )

        ds_to_json(ds,f'{output_path}/{file_name}.json')
    else:
        ds_dict=map_transliterate_words(input_path,src_lang)
        save_dicts_as_json(f'{output_path}/{file_name}.json',dict_list)

        
