import re
import regex
import json
import pandas as pd 
from flashtext import KeywordProcessor

class MemoryWordReplacer:
    def __init__(self,dictionary:dict,src_lang:str):
        self.dictionary=cleaned_dict = {key: value for key, value in dictionary.items() if value is not None and not isinstance(value, list)}
        self.kw_processor=KeywordProcessor()
        [self.kw_processor.add_keyword(key,value) for key,value in self.dictionary.items()]
        self.english_pattern=re.compile(r'[A-Za-z+]')
        self.non_romanized_pattern = regex.compile(r'[\p{Z}\p{P}\p{S}\p{N}]+')
        self.mixed_word_pattern = re.compile(r'[A-Za-z]')
        self.allowed_mixed_word_pattern = re.compile(r'^[a-zA-Z0-9\s.,\'"!?]+$')
        self.regex_replacer=re.compile(r'(?<!\w)(' + '|'.join(re.escape(key) for key in self.dictionary.keys()) + r')(?!\w)')
        self.src_lang=src_lang
        self.indic_script_patterns={
        "Arab": re.compile(r"[\u0600-\u06FF]"),
        "Beng": re.compile(r"[\u0980-\u09FF]"),
        "Deva": re.compile(r"[\u0900-\u097F]"),
        "Guru": re.compile(r"[\u0A00-\u0A7F]"),
        "Gujr": re.compile(r"[\u0A80-\u0AFF]"),
        "Orya": re.compile(r"[\u0B00-\u0B7F]"),
        "Taml": re.compile(r"[\u0B80-\u0BFF]"),
        "Telu": re.compile(r"[\u0C00-\u0C7F]"),
        "Knda": re.compile(r"[\u0C80-\u0CFF]"),
        "Mlym": re.compile(r"[\u0D00-\u0D7F]"),
    }

    def remove_english_words(self,s):
        return self.english_pattern.sub('', s)
        
    def remove_english_words_and_empty_strings(self,words):
        pattern = re.compile(r'^[a-zA-Z]+$')
        filtered_words = [word for word in words if not pattern.match(word) and word.strip()]
        return filtered_words

    def split_non_romanized_string(self, text):
            words = [word.strip() for word in self.non_romanized_pattern.split(text) if self.remove_english_words(word)]
            return words
            
    def extract_script_words(self, sentence):
        script_name=self.src_lang.split('_')[1]
        if script_name not in self.indic_script_patterns:
            print (f"Script name '{script_name}' is not supported.")
        pattern = self.indic_script_patterns[script_name]
        # Split the sentence into words and filter those that contain characters matching the script's pattern
        words = [word for word in sentence.split() if pattern.search(word)]
        return words

    
    def mixed_words(self,text):
        if not isinstance(text, str):
            raise ValueError("Input must be a string.")
        return {
            word for word in  self.extract_script_words(text) 
            if bool(self.english_pattern.search(word)) 
        }
    
    # def fix_mixed_words(self,org_text,transliterated_text):
    #     """
    #     Replaces words in transliterated_text with their original counterparts from org_text
    #     based on the criteria defined by mixed_words().
        
    #     Parameters:
    #     - org_text: The original text.
    #     - transliterated_text: The transliterated version of the text.
        
    #     Returns:
    #     A string where specific words identified by mixed_words() in transliterated_text
    #     are replaced with their counterparts from org_text.
    #     """
    #     org_text_list = org_text.split(' ')
    #     transliterated_text_list = transliterated_text.split(' ')
    #     mixed_words = self.mixed_words(transliterated_text)
    #     if mixed_words:
    #         try:
    #             word_mapping={key: value for key, value in zip(transliterated_text_list,org_text_list)}
    #             mixed_to_org_words={word:word_mapping[word] for word in mixed_words}
    #             transliterated_text=re.sub("|".join(map(re.escape, mixed_to_org_words.keys())), lambda mo: mixed_to_org_words[mo.group()], transliterated_text)
    #             return self.fix_mixed_words(org_text,transliterated_text)
    #         except Exception as e:
    #             # print(f'{e}')
    #             threshold=4
    #             if len(mixed_words)<=threshold:
    #                 return transliterated_text
    #             else:
    #                 if non_romanized_words:=self.split_non_romanized_string(org_text):
    #                     try:
    #                         small_dict = {word: self.dictionary[word] if word in self.dictionary else word for word in non_romanized_words}
    #                         transliterated_text=re.sub("|".join(map(re.escape, small_dict.keys())), lambda mo: small_dict[mo.group()], transliterated_text)
    #                         return transliterated_text
    #                     except Exception as e:
    #                         # print("Couldnt replace so returning original text")
    #                         return org_text
    #     return transliterated_text

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
                word_mapping={key: value for key, value in zip(transliterated_text_list,org_text_list)}
                mixed_to_org_words={word:word_mapping[word] for word in mixed_words}
                transliterated_text=re.sub("|".join(map(re.escape, mixed_to_org_words.keys())), lambda mo: mixed_to_org_words[mo.group()], transliterated_text)
                return self.fix_mixed_words(org_text,transliterated_text)
            except Exception as e:
                threshold=4
                if len(mixed_words)<=threshold:
                    return transliterated_text
                else:
                    if non_romanized_words:=self.extract_script_words(org_text):
                        try:
                            for word in non_romanized_words:
                                if word in self.dictionary.keys():
                                    transliterated_text=transliterated_text.replace(f' {word} ',f' {self.dictionary[word]} ')
                            return transliterated_text
                        except Exception as e:
                            print(e)
                            # print("Couldnt replace so returning original text")
                            return org_text
        return transliterated_text

    def multiple_replace(self,replacements, text):
        text=f" {text} "
        # Create a regular expression from the dictionary keys with spaces
        try:

            if self.src_lang.split('_')[1] == "Deva":
                # pass
                pattern =  r"।(\s|$)"
                replacement = r" . \1"
                text=re.sub(pattern, replacement, text)
                pattern_universal = r"।"
                replacement = " . "
                text=re.sub(pattern_universal, replacement, text)
            # if self.src_lang.split('_')[1] =="Arab":
            #     pattern_universal = r"।"
            #     replacement = "."
            #     text=re.sub(pattern_universal, replacement, text)
                pass

            text=self.kw_processor.replace_keywords(text)
        except Exception as e:
            print(e,'trying regex replacer')
            text=self.regex_replacer.sub(lambda x: self.dictionary[x.group()], text)
        return text.strip()
    
    def find(self,text):
        pattern = r'\b\w*\d\w*\b'
        # Filter words with at least one number
        words_with_numbers = re.findall(pattern, text)
        # Remove English letters and numbers
        cleaned_words = [re.sub(r'[a-zA-Z\d]', '', word) for word in words_with_numbers]
        final_list = [word.replace('"','').replace('(','').replace(')','').replace(',','') for word in cleaned_words if word!='']
        return final_list 

    
    def replace_batches(self,batch,use_placeholder=True):
        if self.dictionary not in (None, {}):
            if use_placeholder:
                placeholder=' [batch] '
                text=placeholder.join(batch)
                transliterated_text=self.multiple_replace(self.dictionary,text)
                transliterated_batch=transliterated_text.split(placeholder)
            else:
                transliterated_batch=[self.multiple_replace(self.dictionary,text) for text in batch]

            if transliterated_batch:
                fixed_batch = [
                        self.fix_mixed_words(org_string, transliterated_string)
                        for org_string, transliterated_string in zip(batch, transliterated_batch)
                    ]
                # missing_words=[[].append('') if self.extract_script_words(sent)==[] else self.extract_script_words(sent) 
                # for sent in fixed_batch ]


                refix=''
                untransliterated_words=self.find(placeholder.join(fixed_batch))
                # print(untransliterated_words)
                for word in untransliterated_words:
                    if word in self.dictionary.keys():
                        refix=placeholder.join(fixed_batch).replace(word,self.dictionary[word])
                if refix:
                    fixed_batch=refix.split(placeholder)

                missing_words=[self.extract_script_words(sent) for sent in fixed_batch]
                missing_words_new=[[].append('') if words ==[] else words for words in missing_words ]
                if missing_words:
                    script_name=self.src_lang.split('_')[1]
                    fixed_batch=[self.indic_script_patterns[script_name].sub('',sent) for sent in fixed_batch]
                    # print(fixed_batch)
                return fixed_batch,missing_words_new
            else:
                print('Failed on transliteration returning Orginal text')
                missing_words=[[].append('') if self.extract_script_words(sent)==[] else self.extract_script_words(sent) 
                for sent in batch ]
            return batch, [[]]
        else:
            print(f'Dictionary is None')    
            return batch, [[]]



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

    dictionary=load_json_as_dict('unique_words/tam.json')
    a=MemoryWordReplacer(dictionary,'tam_Taml')
    text=['''முனிச்சிலிருந்து ரோம் வரை நீங்கள் பயணிக்க பல வழிகள் இங்கேஃ

1. விமானப் பயணம் மூலம் முனிக்கிலிருந்து ரோம் வரை பயணிக்க மிகவும் பொதுவான மற்றும் வேகமான வழியாக இருக்கலாம். நீங்கள் எப்போது பறக்கிறீர்கள், உங்கள் டிக்கெட் வகுப்பு மற்றும் உங்கள் டிக்கெட்டுகளை வாங்கும் தேதிக்கு எவ்வளவு நெருக்கமாக இருக்கிறீர்கள் என்பதைப் பொறுத்து, விலை $100 (91 யூரோக்கள்) க்கும் குறைவாக இருந்து $500 (455 யூரோக்கள்) வரை மாறுபடும். நீங்கள் பணத்தை சேமிப்பதை உறுதிசெய்ய உங்கள் பயணத்தைத் திட்டமிட்டு முன்கூட்டியே டிக்கெட்டுகளை வாங்குவதை உறுதிப்படுத்திக் கொள்ளுங்கள். மேலும், முனிச் ஒரு பெரிய விமான நிலையத்தைக் (ம்யூக்) கொண்டிருந்தாலும், ரோம் இரண்டு பெரிய சர்வதேச விமான நிலையங்களைக் (எஃப்சிஓ மற்றும் சிஐஏ) கொண்டுள்ளது. விமான நிலையம், பாதுகாப்பு கோடுகள் மற்றும் சுங்க வரிகளில் நேரத்தைக் கணக்கிடாமல், முனிச்சிலிருந்து ரோம் வரை பயணிக்க விமானத்தில் சுமார் 90 நிமிடங்கள் ஆகும்.

2. ரயில் மூலம்-ரயில் மூலம் பயணம் செய்வது முனிச்சிலிருந்து ரோம் செல்வதற்கான மற்றொரு பொதுவான வழியாகும். விமானத்தை விட அதிக நேரம் எடுக்கும் என்றாலும், டிக்கெட் மிகவும் மலிவானது மற்றும் பயண நாளில் வாங்கப்படலாம். முனிச்சிலிருந்து ரோம் செல்லும் ஒரு வழி ரயில் டிக்கெட் சுமார் $35 (32 யூரோக்கள்) செலவாகும், மேலும் பாதை மற்றும் நிறுத்தங்களின் எண்ணிக்கையைப் பொறுத்து 9-12 மணிநேரங்களுக்கு இடையில் எடுக்கும்.

3. கார் மூலம்-முனிச்சிலிருந்து ரோம் வரை காரில் பயணம் செய்வதும் ஒரு விருப்பமாகும். வரையறுக்கப்பட்ட நிறுத்தங்களுடன், முனிச்சிலிருந்து ரோம் வரை வாகனம் ஓட்ட சுமார் 10 மணி நேரம் ஆகும், ஆனால் ஒரு காரை வைத்திருப்பது நீங்கள் பார்க்க விரும்பும் எந்த நகரங்களிலும் அல்லது தளங்களிலும் நிறுத்த நெகிழ்வுத்தன்மையை அனுமதிக்கும். 

உங்கள் குறிப்பிட்ட தேவைகளைப் பொறுத்து, இந்த மூன்று விருப்பங்களும் முனிச்சிலிருந்து ரோம் வரை பயணிக்க சாத்தியமான வழிகளாக இருக்கலாம்.''']
    new_text=a.replace_batches(text)
    print(new_text)
    # df=pd.DataFrame({'text':text})
    # df=df.replace(dictionary,regex=True)
    # print(df['text'][0])
    # print(a.mixed_words('முனிச்சிலிருந்து ரோம் வரை நீங்கள் பயணிக்க பல வழிகள் இkங்கேஃ '))
    # p=a.mixed_words(''''முனிச்chiiliiருந்thuu roam varai neengkal payanikka pala vazhigal ingkaehuuu\n\n1. விமானப் பயணmuuuu் moolam முனிக்கிலிருந்து roam varai payanikka மிகவும் podhuvaana mattrum vaekamaana vazhiyaaga irukkalaam. neengkal eppoathu பறக்கிறீர்கள், ungkal டிக்கெட் vaguppu mattrum ungkal டிக்கெட்duukazhaை வாங்கும் thaethikku evvalavu nerukkamaaga இருக்கிறீர்கள் என்பதைப் பொறுத்து, விலை $100 (91 யூரோக்கள்) க்கும் kuraivaaga irunthu $500 (455 யூரோக்கள்) varai மாறுபடும். neengkal பணத்தை சேமிப்பதை uruthiseiya ungkal பயணத்தைத் திட்டமிட்டு முன்கூட்டியே டிக்கெட்duukazhaை வாங்குவதை உறுதிப்படுத்திக் kollungal. maelum, முனிச் oru periya விமான நிலையத்தைக் (ம்யூக்) கொண்டிருந்தாலும், roam irandu periya sarvadesa விமான நிலையங்களைக் (எஃப்சிஓ mattrum சிஐஏ) கொண்டுள்ளது. விமான நிலையம், பாதுகாப்பு கோடுகள் mattrum sunga வரிகளில் நேரத்தைக் கணக்கிடாமல், முனிச்chiiliiருந்thuu roam varai payanikka விமானத்தில் sumar 90 nimidangal aagum.\n\n2. rayil மூலம்-ரயில் moolam பயணmuuuu் seivathu முனிச்chiiliiருந்thuu roam selvatharkaana மற்றொரு podhuvaana வழியாகும். விமானத்தை vida adhiga neram edukkum என்றாலும், டிக்கெட் மிகவும் malivaanathuu mattrum பயண நாளில் vaangkappadalaam. முனிச்chiiliiருந்thuu roam செல்லும் oru vazhi rayil டிக்கெட் sumar $35 (32 யூரோக்கள்) selavaagum, maelum paathai mattrum நிறுத்தங்களின் எண்ணிக்கையைப் பொறுத்து 9-12 மணிநேரங்களுக்கு idaiyil edukkum.\n\n3. kaarr மூலம்-முனிச்சிலிருந்து roam varai qaariill பயணmuuuu் செய்வதும் oru விருப்பமாகும். வரையறுக்கப்பட்ட நிறுத்தங்களுடன், முனிச்chiiliiருந்thuu roam varai vaaganam ஓட்ட sumar 10 manii neram aagum, aanaal oru kaarai vaiththiruppathu neengkal paarkka விரும்பும் endha நகரங்களிலும் allathu தளங்களிலும் நிறுத்த negizhvuththanmaiyaii anumathikkum. \n\nungkal kuripitta தேவைகளைப் பொறுத்து, inththa moontru விருப்பங்களும் முனிச்chiiliiருந்thuu roam varai payanikka saathiyamaana வழிகளாக irukkalaam.''')
    # print(p)