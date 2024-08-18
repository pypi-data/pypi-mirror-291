from yta_multimedia.green_screen.custom_green_screen_video import CustomGreenScreenVideo
from yta_general_utils.tmp_processor import create_tmp_filename
from yta_image_edition_module.green_screen import get_green_screen_position
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
from yta_general_utils.file_downloader import download_file_from_google_drive
from typing import Union

class VideoGreenscreen:
    """
    Object that represents a greenscreen video that will have some image or
    video inserted on itself.
    """
    def __init__(self, google_drive_url: str):
        # We download the green screen file from Google Drive
        # TODO: Expect 'google_drive_url' as an Enum to control them
        filename = download_file_from_google_drive(google_drive_url, create_tmp_filename('tmp.jpg'))
        # We generate a temp frame to get green screen position information
        tmp_frame_filename = create_tmp_filename('tmp_frame.png')
        VideoFileClip(filename).save_frame(tmp_frame_filename, t = 0)

        # We handle rgb color and position
        green_screen_info = get_green_screen_position(tmp_frame_filename)
        rgb_color = green_screen_info['rgb_color']
        self.ulx = green_screen_info['ulx']
        self.uly = green_screen_info['uly']
        self.drx = green_screen_info['drx']
        self.dry = green_screen_info['dry']

        # We work to maintain the proportion
        # TODO: Please, review this below
        gs_width = self.drx - self.ulx
        gs_height = self.dry - self.uly
        aspect_ratio = gs_width / gs_height
        if aspect_ratio > (1920 / 1080):
            # We keep the width, but we calculate the height to keep 16/9 aspect ratio
            gs_height_for_16_9 = gs_width * (1080 / 1920)
            # Now we know the new height, so we only have to center the video on 'y' axis
            difference = gs_height_for_16_9 - gs_height
            # My video (16/9) will not fit the whole width
            self.uly -= difference / 2
            self.dry += difference / 2
        elif aspect_ratio < (1920 / 1080):
            # We keep the height, but we calculate the width to keep 16/9 aspect ratio
            gs_width_for_16_9 = gs_height * (1920 / 1080)
            # Now we know the new width, so we only have to center the video on 'x' axis
            difference = gs_width_for_16_9 - gs_width
            self.ulx -= difference / 2
            self.drx += difference / 2
        # TODO: Are we sure that those coords are int and make a real 16/9 with int numbers?

        # TODO: Is this other object needed or could it be the main one?
        self.cgsv = CustomGreenScreenVideo(filename, rgb_color, self.ulx, self.uly, self.drx, self.dry, None, None, None, None, None, None, None, None, None, None)

    # TODO: Documment this below
    def from_image_to_image(self, image_filename: str, output_filename: str):
        return self.cgsv.from_image_to_image(image_filename, output_filename)

    def from_image_to_video(self, image_filename: str, duration: float = 3.0, output_filename: Union[str, None] = None):
        """
        Receives an 'image_filename', places it into the greenscreen and generates
        a video of 'duration' seconds of duration that is returned. This method
        will store locally the video if 'output_filename' is provided.
        """
        return self.cgsv.from_image_to_video(image_filename, duration, output_filename)

    def from_video_to_image(self):
        return self.cgsv.from_video_to_image()

    def from_video_to_video(self, video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip], output_filename: Union[str, None] = None):
        """
        Inserts the provided 'video' in the greenscreen and returns the
        CompositeVideoClip that has been created. If 'output_filename' 
        provided, it will be written locally with that file name.

        The provided 'video' can be a filename or a moviepy video clip.

        TODO: Careful when video is longer than greenscreen
        """
        return self.cgsv.from_video_to_video(video, output_filename)