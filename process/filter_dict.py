
spare = ["'", ',', '-', '.', ':', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '、']

with open('/home/ai/hdd/tupm/projects/textGenOCR/trdg/dicts/dlo_address_new.txt') as f:
    lines = f.readlines()

f = open('/home/ai/hdd/tupm/projects/textGenOCR/trdg/dicts/dlo_address_new2.txt', 'w+')

count = 0
for line in lines:
    line = line.strip()
    
    flag = True
    for e in line:
        if e in spare:
            flag = False
            break
    if flag:
        count += 1
        f.write(f'{line}\n')

print(count)
