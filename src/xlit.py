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
if __name__ == '__main__':
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Transliterate text using specified method.")
    
    # Add arguments
    parser.add_argument('--input_path', type=str, required=True, help='Input path for the dataset to transliterate.')
    parser.add_argument('--src_lang', type=str, required=True, help='Source language code.')
    parser.add_argument('--batch_size', type=int, default=32, help='Batch size for processing.')
    parser.add_argument('--cache_dir', type=str, default='.cache', help='Cache directory for storing temporary files.')
    parser.add_argument('--output_path', type=str, required=True, help='Output directory for the transliterated dataset.')
    parser.add_argument('--file_name', type=str, required=True, help='File name for the output JSON.')
    parser.add_argument('--using_hugging_face', action='store_true', help='Flag to use Hugging Face for transliteration.')

    # Parse arguments
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_path, exist_ok=True)

    if args.using_hugging_face:
        # Transliterate using Hugging Face
        ds = transliterate_using_hugging_face(
            args.input_path,
            args.src_lang,
            args.batch_size,
            args.cache_dir
        )
        # Save the dataset to JSON
        ds_to_json(ds, f'{args.output_path}/{args.file_name}.json')
    else:
        # Transliterate using a custom mapping function
        ds_dict = map_transliterate_words(args.input_path, args.src_lang)
        # Save the dictionary to JSON
        save_dicts_as_json(f'{args.output_path}/{args.file_name}.json', ds_dict)

        
