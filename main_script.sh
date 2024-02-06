python src/main.py \
    --dictionary_path "data/tam.json" \
    --cache_dir ".cache" \
    --dataset_path "data/tam/*" \
    --column "translated" \
    --num_proc 8 \
    --batch_size 16 \
    --sample_size 500 \
    --output_path "data/tam_transliterated"
    
    
