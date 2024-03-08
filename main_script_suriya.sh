# List of target languages
target_langs = ('asm' 'ben' 'tam' 'tel' 'hin' 'mal' 'mar' 'kan'  'urd' 'pan' 'san')

# Iterate over each target language
for tgt_lang in target_langs:
    python src/main.py \
    --dictionary_path "dictionaries/${tgt_lang}.json" \
    --cache_dir ".cache" \
    --dataset_path "datasets/${tgt_lang}*/*_final_output/*arrow" \
    --column "translated" \
    --num_proc 70 \
    --batch_size 6 \
    --output_path "data/toxic_promps_sarvam/${tgt_lang}_transliterated" \
    --file_type 'arrow' \
    --replacer_type 'flashtext' \
    --replacer_mode 'raw' \
    --missing_log_path "missing_dict_toxic_promps_sarvam/${tgt_lang}.txt"\
    # --sample_size 10 \

    # Execute the command or print it for inspection
    # You can use subprocess to execute the command if needed
    print(command)
