 
class StyleComposerError(Exception):
    """Base class for all exceptions related to StyleComposer."""
    pass

class InvalidStyleComposerError(StyleComposerError):
    """Exception raised for invalid StyleComposer instances."""
    def __init__(self, message="The composer must be an instance of StyleComposer."):
        self.message = message
        super().__init__(self.message)

class InvalidStyleAttributeError(StyleComposerError):
    """Exception raised for unknown style attributes."""
    def __init__(self, attribute):
        self.message = f"Unknown style attribute: {attribute}"
        super().__init__(self.message)

class InvalidColorFormatError(StyleComposerError):
    """
    Exception raised for invalid color formats provided to the StyleComposer.

    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="Invalid color format provided. Only HEX color codes are allowed without specifying a key."):
        self.message = message
        super().__init__(self.message)
        
class InvalidHexColorError(ValueError):
    """
    Exception raised for errors in the input hex color format.
    """
    def __init__(self, value):
        super().__init__(f"Invalid hex color value: {value}. Ensure it is a valid hex color code.")
        self.value = value

