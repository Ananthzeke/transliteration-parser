python src/main.py \
    --dictionary_path "data/tam.json" \
    --cache_dir ".cache" \
    --dataset_path "data/tam/*" \
    --column "translated" \
    --num_proc 8 \
    --batch_size 2 \
    --sample_size 1000 \
    --output_path "data/tam_transliterated" \
    --file_type 'arrow' \
    --replacer_type 'flashtext'