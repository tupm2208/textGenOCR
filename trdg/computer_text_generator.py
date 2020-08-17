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
    image_font = ImageFont.truetype(font=font, size=font_size)
    words = text.split(" ")
    chars = list(text)
    # space_width = image_font.getsize(" ")[0] * space_width

    # words_width = [image_font.getsize(w)[0] for w in words]
    chars_width = [image_font.getsize(w)[0] for w in chars]
    text_width = sum(chars_width) + int(space_width) * (len(chars) - 1)
    text_height = max([image_font.getsize(w)[1] for w in chars])

    txt_img = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))

    txt_draw = ImageDraw.Draw(txt_img)

    colors = [ImageColor.getrgb(c) for c in text_color.split(",")]
    c1, c2 = colors[0], colors[-1]

    fill = (
        rnd.randint(min(c1[0], c2[0]), max(c1[0], c2[0])),
        rnd.randint(min(c1[1], c2[1]), max(c1[1], c2[1])),
        rnd.randint(min(c1[2], c2[2]), max(c1[2], c2[2])),
    )

    for i, w in enumerate(chars):
        x, y = (sum(chars_width[0:i]) + i * int(space_width), 0)
        width, height = image_font.getsize(w)[:2]

        if charset_flag[w] is True:

            char_path = rnd.choice(existed_char[w])
            img_char = Image.open(char_path)
            # img_char.getbbox()
            img_char = img_char.crop(img_char.getbbox())
            c_w, c_h = img_char.size
            new_ch = int(c_h * width/c_w)

            if new_ch > text_height:
                new_cw = int(c_w * height/c_h)
                width = new_cw
            else:
                height = new_ch
            
            img_char = img_char.resize((width, height), Image.BICUBIC)
            
            # print(char_path,(width, height), img_char.size)
            txt_img.paste(img_char, (x, int((text_height-height)/2)))
            txt_draw = ImageDraw.Draw(txt_img)
        else:
            txt_draw.text(
                (x, y),
                w,
                fill=fill,
                font=image_font,
            )

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
