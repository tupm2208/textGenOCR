"""
Utility functions
"""

import os
import pickle


def load_dict(lang):
    """Read the dictionnary file and returns all words in it.
    """

    lang_dict = []
    with open(
        os.path.join(os.path.dirname(__file__), "dicts", lang + ".txt"),
        "r",
        encoding="utf8",
        errors="ignore",
    ) as d:
        lang_dict = [l for l in d.read().splitlines() if len(l) > 0]
    return lang_dict


def load_fonts(lang):
    """Load all fonts in the fonts directories
    """

    if lang == "cn":
        return [
            os.path.join(os.path.dirname(__file__), "fonts/cn", font)
            for font in os.listdir(os.path.join(os.path.dirname(__file__), "fonts/cn"))
        ]
    elif lang in ['dlo_address', 'pass']:
        return [
            os.path.join(os.path.dirname(__file__), "fonts/pass", font)
            for font in os.listdir(os.path.join(os.path.dirname(__file__), "fonts/pass"))
        ]
    else:
        return [
            os.path.join(os.path.dirname(__file__), "fonts/latin", font)
            for font in os.listdir(
                os.path.join(os.path.dirname(__file__), "fonts/latin")
            )
        ]


def load_existed_folder(folder_path=None, charset_path=None):
    if folder_path is None:
        return {}, {}
    with open(charset_path, 'rb') as f:
        charset_flag = pickle.load(f)
    existed_char = {}
    text_list = os.listdir(folder_path)

    for text in text_list:
        existed_char[text] = [os.path.join(folder_path, text, e) for e in os.listdir(os.path.join(folder_path, text))]
        charset_flag[text] = True

    return existed_char, charset_flag
