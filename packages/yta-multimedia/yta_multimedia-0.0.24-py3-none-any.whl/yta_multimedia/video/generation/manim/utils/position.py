from yta_multimedia.video.generation.manim.constants import HALF_SCENE_HEIGHT, HALF_SCENE_WIDTH
from random import random

def get_random_position(width, height):
    """
    Returns a random position inside the screen according to the provided element width and
    height to fit in. If you are trying to position a text inside screen limits, you must
    provide text width and height to let this method calculate that random position.

    This method returns an object containing 'x' and 'y' random fitting coordinates.
    """
    X_MINIMUM = -HALF_SCENE_WIDTH + (width / 2)
    X_MAXIMUM = HALF_SCENE_WIDTH - (width / 2)
    random_x = X_MINIMUM + (random() * (X_MAXIMUM - X_MINIMUM))
    Y_MINIMUM = -HALF_SCENE_HEIGHT + (height / 2)
    Y_MAXIMUM = HALF_SCENE_HEIGHT - (height / 2)
    random_y = Y_MINIMUM + (random() * (Y_MAXIMUM - Y_MINIMUM))

    return {
        'x': random_x,
        'y': random_y
    }

# TODO: Create method to 'get_random_upper_left_position'
# TODO: Create method to 'get_random_upper_right_position'
# TODO: Create method to 'get_random_lower_left_position'
# TODO: Create method to 'get_random_lower_right_position'
# TODO: Create method to 'get_random_center_position'