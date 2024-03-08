from datasets import load_from_disk
import os

def convert_arrow_to_csv(base_folder_path):
    print(base_folder_path)
    # Collect paths to all .arrow files in subdirectories
    arrow_files = []
    subfolder_names = []

    for root, dirs, files in os.walk(base_folder_path):
        print(file)
        for file in files:
            if file.endswith(".arrow"):
                arrow_files.append(os.path.join(root, file))
                subfolder_names.append(os.path.basename(root))

    print(len(arrow_files))
    
    

    # Loop through each subfolder and convert .arrow to .csv
    # for subfolder_name in set(subfolder_names):  # Using set to get unique subfolder names
    #     subfolder_paths = [arrow_files[i] for i, name in enumerate(subfolder_names) if name == subfolder_name]

    #     # Load dataset from Arrow files
    #     ds = load_from_disk(
    #     )
    #     input()


    #     # Save the DataFrame to a CSV file with the subfolder name
    #     csv_filename = f"{subfolder_name}.csv"
    #     csv_path = os.path.join(base_folder_path, csv_filename)
    #     ds.to_csv(csv_path, index=False)

# Replace 'your_dataset_name' and 'path/to/your/base/folder' with the actual values
base_folder_path = '/data/transliteration/translated_data/Dolly'

convert_arrow_to_csv(base_folder_path)

