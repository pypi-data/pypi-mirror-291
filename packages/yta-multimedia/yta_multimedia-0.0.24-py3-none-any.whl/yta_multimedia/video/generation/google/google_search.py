from yta_multimedia.video.utils import generate_videoclip_from_image
from yta_multimedia.resources.image.drive_urls import GOOGLE_SEARCH_IMAGE_GOOGLE_DRIVE_DOWNLOAD_URL
from yta_multimedia.audio.sound.generation import create_typing_audio_clip
from yta_general_utils.file_downloader import download_file_from_google_drive
from yta_general_utils.tmp_processor import create_tmp_filename
from moviepy.editor import TextClip, CompositeVideoClip

class GoogleSearch():
    __EXTENDED_DURATION = 0.5
    __DURATION = 3

    def __init__(self, text):
        self.text = text

    def generate(self):
        # Download the resource we need
        TMP_FILENAME = download_file_from_google_drive(GOOGLE_SEARCH_IMAGE_GOOGLE_DRIVE_DOWNLOAD_URL, create_tmp_filename('tmp.jpg'))
        clip = clip = generate_videoclip_from_image(TMP_FILENAME, self.__DURATION + self.__EXTENDED_DURATION)

        # Calculate each char duration and set texts according to this
        text_len = len(self.text)
        each_char_duration = self.__DURATION / text_len

        clips = []
        for i in range(text_len):
            # Generate a text clip for each text writing part
            txt_clip = TextClip(self.text[:i + 1], font = 'Arial', fontsize = 40, color = 'black')
            clip_duration = each_char_duration
            if i == (text_len - 1):
                clip_duration = each_char_duration + self.__EXTENDED_DURATION
            
            txt_clip = txt_clip.set_position([380, 465]).set_duration(clip_duration).set_start(i * each_char_duration)

            clips.append(txt_clip)

        video = CompositeVideoClip([clip] + clips)
        # Here we have the text being written, we need the sound
        audio = create_typing_audio_clip()
        video = video.set_audio(audio)

        return video