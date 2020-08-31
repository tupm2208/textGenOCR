import pickle


with open('/home/ai/hdd/tupm/projects/textGenOCR/trdg/dicts/dlo_address_new.txt') as f:
    data = f.read()

charset = list(set(data))
charset.sort()



count = {}

for e in charset:
    count[e] = 0

# print(charset, len(charset))

for e in data:
    count[e] += 1

charset.remove('\n')

print(min(count.values()))

data = {}

for idx, e in enumerate(charset):
    data[e] = idx


with open('/home/ai/projects/tupm/datasets/handwriting/charset_3534.pkl', 'wb') as f:
    pickle.dump(data, f)

print(data, len(charset))