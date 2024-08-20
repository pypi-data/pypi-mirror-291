from .style_composer import StyleComposer
from .exceptions.style_exceptions import InvalidStyleComposerError

class StyleFormatter:
    
    def __init__(self, composer, print_mode=False):
        """
        Initialize the formatter with a StyleComposer instance and a mode to control printing.

        Args:
            composer (StyleComposer): An instance of the StyleComposer class.
            print_mode (bool): If True, print the formatted text directly; if False, return the formatted text.
        """
        self._validate_composer(composer)
        self.composer = composer
        self.print_mode = print_mode

    def __call__(self, text):
        """
        Format the given text using the current style settings.

        Args:
            text (str): The text to format.

        Returns:
            str: The formatted text with ANSI escape codes if not in print mode.
        """
        formatted_text = f"{self.composer.build()}{text}{self.composer.reset_code}"
        
        if self.print_mode:
            print(formatted_text)
        else:
            return formatted_text

    def format(self, text):
        """
        An alias for __call__ to provide a more descriptive method name.

        Args:
            text (str): The text to format.

        Returns:
            str: The formatted text with ANSI escape codes if not in print mode.
        """
        return self.__call__(text)

    def update_style(self, **kwargs):
        """
        Update the StyleComposer instance with new style settings.

        Args:
            **kwargs: Key-value pairs to set style attributes (e.g., bold=True, fg_color='red').
        """
        for key, value in kwargs.items():
            method = getattr(self.composer, f'set_{key}', None)
            if callable(method):
                method(value)
            else:
                raise AttributeError(f"Unknown style attribute: {key}")

    def _validate_composer(self, composer):
        """
        Validate that the provided object is an instance of StyleComposer.

        Args:
            composer (object): The object to validate.

        Raises:
            TypeError: If the object is not an instance of StyleComposer.
        """
        if not isinstance(composer, StyleComposer):
            raise InvalidStyleComposerError("The composer must be an instance of StyleComposer.")
    
    def __repr__(self):
        """
        Return a string representation of the StyleFormatter instance for debugging.

        Returns:
            str: The string representation of the instance.
        """
        return (f"StyleFormatter(composer={repr(self.composer)}, print_mode={self.print_mode})")

    def __str__(self):
        """
        Return a user-friendly string representation of the StyleFormatter instance.

        Returns:
            str: A brief description of the instance.
        """
        return (f"StyleFormatter with {str(self.composer)} and print_mode={self.print_mode}")

