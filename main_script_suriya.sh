# target_langs=('asm' 'ben' 'hin' 'kan' 'mal' 'mar' 'npi' 'ory' 'pan' 'san' 'tam' 'tel' 'urd')

# #tgt_lang='tam'
# for tgt_lang in target_langs:
#     echo "${tgt_lang}"
#     python src/main.py \
#         --dictionary_path "/data/umashankar/transliteration/unique_words/Dictionaries/${tgt_lang}.json" \
#         --cache_dir "/data/umashankar/.cache" \
#         --dataset_path "/data/umashankar/transliteration/translated_data/wiki_how/${tgt_lang}*/*_final_output/*arrow" \
#         --column "translated" \
#         --num_proc 70 \
#         --batch_size 16 \
#         --output_path "/data/umashankar/test/${tgt_lang}_transliterated" \
#         --file_type 'arrow' \
#         --replacer_type 'memory_replacer' \
#         --replacer_mode 'raw' \
#         --missing_log_path "/data/umashankar/transliteration/missing_dict_wiki_how/${tgt_lang}.txt"\
#!/bin/bash

# target_langs=('asm' 'ben' 'hin' 'npi' 'ory' 'pan' 'san' 'urd' 'kan' 'mal' 'mar' 'tam' 'tel')
target_langs=( "hin_Deva" "tam_Taml" "asm_Beng" "ben_Beng" "kan_Knda" "mar_Deva" "mal_Mlym" "npi_Deva" "ory_Orya" "pan_Guru" "san_Deva" "tel_Telu" "urd_Arab"  ) #"asm_Beng" "hin_Deva" "ben_Beng" "kan_Knda" "mar_Deva" "mal_Mlym" "npi_Deva" "ory_Orya" "pan_Guru" "san_Deva" "tel_Telu" "urd_Arab" "tam_Taml"
# Loop through target languages 
for tgt_lang in "${target_langs[@]}"; do
    echo "${tgt_lang}"
    # Run the Python script with the specified parameters
    python src/main.py \
        --dictionary_path "/data/umashankar/transliteration/unique_words/Final_Dict/${tgt_lang}_final.json" \
        --cache_dir "/data/umashankar/.cache1" \
        --dataset_path "/data/umashankar/wiki_chat/wiki_chat_data/batches/*/${tgt_lang}*/*_final_output/*arrow" \
        --column "translated" \
        --num_proc  70\
        --batch_size  1\
        --output_path "/data/umashankar/transliteration/2toxic_prompts_sarvam/${tgt_lang}_transliterated" \
        --file_type 'arrow' \
        --replacer_type 'memory_replacer' \
        --replacer_mode 'raw' \
        --missing_log_path "/data/umashankar/transliteration/2_missing_toxic_prompts_sarvam/${tgt_lang}.txt"\
        --src_lang "${tgt_lang}"\
        # --sample_size 100
done
