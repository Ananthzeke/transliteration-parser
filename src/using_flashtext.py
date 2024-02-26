from flashtext import KeywordProcessor
import regex
import re
from dictionary_loader import DictionaryLoader
from functools import lru_cache
class FlashReplacer:
    def __init__(self,dict_loader):
        self.kw_processor=KeywordProcessor()
        self.dict_loader=dict_loader

    @staticmethod
    def remove_english_words(s):
        # Regular expression pattern to match English words
        pattern = r'[A-Za-z]+'
        # Replace English words with an empty string
        return re.sub(pattern, '', s)   
    
    @staticmethod
    def split_non_romanized_string(text):
        pattern = r'[\p{Z}\p{P}\p{S}\p{N}]+'
        words=[word.strip() for word in regex.split(pattern, text) if FlashReplacer.remove_english_words(word)]
        return words
    
    @staticmethod
    def mixed_words(text):
        """
        Returns a set of words from 'text' that contain English letters but don't match a specified pattern.
        """
        english_pattern = re.compile(r'[A-Za-z]')
        allowed_pattern = re.compile(r'^[a-zA-Z0-9\s.,\'"!?]+$')
        if not isinstance(text, str):
            raise ValueError("Input must be a string.")

        words = text.split(' ')
        filtered_words = {word for word in words 
                        if english_pattern.search(word) and not allowed_pattern.match(word)}
        return filtered_words


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
        org_text_list=org_text.split(' ')
        transliterated_text_list=transliterated_text.split(' ')
        mixed_words=self.mixed_words(transliterated_text)
        text=transliterated_text
        if mixed_words:
            try:
                mixed_to_org_words={word:org_text_list[transliterated_text_list.index(word)] 
                                    for word in mixed_words }
                regex = re.compile("(%s)" % "|".join(map(re.escape, mixed_to_org_words.keys())))
                text=regex.sub(lambda mo: mixed_to_org_words[mo.group()], transliterated_text)
            except Exception as e:
                print('Failed on mixed words replacement ')
                # print(f'mixed_words: {mixed_words}\n')
                # print(f'transliterated_text_list: {transliterated_text_list}\n')
                
        return text

 
    
    def using_flashtext_multi_replace(cls,replacements,text,mode='raw'):
        if mode=='raw':
            for key,value in replacements.items():
                if not isinstance(value,dict):
                    cls.kw_processor.add_keyword(key,value)
                else:
                    print(len(key))

        elif mode=='space':
            for key,value in replacements.items():
                cls.kw_processor.add_keyword(f' {key} ',f' {value} ')
    
        text=cls.kw_processor.replace_keywords(' '+text+' ').strip()
        return text
    
    @lru_cache(maxsize=1024)           
    def get_dict(self,word):
        translated_word = self.dict_loader.get_translated_word(word)
        return translated_word
    
    def replace_chunks_of_text(self,batch,mode='raw',using_placeholder=True):
        replacement_dictionaries={}
        transliterated_batch = batch[:] 

        try:
            unq_words=set(self.split_non_romanized_string(str(batch)))
        except Exception as e:
            raise ValueError(f"Error splitting batch into words: {e}")
        
        for word in unq_words:
            try:
                dct = self.get_dict(word)
                if isinstance(dct, dict):
                    replacement_dictionaries.update(dct)
            except KeyError:
                continue  # Skip words not found in the dictionary
            except Exception as e:
                raise ValueError(f"Error retrieving dictionary for word '{word}': {e}")
        if replacement_dictionaries:
            try:
                if using_placeholder:
                    placeholder='[batch]'
                    transliterated_batch=placeholder.join(transliterated_batch)
                    transliterated_batch=self.using_flashtext_multi_replace(replacement_dictionaries,transliterated_batch,mode=mode)
                    transliterated_batch=transliterated_batch.split(placeholder)
                else:
                    transliterated_batch = [
                        self.using_flashtext_multi_replace(replacement_dictionaries, string, mode=mode)
                        for string in batch
                    ]
            except Exception as e:
                raise ValueError(f"Error replacing words in batch: {e}")
        fixed_batch = [
            self.fix_mixed_words(org_string, transliterated_string)
            for org_string, transliterated_string in zip(batch, transliterated_batch)
        ]

        return fixed_batch
if __name__=='__main__':


    dct_loader= DictionaryLoader('data/tam.json')
    flash=FlashReplacer(dct_loader)
    text='''goopal parathamaின் pinnani matrum thanipatta vaazhkkai patrri melum sollungkal.\n" goopal paratham septumber 9,1935 அன்று singappooril ஒரு marudhuvar thandhai matrum ஒரு seviliyar thaaikகு piranthaar. avarathu ilamai japaniya aakkiramippin anubavaththaal kurikkappattathu. அவர் thanadhu pettroarin adichchuvadugalaip பின்parra mudivu seithu maruththuvath tholilil nuzhinththaar. paratham thanadhu maruththuva vaazhkkai muzhuvathum ezhuthuvathai orupoathum nirutthavillai, melum avarathu muthal sirukadhai, ""diu"", 1974 ஆம் aandil singapure samoogaththin thaesiya palkalaikkazhagaththin veliyeedaana varnanaiyil veliyidappattadhu.\n, thaகு '''
    # print(filter_non_english_numeric_symbols(text))
    text=['''கோபால் பரதமின் பின்னணி மற்றும் தனிப்பட்ட வாழ்க்கை பற்றி மேலும் சொல்லுங்கள்.
" கோபால் பரதம் செப்டம்பர் 9,1935 அன்று சிங்கப்பூரில் ஒரு மருத்துவர் தந்தை மற்றும் ஒரு செவிலியர் தாய்க்கு பிறந்தார். அவரது இளமை ஜப்பானிய ஆக்கிரமிப்பின் அனுபவத்தால் குறிக்கப்பட்டது. அவர் தனது பெற்றோரின் அடிச்சுவடுகளைப் பின்பற்ற முடிவு செய்து மருத்துவத் தொழிலில் நுழைந்தார். பரதம் தனது மருத்துவ வாழ்க்கை முழுவதும் எழுதுவதை ஒருபோதும் நிறுத்தவில்லை, மேலும் அவரது முதல் சிறுகதை, ""தீவு"", 1974 ஆம் ஆண்டில் சிங்கப்பூர் சமூகத்தின் தேசிய பல்கலைக்கழகத்தின் வெளியீடான வர்ணனையில் வெளியிடப்பட்டது.
''',"1974 ஆம் ஆண்டில் சிங்கப்பூர் சமூகத்தின் தேசிய பல்கலைக்கழகத்தின் வெளியீடான வர்ணனையில் வெளியிடப்பட்டது."]
    new_text=flash.replace_chunks_of_text(text,mode='space')
    print(new_text)