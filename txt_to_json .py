import json
import os
import glob
import chardet
import pandas

def preprocess_json(json_file):
    with open(json_file, 'rb') as file:
        raw_data = file.read()
        encoding_result = chardet.detect(raw_data)
        encoding = encoding_result['encoding']

    with open(json_file, 'r', encoding=encoding, errors='replace') as file:
        json_list = [eval(line.strip()) for line in file]

    return json_list

def txt_to_json(json_file, txt_file):
    json_list = preprocess_json(json_file)
    
    #print(json_list[1])
    json_data = []
    for data in json_list:
        start_time = "{:.2f}".format(data.get('start', ''))
        duration = "{:.2f}".format(data.get('duration', ''))
        end_time = "{:.2f}".format(data.get('start', '') + data.get('duration', ''))
        text = data.get('text', '')
    
        subtitle = {
            'start_time': start_time,
            'end_time': end_time,
            'text': text
        }
        json_data.append(subtitle)

    with open(txt_file, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, indent=4, ensure_ascii=False)

    # with open(txt_file, 'w') as file:
    #     for subtitle in json_data:

    #         file.write('start_time: {}\n'.format(subtitle['start_time']))
    #         file.write('end_time: {}\n'.format(subtitle['end_time']))
    #         file.write('text: {}\n'.format(subtitle['text']))

# Folder path containing the TXT files
txt_folder_path = r"C:\Users\91032\Desktop\TWsignTube\test\txt"

# Output folder path for JSON files
json_folder_path = r"C:\Users\91032\Desktop\TWsignTube\test\json"
# Create the output folder if it doesn't exist
os.makedirs(json_folder_path, exist_ok=True)

# Get a list of TXT files in the folder
txt_files = glob.glob(os.path.join(txt_folder_path, '*.txt'))

# Convert each TXT file to JSON
for txt_file in txt_files:
    txt_file_name = os.path.basename(txt_file)
    json_file_name = os.path.splitext(txt_file_name)[0] + '.json'
    json_file_path = os.path.join(json_folder_path, json_file_name)
    txt_to_json(txt_file, json_file_path)
