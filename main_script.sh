# target_langs=('asm' 'ben' 'hin' 'kan' 'mal' 'mar' 'npi' 'ory' 'pan' 'san' 'tam' 'tel' 'urd')

# #tgt_lang='tam'
# for tgt_lang in target_langs:
#     echo "${tgt_lang}"
#     python src/main.py \
#         --dictionary_path "/data/umashankar/transliteration/unique_words/Dictionaries/${tgt_lang}.json" \
#         --cache_dir "/data/umashankar/.cache" \
#         --dataset_path "/data/umashankar/transliteration/translated_data/Dolly/${tgt_lang}*/*_final_output/*arrow" \
#         --column "translated" \
#         --num_proc 70 \
#         --batch_size 16 \
#         --output_path "/data/umashankar/test/${tgt_lang}_transliterated" \
#         --file_type 'arrow' \
#         --replacer_type 'memory_replacer' \
#         --replacer_mode 'raw' \
#         --missing_log_path "/data/umashankar/transliteration/missing_dict_Dolly/${tgt_lang}.txt"\
#!/bin/bash

# target_langs=('asm' 'ben' 'hin' 'npi' 'ory' 'pan' 'san' 'urd' 'kan' 'mal' 'mar' 'tam' 'tel')
target_langs='tam'
# Loop through target languages 
for tgt_lang in "${target_langs[@]}"; do
    echo "${tgt_lang}"
    
    # Run the Python script with the specified parameters
    python src/main.py \
        --dictionary_path "/data/umashankar/transliteration/unique_words/Dictionaries/${tgt_lang}.json" \
        --cache_dir "/data/umashankar/.cache1" \
        --dataset_path "/data/umashankar/transliteration/translated_data/Dolly/${tgt_lang}*/*_final_output/*arrow" \
        --column "translated" \
        --num_proc 70 \
        --batch_size  19\
        --output_path "/data/umashankar/transliteration/Dolly/${tgt_lang}_transliterated" \
        --file_type 'arrow' \
        --replacer_type 'memory_replacer' \
        --replacer_mode 'raw' \
        --missing_log_path "/data/umashankar/transliteration/missing_dict_Dolly/${tgt_lang}.txt"\
        --src_lang "tam_Taml"\
        --sample_size 100
done
