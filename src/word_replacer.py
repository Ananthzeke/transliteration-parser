import re
import ast
import regex

class WordReplacer:
    def __init__(self, dictionary_loader):
        """
        Initializes the Word Replacer with a DictionaryLoader instance.

        :param dictionary_loader: An instance of DictionaryLoader.
        """
        self.dictionary_loader = dictionary_loader

        self.script_pattern= {
            'Bengali': r'\u0980-\u09FF',
            'Devanagari': r'\u0900-\u097F',
            'Gujarati': r'\u0A80-\u0AFF',
            'Gurmukhi': r'\u0A00-\u0A7F',
            'Kannada': r'\u0C80-\u0CFF',
            'Malayalam': r'\u0D00-\u0D7F',
            'Oriya': r'\u0B00-\u0B7F',
            'Tamil': r'\u0B80-\u0BFF',
            'Telugu': r'\u0C00-\u0C7F',
            'English': r'a-zA-Z'
            }

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
    def merge_dictionaries(d1, d2):
        d3 = {}
        
        for key1, value1 in d1.items():
            for key2, value2 in d2.items():
                if value1 == value2:
                    d3[key1] = key2
                    break  # Break the inner loop once the matching value is found
        return d3
    
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

    def find_indic(self,word):
        pattern = r'[\u0900-\u097F\u0980-\u09FF\u0A00-\u0A7F\u0A80-\u0AFF\u0B00-\u0B7F\u0B80-\u0BFF\u0C00-\u0C7F\u0C80-\u0CFF\u0D00-\u0D7F\u0D80-\u0DFF\u0E00-\u0E7F\u0F00-\u0FFF]'
        try:
            match=re.search(pattern,word)
            word_index = match.start()
            if len(word[:word_index])< len(word)//2:
                return 'prefix'
            else:
                return 'suffix'
        except Exception as e:
            print(f'There is no pattern')


    
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
    def extract_and_clean_mixed_script_words(text, script_ranges):
        # Extract potential mixed-script words using the previously defined logic
        potential_mixed_words = re.findall(rf'[\w{"".join(script_ranges.values())}]+', text)
        
        # Initialize a dictionary to store mixed words and their cleaned English versions
        cleaned_words = {}
        
        # Filter for mixed-script words and clean them
        for word in potential_mixed_words:
            if any(re.search(f'[{range}]', word) for name, range in script_ranges.items() if name != 'English') and re.search('[a-zA-Z]', word):
                # Clean the word by removing non-English characters
                cleaned_word = re.sub(r'[^a-zA-Z]', '', word)
                # Add the original mixed word and its cleaned version to the dictionary
                cleaned_words[word] = cleaned_word
        
        return cleaned_words


    @staticmethod
    def multiple_replace(replacements, text,mode):

        if mode.lower()=='correction':
            new_replacements=replacements
        if mode.lower()=='normal':
            text_list=WordReplacer.split_non_romanized_string(text)
            new_replacements=WordReplacer.filter_and_sort_dict(text_list,replacements)
        
        # Create a regular expression from the dictionary keys with spaces
        regex = re.compile("(%s)" % "|".join(map(re.escape, new_replacements.keys())))
        
        # For each match, look-up corresponding value in dictionary with spaces included

        text=regex.sub(lambda mo: new_replacements[mo.group()], text)

        text=WordReplacer.replace_words_with_symbols(text,new_replacements)
        
        return text
    

    def replace_mixed_words(self, replacements, text):
        try:
            # Attempt to extract and clean mixed-script words
            try:
                mixed_word_dict = self.extract_and_clean_mixed_script_words(text, self.script_pattern)
            except Exception as e:
                raise ValueError(f"Error extracting/cleaning mixed-script words: {e}")
            
            # Proceed only if mixed_word_dict is not empty
            if mixed_word_dict:
                try:
                    correction_dict = self.merge_dictionaries(mixed_word_dict, replacements)
                except Exception as e:
                    raise ValueError(f"Error merging dictionaries: {e}")
                
                # Perform replacements if correction_dict is not empty
                if correction_dict:

                    correction_dict = {
                        key: self.remove_english_words(key) + value if self.find_indic(key) == 'prefix' else value + self.remove_english_words(key)
                        for key, value in correction_dict.items()
                    }

                    try:
                        return self.multiple_replace(correction_dict, text, mode='correction')
                    except Exception as e:
                        raise ValueError(f"Error performing replacements: {e}")
            
            # Return the original text if no replacements were made
            return text
        except Exception as e:
            # Handle unexpected errors
            print(f"An unexpected error occurred during replace_mixed_words: {e}")
            # Optionally, return the original text or handle the error as appropriate
            return text


    def get_dict(self,word):
        translated_word = self.dictionary_loader.get_translated_word(word)
        # if isinstance(ast.literal_eval(translated_word.values()),dict):
        #     translated_word=ast.literal_eval(translated_word.values())
        return translated_word
    
    def replace_chunks(self, chunk):
        try:
            # Check if chunk is a list and convert to string if necessary
            if isinstance(chunk, list):
                chunk = str(chunk)
            
            # Generate a list of unique words
            try:
                unique_words = list(set(self.split_non_romanized_string(chunk)))
            except Exception as e:
                raise ValueError(f"Error splitting chunk into words: {e}")
            
            # Iterate over unique words for replacements
            for word in unique_words:
                try:
                    dct = self.get_dict(word)
                except KeyError:
                    continue  # Skip words not found in the dictionary
                except Exception as e:
                    raise ValueError(f"Error retrieving dictionary for word '{word}': {e}")
                
                if isinstance(dct, dict):
                    try:
                        chunk = self.multiple_replace(dct, chunk, mode='normal')
                        chunk = self.replace_mixed_words(dct, chunk)
                    except Exception as e:
                        raise ValueError(f"Error replacing words in chunk: {e}")
            
            # Convert chunk back to its original format if applicable
            try:
                if isinstance(chunk, (str, dict)):
                    chunk = ast.literal_eval(chunk)
            except ValueError as e:
                raise ValueError(f"Error converting chunk back to original format: {e}")
            except SyntaxError as e:
                print(chunk)
                raise SyntaxError(f"Invalid syntax in chunk for literal evaluation: {e}")
            
            return chunk
        except Exception as e:
            # Handle unexpected errors
            print(f"An unexpected error occurred: {e}")
            # Optionally, return the original chunk or handle the error as appropriate
            return chunk

if __name__=='__main__':
    a=WordReplacer('s')
    print(a.find_indic('therivikkirathத'))