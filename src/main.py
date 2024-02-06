import argparse
import glob
from dictionary_loader import DictionaryLoader
from word_replacer import WordReplacer
from datasets import load_dataset,disable_caching
# disable_caching()

def apply_map(ds, column='translated', num_proc=4, batch_size=16):
    ds = ds.map(
        lambda x: {column:x[column],'transliterated': wrd_replacer.replace_chunks(x[column])},
        num_proc=num_proc,
        batched=True,
        batch_size=batch_size,
        remove_columns=ds.column_names
    )
    return ds

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process dataset for transliteration.')
    parser.add_argument('--dictionary_path', type=str, required=True, help='Path to the dictionary JSON file.')
    parser.add_argument('--cache_dir', type=str, default=None,required=True, help='Cache directory for storing temporary files.')
    parser.add_argument('--dataset_path', type=str, required=True, help='Glob path for dataset files.')
    parser.add_argument('--column', type=str, default='translated', help='Column to be processed.')
    parser.add_argument('--num_proc', type=int, default=4, help='Number of processes to use.')
    parser.add_argument('--batch_size', type=int, default=16, help='Batch size for processing.')
    parser.add_argument('--sample_size', type=int, help='Sample size to select from dataset.')
    parser.add_argument('--output_path', type=str, required=True, help='Output path for the processed dataset.')

    args = parser.parse_args()

    dictionary_path = args.dictionary_path
    cache_dir = args.cache_dir
    dataset_path = glob.glob(args.dataset_path)
    column = args.column
    num_proc = args.num_proc
    batch_size = args.batch_size
    sample_size = args.sample_size
    output_path = args.output_path

    dct_loader = DictionaryLoader(dictionary_path)
    wrd_replacer = WordReplacer(dct_loader)

    ds = load_dataset(
        'arrow',
        data_files=dataset_path,
        cache_dir=cache_dir
    )

    if sample_size:
        ds = ds['train'].select(range(sample_size))
    else:
        ds=ds['train']

    new_ds = apply_map(ds, column, num_proc, batch_size)

    new_ds.to_csv('new.csv')
    # new_ds.save_to_disk(output_path,num_proc=num_proc)

