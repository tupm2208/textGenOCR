import pickle


with open('/home/ai/projects/tupm/datasets/handwriting/charset_3595.pkl', 'rb') as f:
    data = pickle.load(f)

# print(data.keys())

spare = ["'", ',', '-', '.', ':', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '、']

for e in spare:
    del data[e]


for idx, e in enumerate(list(data.keys())):
    data[e] = idx


with open('/home/ai/projects/tupm/datasets/handwriting/charset_3537.pkl', 'wb') as f:
    pickle.dump(data, f)
print(data)