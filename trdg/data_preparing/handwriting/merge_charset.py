import pickle
import os

text_path = "/home/tupm/projects/TextRecognitionDataGenerator/trdg/dicts/dlo_address.txt"

with open(text_path, 'r') as f:
    text = f.read()

    unique = ''.join(set(text))


current_charset_path = "/home/tupm/datasets/handwriting/char_mapping_general_3597.pkl"

with open(current_charset_path, 'rb') as f:
    current_charset = pickle.load(f)

current_idx = max(current_charset.values())

for c in unique:
    try:
        current_charset[c]
    except Exception:
        current_idx += 1
        current_charset[c] = current_idx

with open("/home/tupm/datasets/handwriting/char_mapping_general_3663.pkl", 'wb') as f:
    pickle.dump(current_charset, f)
print(current_idx)
