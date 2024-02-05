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
    def replace_words_with_symbols(text, replacements):
        # Ensure pattern matches complete words with word boundaries in Unicode strings
        pattern = r'\b(' + '|'.join(re.escape(key) for key in replacements.keys()) + r')\b'

        def repl(match):
            # Fetch the replacement value from the dictionary
            return replacements[match.group(0)]

        # Adjusted pattern to handle non-ASCII character word boundaries
        pattern = r'(?<!\w)(' + '|'.join(re.escape(key) for key in replacements.keys()) + r')(?!\w)'
        return re.sub(pattern, repl, text)
    
    @staticmethod
    def filter_and_sort_dict(input_list, input_dict):
        # Filter the dictionary by keys present in the input list
        filtered_dict = {key: input_dict[key] for key in input_list if key in input_dict}
        
        # Sort the filtered dictionary by the length of its values
        sorted_filtered_dict = dict(sorted(filtered_dict.items(), key=lambda item: len(str(item[1]))))
        if not sorted_filtered_dict:
            return {'':''}
        
        return sorted_filtered_dict
        
    @staticmethod
    def multiple_replace(replacements, text):
        # Add trailing spaces to each key in the dictionary
        # spaced_replacements = {f" {key} ": f" {value} " for key, value in replacements.items()}
        text_list=WordReplacer.split_non_romanized_string(text)
        new_replacements=WordReplacer.filter_and_sort_dict(text_list,replacements)
        
        # Create a regular expression from the dictionary keys with spaces
        regex = re.compile("(%s)" % "|".join(map(re.escape, new_replacements.keys())))
        
        # For each match, look-up corresponding value in dictionary with spaces included

        text=regex.sub(lambda mo: new_replacements[mo.group()], text)

        text=WordReplacer.replace_words_with_symbols(text,new_replacements)
        
        return text


    def get_dict(self,word):
        translated_word = self.dictionary_loader.get_translated_word(word)
        return translated_word
    
    def replace_chunks(self,chunk):
        unique_words=list(set(WordReplacer.split_non_romanized_string(chunk)))
        for word in unique_words:
            dct=self.get_dict(word)
            if isinstance(dct,dict) :
                chunk=WordReplacer.multiple_replace(dct,chunk)
        return chunk

if __name__=='__main__':
    pass