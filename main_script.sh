
tgt_lang='tam'

python src/main.py \
    --dictionary_path "dictionaries/${tgt_lang}.json" \
    --cache_dir ".cache" \
    --dataset_path "datasets/${tgt_lang}*/*_final_output/*arrow" \
    --column "translated" \
    --num_proc 32 \
    --batch_size 10 \
    --output_path "data/${tgt_lang}_transliterated" \
    --file_type 'arrow' \
    --replacer_type 'flashtext' \
    --replacer_mode 'raw' \
    --missing_log_path "missing_dict/${tgt_lang}.txt"
    # --sample_size 10 \