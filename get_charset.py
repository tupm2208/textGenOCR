from pickle import dump


with open('/home/ai/hdd/tupm/projects/textGenOCR/trdg/dicts/dlo_address.txt') as f:
    data = f.read()

data = list(set(data))

data.remove('\n')

data.sort()

data = {e: idx for idx, e in enumerate(data)}

with open(f'charset_{len(data)}.pkl', 'wb+') as f:
    dump(data, f)

print(data)