import pickle
import os

text_path = "trdg/dicts/dlo_address.txt"

with open(text_path, 'r') as f:
    text = f.read()

    unique = list(''.join(set(text)))
unique.sort()


current_charset_path = "/home/ai/projects/linhtd/general/AOCR/1/char_mapping_general_3597.pkl"

with open(current_charset_path, 'rb') as f:
    current_charset = pickle.load(f)
    vv = list(current_charset.keys())
    vv.sort()
    print(vv)

current_idx = max(current_charset.values())

for c in unique:
    try:
        current_charset[c]
    except Exception:
        current_idx += 1
        current_charset[c] = current_idx

with open("/home/ai/projects/tupm/datasets/handwriting/char_mapping_general_3597.pkl", 'wb') as f:
    pickle.dump(current_charset, f)
print(current_idx)
