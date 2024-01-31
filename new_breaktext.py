import json

with open('new_break2.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

for key, value in data.items():
    if key.startswith("@slnewsptsTaiwan_"):
        sign = value.get('sign', {})
        for subkey, subvalue in sign.items():
            text = subvalue.get('text', '')
            text_parts = text.split('/')

            # ������??��??�����?"breaktext"??��??��??��??�孵???���?��??��
            subvalue['breaktext'] = text_parts


# ???����??��??��������?���?��������?����??�?
with open('new_break_updated.json', 'w', encoding='utf-8') as output_file:
    json.dump(data, output_file, indent=4, ensure_ascii=False)
