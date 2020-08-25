import os
import random as rnd
import random

from PIL import Image, ImageFilter
import cv2
from .utils import load_existed_folder
from skimage.util import random_noise
import numpy as np

from trdg import (
    computer_text_generator,
    background_generator,
    distorsion_generator,
)

try:
    from trdg import handwritten_text_generator
except ImportError as e:
    print("Missing modules for handwritten text generation.")


class FakeTextDataGenerator(object):
    @classmethod
    def generate_from_tuple(cls, t):
        """
            Same as generate, but takes all parameters as one tuple
        """

        cls.generate(*t)

    @classmethod
    def generate(
        cls,
        index,
        text,
        font,
        out_dir,
        size,
        extension,
        skewing_angle,
        random_skew,
        blur,
        random_blur,
        background_type,
        distorsion_type,
        distorsion_orientation,
        is_handwritten,
        name_format,
        width,
        alignment,
        text_color,
        orientation,
        space_width,
        margins,
        fit,
    ):
        image = None


        margin_top, margin_left, margin_bottom, margin_right = margins

        margin_top = rnd.randint(0, 7)
        margin_bottom = rnd.randint(0, 7-margin_top)
        horizontal_margin = margin_left + margin_right
        vertical_margin = margin_top + margin_bottom

        ##########################
        # Create picture of text #
        ##########################
        if is_handwritten:
            if orientation == 1:
                raise ValueError("Vertical handwritten text is unavailable")
            image = handwritten_text_generator.generate(text, text_color)
        else:
            image = computer_text_generator.generate(
                text, font, text_color, size, orientation, space_width, fit
            )

        # random_angle = rnd.randint(0 - skewing_angle, skewing_angle)

        # rotated_img = image.rotate(
        #     skewing_angle if not random_skew else random_angle, expand=1
        # )

        rotated_img = image

        #############################
        # Apply distorsion to image #
        #############################
        if distorsion_type == 0:
            distorted_img = rotated_img  # Mind = blown
        elif distorsion_type == 1:
            distorted_img = distorsion_generator.sin(
                rotated_img,
                vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2),
            )
        elif distorsion_type == 2:
            distorted_img = distorsion_generator.cos(
                rotated_img,
                vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2),
            )
        else:
            distorted_img = distorsion_generator.random(
                rotated_img,
                vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2),
            )

        ##################################
        # Resize image to desired format #
        ##################################

        # Horizontal text
        if orientation == 0:
            new_width = int(
                distorted_img.size[0]
                * (float(size - vertical_margin) / float(distorted_img.size[1]))
            )
            resized_img = distorted_img.resize(
                (new_width, size - vertical_margin), Image.ANTIALIAS
            )
            background_width = width if width > 0 else new_width + horizontal_margin
            background_height = size
        # Vertical text
        elif orientation == 1:
            new_height = int(
                float(distorted_img.size[1])
                * (float(size - horizontal_margin) / float(distorted_img.size[0]))
            )
            resized_img = distorted_img.resize(
                (size - horizontal_margin, new_height), Image.ANTIALIAS
            )
            background_width = size
            background_height = new_height + vertical_margin
        else:
            raise ValueError("Invalid orientation")

        #############################
        # Generate background image #
        #############################
        if background_type == 0:
            background = background_generator.gaussian_noise(
                background_height, background_width
            )
        elif background_type == 1:
            background = background_generator.plain_white(
                background_height, background_width
            )
        elif background_type == 2:
            background = background_generator.quasicrystal(
                background_height, background_width
            )
        else:
            background = background_generator.picture(
                background_height, background_width
            )

        #############################
        # Place text with alignment #
        #############################

        new_text_width, _ = resized_img.size

        if alignment == 0 or width == -1:
            background.paste(resized_img, (margin_left, margin_top), resized_img)
        elif alignment == 1:
            background.paste(
                resized_img,
                (int(background_width / 2 - new_text_width / 2), margin_top),
                resized_img,
            )
        else:
            background.paste(
                resized_img,
                (background_width - new_text_width - margin_right, margin_top),
                resized_img,
            )
        ##################################
        # Add Noise                      #
        ##################################
        """
         - 'gaussian'  Gaussian-distributed additive noise.
        - 'localvar'  Gaussian-distributed additive noise, with specified
                      local variance at each point of `image`.
        - 'poisson'   Poisson-distributed noise generated from the data.
        - 'salt'      Replaces random pixels with 1.
        - 'pepper'    Replaces random pixels with 0 (for unsigned images) or
                      -1 (for signed images).
        - 's&p'       Replaces random pixels with either 1 or `low_val`, where
                      `low_val` is 0 for unsigned images or -1 for signed
                      images.
        - 'speckle'   Multiplicative noise using out = image + n*image, where
                      n is uniform noise with specified mean & variance.
        """

        # im_arr = np.asarray(background)
        # NOISES = ['gaussian', 'localvar', 'poisson', 'salt', 'pepper', 's&p', 'speckle']
        
        # if random.choice([1]) == 1:
        #     final_image = random_noise(im_arr, mode=random.choice(NOISES[:4]))
        #     final_image = (255 * final_image).astype(np.uint8)
        #     final_image = Image.fromarray(final_image)
        #     if random.choice([0, 1]) == 1:
        #         final_image = final_image.filter(
        #             ImageFilter.GaussianBlur(
        #                 radius=(blur if not random_blur else random.randint(2, 3))
        #             )
        #         )
        # elif random.choice([0, 1, 1, 1]) == 0:
        #     final_image = background
        #     ##################################
        #     # Apply gaussian blur            #
        #     ##################################
        #     final_image = final_image.filter(
        #         ImageFilter.GaussianBlur(
        #             radius=(blur if not random_blur else random.randint(0, blur))
        #         )
        #     )
        # else:
        #     final_image = background

        final_image = background
        ##################################
        # Apply gaussian blur #
        ##################################

        final_image = background.filter(
            ImageFilter.GaussianBlur(
                radius=(blur if not random_blur else rnd.randint(0, blur))
            )
        )

        #####################################
        # Generate name for resulting image #
        #####################################
        if name_format == 0:
            image_name = "{}_{}.{}".format(text, str(index), extension)
        elif name_format == 1:
            image_name = "{}_{}.{}".format(str(index), text, extension)
        elif name_format == 2:
            image_name = "{}/{}.{}".format(str(index//1000), str(index), extension)
        else:
            print("{} is not a valid name format. Using default.".format(name_format))
            image_name = "{}_{}.{}".format(text, str(index), extension)

        # Save the image
        if out_dir is not None:
            image_path = os.path.join(out_dir, image_name)
            image_dir_path = os.path.dirname(image_path)
            os.makedirs(image_dir_path, exist_ok=True)
            final_image.convert("RGB").save(image_path)
            
            # cv2.imwrite(os.path.join(image_dir_path, image_name), final_image)
        else:
            return final_image.convert("RGB")
