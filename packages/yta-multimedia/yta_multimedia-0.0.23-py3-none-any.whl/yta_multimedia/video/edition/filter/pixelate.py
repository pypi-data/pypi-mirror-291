# TODO: Here we are importing the library itself, but this is not 
# working if we change the library name, no (?)
from yta_multimedia.image.edition.filter.pixelate import pixelate_image_file
from moviepy.editor import VideoFileClip, ImageSequenceClip
from yta_general_utils.tmp_processor import create_custom_tmp_filename
from yta_general_utils.file_processor import file_is_video_file
from yta_general_utils.type_checker import variable_is_type
from typing import Union

import shutil

def pixelate_video_file(video_input: Union[VideoFileClip, str], output_filename: str = None):
    """
    This methods pixelates the video progressively and then depixelates
    it progressively again. Finally, it writes the new video as
    'output_filename'.

    TODO: Review this to improve and to check, please, it maybe 
    should be experimental (?)
    """
    # TODO: There is another video pixelating method that I think is
    # faster than this one (the 'artistic.pixelated_video.py')
    if not video_input:
        return None
    
    if variable_is_type(video_input, str):
        if not file_is_video_file(video_input):
            return None
        
        video_input = VideoFileClip(video_input)
    
    # We extract frames, and pixelate in ascending order
    original_frames_array = []
    for frame in video_input.iter_frames():
        frame_name = create_custom_tmp_filename('tmp_frame_' + str(len(original_frames_array)) + '.png')
        original_frames_array.append(frame_name)
    video_input.write_images_sequence(create_custom_tmp_filename('tmp_frame_%01d.png'), logger = 'bar')

    # Remove green screen of each frame and store it
    processed_frames_array = []
    num_of_frames = round(video_input.fps * video_input.duration)
    # By now, from start to end
    start_frame = 0
    end_frame = num_of_frames
    pixelate_factor = (1024, 1024)
    pixelation_duration = int(1024 / 64) - 2
    # We will start pixelating, maintain, and remove pixelation
    for index, frame in enumerate(original_frames_array):
        tmp_frame_filename = create_custom_tmp_filename('tmp_frame_processed_' + str(index) + '.png')
        processed_frames_array.append(tmp_frame_filename)
        if index >= start_frame and index <= end_frame:
            pixelate_image_file(frame, pixelate_factor, tmp_frame_filename)

            if index <= (start_frame + pixelation_duration):
                # We are in incrementing process
                tmp_list = list(pixelate_factor)
                tmp_list[0] -= 64
                tmp_list[1] -= 64
                pixelate_factor = tuple(tmp_list)
            elif index >= (end_frame - pixelation_duration):
                # We are in decrementing process
                tmp_list = list(pixelate_factor)
                tmp_list[0] += 64
                tmp_list[1] += 64
                pixelate_factor = tuple(tmp_list)
        else:
            # Just copy the original frame
            shutil.copy(original_frames_array[index], tmp_frame_filename)

    clip = ImageSequenceClip(processed_frames_array, fps = video_input.fps).set_audio(video_input.audio)

    if output_filename:
        clip.write_videofile(output_filename)
            
    return clip
        
    # TODO: Which one is faster, moviepy or ffmpeg (?)
    #parameters = ['ffmpeg', '-y', '-i', WIP_FOLDER + 'tmp_frame_processed_%01d.png', '-r', '30', '-pix_fmt', 'yuva420p', output_filename]
    #run(parameters)