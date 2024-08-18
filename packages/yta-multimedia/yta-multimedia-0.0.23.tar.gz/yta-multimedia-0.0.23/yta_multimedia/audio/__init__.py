from moviepy.editor import AudioFileClip

def append_audio_clip_to_audio_clip(base_audio_clip: AudioFileClip, new_audio_clip: AudioFileClip, start_time: float = 0.0, output_filename: str = None):
    """
    We receive a 'base_audio_clip' in which we will append the 'new_audio_clip'
    starting at 'start_time' seconds since the first one started. A combined 
    audio will be generated and returned.

    If 'output_filename' is provided, it will be also written in that 
    destination.
    """
    if start_time < 0:
        start_time = 0

    from moviepy.editor import CompositeAudioClip

    combined = CompositeAudioClip([base_audio_clip, new_audio_clip.set_start(start_time)])
    # TODO: Why 441000 here below?
    combined.fps = 44100

    if output_filename:
        combined.write_audiofile(output_filename)

    return combined

def append_audio_file_to_audio_file(base_audio_filename: str, new_audio_filename: str, start_time: float = 1.0, output_filename: str = None):
    """
    We receive an audio file called 'base_audio_filename' and we append the provided
    'new_audio_filename' to that existing audio to sound over it. That second 
    sound will start in the 'start_time' second of the first 'audio_filename'.

    If 'output_filename' provided, it will write the new combined audio. If not,
    it will only return the new CompositeAudioClip object.

    # TODO: Is this method really necessary (?) I think it is not...
    """
    from yta_general_utils.file_processor import file_is_audio_file

    if not base_audio_filename:
        return None
    
    if not file_is_audio_file(base_audio_filename):
        return None
    
    if not new_audio_filename:
        return None
    
    if not file_is_audio_file(new_audio_filename):
        return None
    
    if start_time < 0:
        return None

    return append_audio_clip_to_audio_clip(AudioFileClip(base_audio_filename), AudioFileClip(new_audio_filename), start_time, output_filename)