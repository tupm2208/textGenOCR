import os
import pickle
import numpy as np
import random as rnd
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import seaborn
from PIL import Image, ImageColor
from collections import namedtuple


tf.device(0):
sess = tf.Session()
saver = tf.train.import_meta_graph("trdg/handwritten_model/model-29.meta")
saver.restore(sess, "trdg/handwritten_model/model-29")

def generate(text, text_color):
    with open(os.path.join("trdg/handwritten_model", "translation.pkl"), "rb") as file:
        translation = pickle.load(file)

    # config = tf.ConfigProto(device_count={'GPU':0})
    # config.gpu_options.allow_growth = True
    # tf.reset_default_graph()

    # with tf.Session(config=config) as sess:
    if True:
        saver = tf.train.import_meta_graph("trdg/handwritten_model/model-29.meta")
        saver.restore(sess, "trdg/handwritten_model/model-29")

        images = []
        colors = [ImageColor.getrgb(c) for c in text_color.split(",")]
        c1, c2 = colors[0], colors[-1]

        color = "#{:02x}{:02x}{:02x}".format(
            rnd.randint(min(c1[0], c2[0]), max(c1[0], c2[0])),
            rnd.randint(min(c1[1], c2[1]), max(c1[1], c2[1])),
            rnd.randint(min(c1[2], c2[2]), max(c1[2], c2[2])),
        )

        for word in text.split(" "):
            _, window_data, kappa_data, stroke_data, coords = _sample_text(
                sess, word, translation
            )

            strokes = np.array(stroke_data)
            strokes[:, :2] = np.cumsum(strokes[:, :2], axis=0)
            _, maxx = np.min(strokes[:, 0]), np.max(strokes[:, 0])
            miny, maxy = np.min(strokes[:, 1]), np.max(strokes[:, 1])

            fig, ax = plt.subplots(1, 1)
            fig.patch.set_visible(False)
            ax.axis("off")

            for stroke in _split_strokes(_cumsum(np.array(coords))):
                plt.plot(stroke[:, 0], -stroke[:, 1], color=color)

            fig.patch.set_alpha(0)
            fig.patch.set_facecolor("none")

            canvas = plt.get_current_fig_manager().canvas
            canvas.draw()

            image = Image.frombytes(
                'RGB', canvas.get_width_height(), canvas.tostring_rgb()
            )
            image_final=_crop_white_borders(image)

            plt.close()
    
def main():
    text_file = '/media/ai/HDD/tupm/projects/textGenOCR/trdg/dicts/en.txt'
    texts = open(text_file, 'r')