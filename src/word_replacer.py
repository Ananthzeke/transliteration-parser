from dictionary_loader import DictionaryLoader 
import re
import regex


class WordReplacer:
    def __init__(self, dictionary_loader):
        """
        Initializes the Word Replacer with a DictionaryLoader instance.

        :param dictionary_loader: An instance of DictionaryLoader.
        """
        self.dictionary_loader = dictionary_loader

    @staticmethod
    def remove_english_words(s):
        # Regular expression pattern to match English words
        pattern = r'[A-Za-z]+'
        # Replace English words with an empty string
        return re.sub(pattern, '', s)
    @staticmethod
    def split_non_romanized_string(text):
        pattern = r'[\p{Z}\p{P}\p{S}\p{N}]+'
        words=[word.strip() for word in regex.split(pattern, text) if WordReplacer.remove_english_words(word)]
        return words
    @staticmethod
    def multiple_replace(replacements, text):
        # Create a regular expression from the dictionary keys
        regex = re.compile("(%s)" % "|".join(map(re.escape, replacements.keys())))
        # For each match, look-up corresponding value in dictionary
        return regex.sub(lambda mo: replacements[mo.group()], text) 

    
    def get_dict(self,word):
        translated_word = self.dictionary_loader.get_translated_word(word)
        return translated_word
    
    def replace_chunks(self,chunk):
        unique_words=list(set(WordReplacer.split_non_romanized_string(chunk)))
        for word in unique_words:
            dct=self.get_dict(word)
            chunk=WordReplacer.multiple_replace(dct,chunk)
        return chunk

if __name__=='__main__':
    a=DictionaryLoader