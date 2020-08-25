
with open('/home/ai/hdd/tupm/projects/textGenOCR/trdg/dicts/general_form_ocr.txt') as f:
    text = f.readlines()

f2 =  open('/home/ai/hdd/tupm/projects/textGenOCR/trdg/dicts/dlo_address.txt', 'w+')


# data = list(set(text))
# data.sort()
# # count2 = 0

# count = {e: 0 for e in data}
# count2 = 0
for e in text:
    e = e.strip()
    length = len(e)
    if length > 25:
        f2.write(f'{e[:length//2]}\n')
        f2.write(f'{e[length//2:]}\n')
    else:
        f2.write(f'{e}\n')

# # data.sort()
# print(count)
# print(len(count))
# print(min(count.values()))