
from green_screen.titled_green_screen_image import TitledGreenScreenImage

class GreenScreenImage(TitledGreenScreenImage):
    """
    Green screen of custom size that is placed over a background image of 1920x1080.
    """
    def __init__(self, width = 1344, height = 756):
        super().__init__('', width, height)
