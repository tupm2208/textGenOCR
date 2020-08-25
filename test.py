from PIL import Image
import cv2
import numpy as np


pil_image = Image.open('/home/tupm/datasets/handwriting/683521_1218106_compressed_CASIA-HWDB_Train/existed/静/358.png')



bbox = pil_image.getbbox()
pil_image = pil_image.crop(bbox)

pil_image.show()
print(pil_image.size)
pil_image = pil_image.resize((80, 112), Image.BICUBIC)
print(pil_image.size)

pil_image.show()