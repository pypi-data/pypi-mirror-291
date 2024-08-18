from yta_multimedia.video.generation.manim.classes.base_manim_animation import BaseManimAnimation
from yta_multimedia.video.generation.manim.constants import MANDATORY_CONFIG_PARAMETER
from yta_multimedia.video.generation.manim.utils.animate import simple_play_animation
from manim import Text, DOWN, Write

class SimpleTextManimAnimation(BaseManimAnimation):
    # TODO: Maybe make this more strict with 'type' also
    required_parameters = {
        'text': MANDATORY_CONFIG_PARAMETER,
        'duration': MANDATORY_CONFIG_PARAMETER,
    }

    def construct(self):
        """
        This method is called by manim when executed by shell and
        will call the scene animation render method to be processed
        and generated.
        """
        self.animate()

    def generate(self, text: str = 'Texto', duration: float = 2, output_filename: str = 'output.mov'):
        """
        Checks and validates the provided parameters and generates
        the manim animation if those parameters are valid.
        """
        # Check and validate all parameters
        parameters = {}

        if super().parameter_is_mandatory('text', self.required_parameters) and not text:
            raise Exception('Field "text" is mandatory. Aborting manim creation...')
        
        parameters['text'] = text

        if super().parameter_is_mandatory('duration', self.required_parameters) and not duration:
            raise Exception('Field "duration" is mandatory. Aborting manim creation...')
        if duration < 0 or duration > 100:
            raise Exception('Field "duration" value is not valid. Must be between 0 and 100')
        
        parameters['duration'] = duration

        if not output_filename:
            output_filename = 'output.mov'

        # Generate the animation when parameters are valid
        super().generate(parameters, output_filename)

        return output_filename
    
    def animate(self):
        """
        This code will generate the manim animation and belongs to the
        Scene manim object.
        """
        text = Text(self.parameters['text'], font_size = 100, stroke_width = 2.0, font = 'Arial').shift(DOWN * 0)
        simple_play_animation(self, Write, text, self.parameters['duration'])
