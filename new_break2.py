import json
import re


with open('break_2.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

with open('BK_compound3.json', 'r', encoding='utf-8') as file2:
    info = json.load(file2)


def extract_text(text, info):
    result = []
    i = 0
    while i < len(text):
        found = False
        for length in range(len(text) - i, 0, -1):
            substring = text[i:i+length]

            if "NOTcompound" in info and any(substring in word_list for word_list in info.get("NOTcompound", {}).values()):
                result.append(substring)
                i += length
                found = True
                break

            elif "compound" in info:
                for compound_key, compound_value in info["compound"].items():
                    if substring in compound_value.get("word", []):
                        result.append(substring)
                        i += length
                        found = True
                        break

        if not found:
            result.append(text[i])
            i += 1
    return '/'.join(result)


excluded_characters_pattern = r"[，。:\n\/　…,\.!\"~！》《「」、;『』()+]"

for key, value in data.items():
    if key.startswith("@slnewsptsTaiwan_"):
        sign = value.get('sign', {})
        for subkey, subvalue in sign.items():
            text = subvalue.get('ori_text', '')
            subvalue['ori_text'] = text
            cleaned_text = re.sub(excluded_characters_pattern, '', text)
            extracted_info = extract_text(cleaned_text, info)
            subvalue['text'] = extracted_info

with open('new_break2.json', 'w', encoding='utf-8') as output_file:
    json.dump(data, output_file, ensure_ascii=False, indent=4)

print("已經修改並保存到 'new_break2.json' 文件中。")
