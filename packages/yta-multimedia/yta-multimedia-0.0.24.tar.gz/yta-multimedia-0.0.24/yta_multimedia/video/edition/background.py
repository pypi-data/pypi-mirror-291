def remove_video_file_background(video_filename: str, output_filename: str):
    """
    Removes the background from the provided 'video_filename' and
    stores it in a new video as 'output_filename' file. The output
    file will be forced to have the '.mov' extension.
    """
    # TODO: This is too demanding as I cannot process it properly
    # Output must end in .mov to preserve transparency
    # TODO: Refactor this code to make it work with python code and not command
    if not video_filename:
        return None
    
    if not output_filename:
        return None
    
    if not output_filename.endswith('.mov'):
        output_filename += '.mov'

    from subprocess import run

    command_parameters = ['backgroundremover', '-i', video_filename, '-tv', '-o', output_filename]

    run(command_parameters)

    return output_filename