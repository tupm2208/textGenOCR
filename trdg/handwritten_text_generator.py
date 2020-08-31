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


# sess = None

# with tf.device(0):
#     sess = tf.Session()
#     saver = tf.train.import_meta_graph("trdg/handwritten_model/model-29.meta")
#     saver.restore(sess, "trdg/handwritten_model/model-29")


def _sample(e, mu1, mu2, std1, std2, rho):
    cov = np.array([[std1 * std1, std1 * std2 * rho], [std1 * std2 * rho, std2 * std2]])
    mean = np.array([mu1, mu2])

    x, y = np.random.multivariate_normal(mean, cov)
    end = np.random.binomial(1, e)
    return np.array([x, y, end])


def _split_strokes(points):
    points = np.array(points)
    strokes = []
    b = 0
    for e in range(len(points)):
        if points[e, 2] == 1.0:
            strokes += [points[b : e + 1, :2].copy()]
            b = e + 1
    return strokes


def _cumsum(points):
    sums = np.cumsum(points[:, :2], axis=0)
    return np.concatenate([sums, points[:, 2:]], axis=1)


def _sample_text(sess, args_text, translation, style=None):
    style = 3
    if style is not None:
        with open('data/styles.pkl', 'rb') as file:
            styles = pickle.load(file)

        if style > len(styles[0]):
            raise ValueError('Requested style is not in style list')

        style = [styles[0][style], styles[1][style]]
    fields = ['coordinates', 'sequence', 'bias', 'e', 'pi', 'mu1', 'mu2', 'std1', 'std2',
              'rho', 'window', 'kappa', 'phi', 'finish', 'zero_states']
    # for name in fields:
    #     print(name, tf.get_collection(name))
    vs = namedtuple('Params', fields)(
        *[tf.compat.v1.get_collection(name)[0] for name in fields]
    )

    text = np.array([translation.get(c, 0) for c in args_text])
    coord = np.array([0., 0., 1.])
    coords = [coord]

    # Prime the model with the author style if requested
    prime_len, style_len = 0, 0
    if style is not None:
        # Priming consist of joining to a real pen-position and character sequences the synthetic sequence to generate
        #   and set the synthetic pen-position to a null vector (the positions are sampled from the MDN)
        style_coords, style_text = style
        prime_len = len(style_coords)
        style_len = len(style_text)
        prime_coords = list(style_coords)
        coord = prime_coords[0] # Set the first pen stroke as the first element to process
        text = np.r_[style_text, text] # concatenate on 1 axis the prime text + synthesis character sequence
        sequence_prime = np.eye(len(translation), dtype=np.float32)[style_text]
        sequence_prime = np.expand_dims(np.concatenate([sequence_prime, np.zeros((1, len(translation)))]), axis=0)
    sequence = np.eye(len(translation), dtype=np.float32)[text]
    sequence = np.expand_dims(np.concatenate([sequence, np.zeros((1, len(translation)))]), axis=0)

    phi_data, window_data, kappa_data, stroke_data = [], [], [], []
    sess.run(vs.zero_states)
    sequence_len = len(args_text) + style_len
    for s in range(1, 60 * sequence_len + 1):
        is_priming = s < prime_len
        # is_priming = True

        # print('\r[{:5d}] sampling... {}'.format(s, 'priming' if is_priming else 'synthesis'), end='')

        e, pi, mu1, mu2, std1, std2, rho, \
        finish, phi, window, kappa = sess.run([vs.e, vs.pi, vs.mu1, vs.mu2,
                                               vs.std1, vs.std2, vs.rho, vs.finish,
                                               vs.phi, vs.window, vs.kappa],
                                              feed_dict={
                                                  vs.coordinates: coord[None, None, ...],
                                                  vs.sequence: sequence_prime if is_priming else sequence,
                                                  vs.bias: 1.0
                                              })

        if is_priming:
            # Use the real coordinate if priming
            coord = prime_coords[s]
        else:
            # Synthesis mode
            phi_data += [phi[0, :]]
            window_data += [window[0, :]]
            kappa_data += [kappa[0, :]]
            # ---
            g = np.random.choice(np.arange(pi.shape[1]), p=pi[0])
            coord = _sample(e[0, 0], mu1[0, g], mu2[0, g],
                           std1[0, g], std2[0, g], rho[0, g])
            coords += [coord]
            stroke_data += [[mu1[0, g], mu2[0, g], std1[0, g], std2[0, g], rho[0, g], coord[2]]]

            if finish[0, 0] > 0.8:
                # print('\nFinished sampling!\n')
                break

    coords = np.array(coords)
    coords[-1, 2] = 1.

    return phi_data, window_data, kappa_data, stroke_data, coords


def _crop_white_borders(image):
    image_data = np.asarray(image)
    grey_image_data = np.asarray(image.convert("L"))
    non_empty_columns = np.where(grey_image_data.min(axis=0) < 255)[0]
    non_empty_rows = np.where(grey_image_data.min(axis=1) < 255)[0]
    cropBox = (
        min(non_empty_rows),
        max(non_empty_rows),
        min(non_empty_columns),
        max(non_empty_columns),
    )
    image_data_new = image_data[
        cropBox[0] : cropBox[1] + 1, cropBox[2] : cropBox[3] + 1, :
    ]

    img_h = image_data_new.shape[0]

    if rnd.choice([0, 0, 0, 1]) == 0:
        blank_image = np.ones((img_h, 45*rnd.choice([1, 1, 2, 5, 5, 6, 7]), 3), dtype=np.uint8) * 255

        image_data_new = np.concatenate((blank_image, image_data_new ), axis=1)

    return Image.fromarray(image_data_new)


def _join_images(images):
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths) - 35 * len(images)
    max_height = max(heights)

    compound_image = Image.new("RGBA", (total_width, max_height))

    x_offset = 0
    for im in images:
        compound_image.paste(im, (x_offset, 0))
        x_offset += im.size[0] - 35

    return compound_image


class HandwritingSession():
    def __init__(self):
        config = tf.ConfigProto(device_count={'GPU':0})
        self.sess = tf.Session(config=config)
        saver = tf.train.import_meta_graph("trdg/handwritten_model/model-29.meta")
        saver.restore(self.sess, "trdg/handwritten_model/model-29")




def generate(text, text_color):
    with open(os.path.join("trdg/handwritten_model", "translation.pkl"), "rb") as file:
        translation = pickle.load(file)

    # config = tf.ConfigProto(device_count={'GPU':0})
    # config.gpu_options.allow_growth = True
    # tf.reset_default_graph()

    with tf.Session(config=config) as sess:
    # if True:
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
            images.append(_crop_white_borders(image))

            plt.close()

        return _join_images(images)
