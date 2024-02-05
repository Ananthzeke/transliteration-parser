from dictionary_loader import DictionaryLoader
from word_replacer import WordReplacer
from datasets import load_dataset
import glob

# if __name__=='_main':
dct_loader=DictionaryLoader('../data/tam.json')
wrd_replacer=WordReplacer(dct_loader)

ds=load_dataset(
    'arrow',
    data_files=glob.glob('../data/tam/*')
)

def apply_map(ds,column='translated'):
    ds=ds.map(
        lambda x : {column:wrd_replacer.replace_chunks(x[column].strip())},
        num_proc=4,
        remove_columns=ds.features
    )
    return ds

ds=ds['train'].select(range(1000))
# ds.to_csv('old.csv')
new_ds=apply_map(ds)

new_ds.to_csv('new.csv')

