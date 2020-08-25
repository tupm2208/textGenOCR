from tqdm import tqdm


with open('/home/ai/projects/tupm/datasets/handwriting/train/labels.txt') as f:
    lines = f.readlines()

f = open('/home/ai/projects/tupm/datasets/handwriting/train/labels.txt', 'w')

for line in tqdm(lines):
    line = line.strip()
    splited = line.split()
    img_path = splited[0]
    content = "".join(splited[1:])

    f.write(f'{img_path} {content}\n')