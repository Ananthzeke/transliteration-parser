import re
import regex
import json
class MemoryWordReplacer:
    def __init__(self,dictionary:dict):
        self.dictionary=dictionary
        self.english_pattern=re.compile(r'[A-Za-z]+')
        self.non_romanized_pattern = regex.compile(r'[\p{Z}\p{P}\p{S}\p{N}]+')
        self.mixed_word_pattern = re.compile(r'[A-Za-z]')
        self.allowed_mixed_word_pattern = re.compile(r'^[a-zA-Z0-9\s.,\'"!?]+$')

    def remove_english_words(self,s):
        return self.english_pattern.sub('', s)
    
    def split_non_romanized_string(self, text):
            words = [word.strip() for word in self.non_romanized_pattern.split(text) if self.remove_english_words(word)]
            return words
    
    def mixed_words(self, text):
            if not isinstance(text, str):
                raise ValueError("Input must be a string.")
            words = text.split(' ')
            return {
                word for word in words if self.mixed_word_pattern.search(word) and not self.allowed_mixed_word_pattern.match(word)}
    
    def fix_mixed_words(self,org_text,transliterated_text):
        """
        Replaces words in transliterated_text with their original counterparts from org_text
        based on the criteria defined by mixed_words().
        
        Parameters:
        - org_text: The original text.
        - transliterated_text: The transliterated version of the text.
        
        Returns:
        A string where specific words identified by mixed_words() in transliterated_text
        are replaced with their counterparts from org_text.
        """
        org_text_list = org_text.split(' ')
        transliterated_text_list = transliterated_text.split(' ')
        mixed_words = self.mixed_words(transliterated_text)
        if mixed_words:
            try:
                mixed_to_org_words = {word: org_text_list[transliterated_text_list.index(word)] for word in mixed_words}
                return re.sub("|".join(map(re.escape, mixed_to_org_words.keys())), lambda mo: mixed_to_org_words[mo.group()], transliterated_text)
            except Exception as e:
                print('Failed on mixed words replacement')
        return transliterated_text
 

    @staticmethod
    def multiple_replace(replacements, text):

        # Create a regular expression from the dictionary keys with spaces
        regex = re.compile("(%s)" % "|".join(map(re.escape, replacements.keys())))
        
        # For each match, look-up corresponding value in dictionary with spaces included

        text=regex.sub(lambda mo: replacements[mo.group()], text)
        
        return text
    

    def replace_batches(self,batch,use_placeholder=True):

        if not self.dictionary=={}:

            if use_placeholder:
                placeholder='[batch]'
                text=placeholder.join(batch)
                transliterated_text=self.multiple_replace(self.dictionary,text)
                transliterated_batch=transliterated_text.split(placeholder)
            else:
                transliterated_batch=[self.multiple_replace(self.dictionary,text) for text in batch]

        
            fixed_batch = [
                    self.fix_mixed_words(org_string, transliterated_string)
                    for org_string, transliterated_string in zip(batch, transliterated_batch)
                ]
            
            missing_words=[self.split_non_romanized_string(text) for text in fixed_batch ]
            return fixed_batch,missing_words
        else:
            print(f'Dictionary is None')    
            return batch,None

def load_json_as_dict(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("The file was not found.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
if __name__=='__main__':
    a=MemoryWordReplacer({'கோபால்':'gopal','மற்றும்':'matrum','பட்ட':'patta'})
    text=['''கோபால் பரதமின் பின்னணி மற்றும் தனிப்பட்ட வாழ்க்கை பற்றி மேலும் சொல்லுங்கள்.
" கோபால் பரதம் செப்டம்பர் 9,1935 அன்று சிங்கப்பூரில் ஒரு மருத்துவர் தந்தை மற்றும் ஒரு செவிலியர் தாய்க்கு பிறந்தார். அவரது இளமை ஜப்பானிய ஆக்கிரமிப்பின் அனுபவத்தால் குறிக்கப்பட்டது. அவர் தனது பெற்றோரின் அடிச்சுவடுகளைப் பின்பற்ற முடிவு செய்து மருத்துவத் தொழிலில் நுழைந்தார். பரதம் தனது மருத்துவ வாழ்க்கை முழுவதும் எழுதுவதை ஒருபோதும் நிறுத்தவில்லை, மேலும் அவரது முதல் சிறுகதை, ""தீவு"", 1974 ஆம் ஆண்டில் சிங்கப்பூர் சமூகத்தின் தேசிய பல்கலைக்கழகத்தின் வெளியீடான வர்ணனையில் வெளியிடப்பட்டது.
''',"1974 ஆம் ஆண்டில் சிங்கப்பூர் சமூகத்தின் தேசிய பல்கலைக்கழகத்தின் வெளியீடான வர்ணனையில் வெளியிடப்பட்டது."]
    new_text=a.replace_batches(text)
    print(new_text)