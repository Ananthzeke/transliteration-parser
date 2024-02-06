python src/main.py \
    --dictionary_path "data/tam.json" \
    --cache_dir ".cache" \
    --dataset_path "data/tam/*" \
    --column "translated" \
    --num_proc 4 \
    --batch_size 16 \
    --output_path "data/tam_transliterated"
    # --sample_size 1000 \
    
