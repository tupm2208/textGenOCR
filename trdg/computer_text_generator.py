import random as rnd

from PIL import Image, ImageColor, ImageFont, ImageDraw, ImageFilter
from .utils import load_existed_folder
from .config import charset_folder, existed_image_folder


existed_char, charset_flag = load_existed_folder(existed_image_folder, charset_folder)


def generate(text, font, text_color, font_size, orientation, space_width, fit):
    if orientation == 0:
        return _generate_existed_text(
            text, font, text_color, font_size, space_width, fit
        )
    elif orientation == 1:
        return _generate_vertical_text(
            text, font, text_color, font_size, space_width, fit
        )
    else:
        raise ValueError("Unknown orientation " + str(orientation))


def _generate_horizontal_text(text, font, text_color, font_size, space_width, fit):
    image_font = ImageFont.truetype(font=font, size=font_size)
    words = text.split(" ")
    space_width = image_font.getsize(" ")[0] * space_width

    words_width = [image_font.getsize(w)[0] for w in words]
    text_width = sum(words_width) + int(space_width) * (len(words) - 1)
    text_height = max([image_font.getsize(w)[1] for w in words])

    txt_img = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))

    txt_draw = ImageDraw.Draw(txt_img)

    colors = [ImageColor.getrgb(c) for c in text_color.split(",")]
    c1, c2 = colors[0], colors[-1]

    fill = (
        rnd.randint(min(c1[0], c2[0]), max(c1[0], c2[0])),
        rnd.randint(min(c1[1], c2[1]), max(c1[1], c2[1])),
        rnd.randint(min(c1[2], c2[2]), max(c1[2], c2[2])),
    )

    for i, w in enumerate(words):
        txt_draw.text(
            (sum(words_width[0:i]) + i * int(space_width), 0),
            w,
            fill=fill,
            font=image_font,
        )

    if fit:
        return txt_img.crop(txt_img.getbbox())
    else:
        return txt_img


def _generate_existed_text(text, font, text_color, font_size, space_width, fit):
    new_txt = text
    nb_space = rnd.randint(0, 5)
    if len(new_txt) > 2:
        if nb_space > 0:
            for i in range(nb_space):
                inserted_idx = rnd.randint(1, len(new_txt) - 1)
                new_txt = new_txt[:inserted_idx] + ' ' + new_txt[inserted_idx:]
    new_txt = new_txt.strip()
    text = new_txt
    image_font = ImageFont.truetype(font=font, size=font_size)
    words = text.split(" ")
    chars = list(text)

    chars_width = [image_font.getsize(w)[0] for w in chars]
    text_width = sum(chars_width) + int(space_width) * (len(chars) - 1)
    text_height = max([image_font.getsize(w)[1] for w in chars])

    txt_img = Image.new("RGBA", (text_width+300, text_height), (0, 0, 0, 0))

    txt_draw = ImageDraw.Draw(txt_img)

    colors = [ImageColor.getrgb(c) for c in text_color.split(",")]
    c1, c2 = colors[0], colors[-1]

    fill = (
        rnd.randint(min(c1[0], c2[0]), max(c1[0], c2[0])),
        rnd.randint(min(c1[1], c2[1]), max(c1[1], c2[1])),
        rnd.randint(min(c1[2], c2[2]), max(c1[2], c2[2])),
    )

    current_x = 0

    for i, w in enumerate(chars):
        x, y = (sum(chars_width[0:i]) + i * int(space_width), 0)
        width, height = image_font.getsize(w)[:2]

        start_y = 0

        if rnd.choice([0, 0, 0, 1]) == 1:
        # if True:
            start_y = rnd.randint(int(0.2*height), int(0.3*height))
            # if w in ['・', 'ー']:
            #     print(start_y)
            cr_height = height
            cr_width = width
            height = cr_height - start_y

            width = int(cr_width* height/cr_height)
        

        if charset_flag[w] is True:

            while True:
                try:
                    char_path = rnd.choice(existed_char[w])
                    img_char = Image.open(char_path)
                    break
                except Exception:
                    pass
            bbox = img_char.getbbox()
            img_char = img_char.crop(bbox)
            c_w, c_h = img_char.size
            # print(img_char.size)
            new_ch = int(c_h * width/c_w)

            if new_ch > text_height:
                new_cw = int(c_w * height/c_h)
                width = new_cw
            else:
                height = new_ch
            # width = int(c_w * height/c_h)
            # img_char = img_char.resize((width, height), Image.BICUBIC)
            # txt_img.paste(img_char, (current_x, int((text_height-height + start_y)/2)))
            # # txt_img.paste(img_char, (current_x, rnd.randint(0, text_height-height)))
            # txt_draw = ImageDraw.Draw(txt_img)
            start_y = int((text_height-height + start_y)/2)
        else:
            img_char = Image.new("RGBA", image_font.getsize(w)[:2], (0, 0, 0, 0))
            char_img_draw = ImageDraw.Draw(img_char)

            char_img_draw.text(
                (0, 0),
                w,
                fill=fill,
                font=image_font
            )

            # bbox = img_char.getbbox()
            # img_char = img_char.crop(bbox)
            
        if rnd.choice([0, 0, 0, 0, 1]) == 1:
        # if True:
            img_char = img_char.rotate(rnd.randint(1, 5), expand=True, fillcolor=255)
        img_char = img_char.resize((width, height), Image.BICUBIC)

        txt_img.paste(img_char, (current_x, start_y))
        # txt_img.paste(img_char, (current_x, rnd.randint(0, text_height-height)))
        txt_draw = ImageDraw.Draw(txt_img)
        
        current_x += width
    
    txt_img = txt_img.crop((0, 0, current_x, text_height))
    if fit:
        return txt_img.crop(txt_img.getbbox())
    else:
        return txt_img


def _generate_vertical_text(text, font, text_color, font_size, space_width, fit):
    image_font = ImageFont.truetype(font=font, size=font_size)

    space_height = int(image_font.getsize(" ")[1] * space_width)

    char_heights = [
        image_font.getsize(c)[1] if c != " " else space_height for c in text
    ]
    text_width = max([image_font.getsize(c)[0] for c in text])
    text_height = sum(char_heights)

    txt_img = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))

    txt_draw = ImageDraw.Draw(txt_img)

    colors = [ImageColor.getrgb(c) for c in text_color.split(",")]
    c1, c2 = colors[0], colors[-1]

    fill = (
        rnd.randint(c1[0], c2[0]),
        rnd.randint(c1[1], c2[1]),
        rnd.randint(c1[2], c2[2]),
    )

    for i, c in enumerate(text):
        txt_draw.text((0, sum(char_heights[0:i])), c, fill=fill, font=image_font)
    
    if fit:
        return txt_img.crop(txt_img.getbbox())
    else:
        return txt_img
