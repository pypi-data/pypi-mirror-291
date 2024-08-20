from functools import wraps
from .style_composer import StyleComposer

class StyleDecorator:
    """
    A class-based decorator for applying styles to the output of a function.

    Attributes:
        composer (StyleComposer): An instance of the StyleComposer class to apply styles.
        stringify (bool): Whether to return the formatted string or print it directly.
    """

    def __init__(self, composer: StyleComposer, stringify: bool = False):
        """
        Initialize the decorator with a StyleComposer instance and a stringify option.

        Args:
            composer (StyleComposer): An instance of the StyleComposer class.
            stringify (bool): If True, return the formatted string; if False, print the formatted string.
        """
        if not isinstance(composer, StyleComposer):
            raise TypeError("The composer must be an instance of StyleComposer.")
        self.composer = composer
        self.stringify = stringify

    def __call__(self, func):
        """
        Apply the decorator to the provided function.

        Args:
            func (Callable): The function to decorate.

        Returns:
            Callable: A wrapped function that formats its return value using the composer.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Call the original function
            result = func(*args, **kwargs)
            
            if not isinstance(result, str):
                raise TypeError("The decorated function must return a string.")
            
            # Format the result using the composer
            formatted_result = f"{self.composer.build()}{result}{self.composer.reset_code}"
            
            if self.stringify:
                return formatted_result
            else:
                print(formatted_result)
                return None  # Return None as the output is printed directly
        
        return wrapper
