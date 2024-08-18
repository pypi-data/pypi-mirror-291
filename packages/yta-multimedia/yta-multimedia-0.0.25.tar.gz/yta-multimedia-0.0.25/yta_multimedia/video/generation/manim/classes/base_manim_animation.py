from yta_multimedia.video.generation.manim.constants import MANDATORY_CONFIG_PARAMETER
from yta_multimedia.video.generation.manim.utils.config import read_manim_config_file, write_manim_config_file
from yta_general_utils.file_processor import get_code_abspath, get_project_abspath, rename_file, get_code_filename, get_file_filename_without_extension
from manim import Scene, AddTextLetterByLetter, Write, DrawBorderThenFill, ApplyWave, FadeIn
from random import randrange
from subprocess import run

class BaseManimAnimation(Scene):
    """
    General class so that our own classes can inherit it 
    and work correctly.
    """
    required_parameters = {}
    parameters = {}

    def parameter_is_mandatory(self, parameter, required_parameters):
        """
        Returns true if the provided 'parameter' is mandatory, based on
        'required_parameters' definition.
        """
        if parameter in required_parameters and required_parameters[parameter] == MANDATORY_CONFIG_PARAMETER:
            return True
        
        return False

    def __set_mandatory_config(self):
        """
        This method set some configuration parameters we need to build perfect
        animation videos.
        """
        # This makes the video background transparent to fit well over the main video
        # TODO: I commented below line because of: AttributeError: 'SimpleText' object has no attribute 'renderer'
        self.camera.background_opacity = 0.0
    
    def setup(self):
        """
        This method is called when manim is trying to use it to
        render the scene animation. It is called the first, to
        instantiate it and before the 'construct' method that
        is the one that will render.
        """
        self.__set_mandatory_config()
        self.parameters = read_manim_config_file()

        return self.parameters
    
    def construct(self):
        """
        This method is called by manim when executed by shell and
        will call the scene animation render method to be processed
        and generated.
        """
        self.setup()

    def animate(self):
        pass

    def generate(self, parameters, output_filename):
        """
        Generates the animation video file using the provided
        'parameters' and stores it locally as 'output_filename'
        """
        # We write parameters in file to be able to read them
        write_manim_config_file(parameters)

        # Variables we need to make it work
        FPS = str(60)
        CLASS_MANIM_CONTAINER_ABSPATH = get_code_abspath(self.__class__)
        CLASS_FILENAME_WITHOUT_EXTENSION = get_file_filename_without_extension(get_code_filename(self.__class__))
        CLASS_NAME = self.__class__.__name__

        # TODO: Please, try to execute it from here as Python code and not through the
        # command line (see here: https://stackoverflow.com/questions/66642657/is-it-possible-to-run-manim-programmatically-and-not-from-the-command-line)
        # TODO: Check if 'animation_name' is accepted
        # -qh is high quality (1080p)
        # '-t' parameter creates a .mov file (that accepts transparency) instead of .mp4
        command_parameters = ['manim', '-qh', '-t', '--fps', FPS, CLASS_MANIM_CONTAINER_ABSPATH, CLASS_NAME]

        manim_output_file_extension = '.mov'
        # TODO: Do more Exception checkings (such as '.smtg')
        if output_filename.endswith('.mp4'):
            #output_filename.replace('.mp4', '.mov')
            # We now delete '-t' parameter instead of forcing .mov
            manim_output_file_extension = '.mp4'
            del command_parameters[2]

        MANIM_CREATIONS_ABSPATH = get_project_abspath() + 'media/videos/' + CLASS_FILENAME_WITHOUT_EXTENSION + '/1080p' + FPS + '/' + CLASS_NAME + manim_output_file_extension

        run(command_parameters)
            
        rename_file(MANIM_CREATIONS_ABSPATH, output_filename)

        return output_filename