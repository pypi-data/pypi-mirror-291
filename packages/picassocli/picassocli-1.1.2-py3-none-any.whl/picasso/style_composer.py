from .utility import ColorConverter , Validator
from .exceptions import InvalidColorFormatError
class StyleComposer:
    """
    A class for constructing ANSI escape codes for terminal text styling.

    Attributes:
        _styles (list): List of text style codes.
        _fg_r (int): Red component of the foreground color.
        _fg_g (int): Green component of the foreground color.
        _fg_b (int): Blue component of the foreground color.
        _brightness (float): Brightness adjustment factor.
        _fg_color (str): Foreground color code.
        _bg_color (str): Background color code.
        _term_bg_color (str): Terminal background color code.
        _negative (bool): Whether to use a negative color scheme.
        _bright_fg_color (str): Bright foreground color code.
        _bright_bg_color (str): Bright background color code.
        _fg_bright (bool): Whether to use bright foreground color.
        _bg_bright (bool): Whether to use bright background color.
        _ansi_code (str): The generated ANSI escape code string.
    """

    def __init__(self):
        """
        Initializes the composer with default values.
        """
        self._fg_r = 0
        self._fg_g = 0
        self._fg_b = 0
        self._brightness = 0
        
        self._styles = []
        
        self._fg_color = None
        self._bg_color = None
        
        self._term_bg_color = None
        
        self._negative = False
        
        self._bright_fg_color = None
        self._bright_bg_color = None
        
        self._fg_bright = False
        self._bg_bright = False
        
        self._ansi_code = ""
        
    def _adjust_brightness(self, r, g, b, brightness):
        """
        Adjust the brightness of the color by modifying the lightness in the HSL color space.

        Args:
            r (int): Red component (0-255).
            g (int): Green component (0-255).
            b (int): Blue component (0-255).
            brightness (float): Brightness adjustment. Positive values make the color brighter,
                                negative values make it darker.

        Returns:
            tuple: Adjusted RGB values as integers in the range [0, 255].
        """
        # Convert RGB to HSL
        h, s, l = ColorConverter.rgb_to_hsl((r, g, b))
        # Adjust lightness
        l = max(0, min(100, l + brightness * 100))
        # Convert back to RGB
        return ColorConverter.hsl_to_rgb((h, s, l))

    def set_bold(self, enabled=True):
        """
        Enable or disable bold style.

        Args:
            enabled (bool): If True, enable bold style; if False, disable it.

        Returns:
            StyleComposer: The instance of the composer for method chaining.
        """
        self._styles.append('1' if enabled else '22')
        return self

    def set_italic(self, enabled=True):
        """
        Enable or disable italic style.

        Args:
            enabled (bool): If True, enable italic style; if False, disable it.

        Returns:
            StyleComposer: The instance of the composer for method chaining.
        """
        self._styles.append('3' if enabled else '23')
        return self

    def set_underline(self, enabled=True):
        """
        Enable or disable underline style.

        Args:
            enabled (bool): If True, enable underline style; if False, disable it.

        Returns:
            StyleComposer: The instance of the composer for method chaining.
        """
        self._styles.append('4' if enabled else '24')
        return self

    def set_strikethrough(self, enabled=True):
        """
        Enable or disable strikethrough style.

        Args:
            enabled (bool): If True, enable strikethrough style; if False, disable it.

        Returns:
            StyleComposer: The instance of the composer for method chaining.
        """
        self._styles.append('9' if enabled else '29')
        return self

    def set_overline(self, enabled=True):
        """
        Enable or disable overline style.

        Args:
            enabled (bool): If True, enable overline style; if False, disable it.

        Returns:
            StyleComposer: The instance of the composer for method chaining.
        """
        self._styles.append('53' if enabled else '55')
        return self

    def set_fg_color(self, hex_val=None, **kwargs):
        """
        Set the foreground color.

        Args:
            hex_val (str): HEX color code (e.g., '#ff0000').
            **kwargs: Color specification (either 'color', 'rgb', or 'hsl').

        Returns:
            StyleComposer: The instance of the composer for method chaining.
        """
        if hex_val is not None:
            if Validator.is_valid_hex_color(str(hex_val)):
                kwargs['color'] = hex_val
            else:
                raise InvalidColorFormatError("\n\n\tInvalid hex color format, provide a valid hex color code. e.g. '#ff0000'\n")
            
        r, g, b = self._parse_color(**kwargs)
        
        self._fg_r = r
        self._fg_g = g
        self._fg_b = b
        
        # Update the foreground color code with brightness adjustment
        self._fg_color = self.fg_color
        
        return self
    
    @property
    def fg_color(self):
        r, g, b = self._adjust_brightness(self._fg_r, self._fg_g, self._fg_b, self._brightness)
        return f'38;2;{r};{g};{b}'
    
    def set_bright_fg_color(self, **kwargs):
        """
        Set the bright foreground color.

        Args:
            **kwargs: Color specification (either 'color', 'rgb', or 'hsl').

        Returns:
            StyleComposer: The instance of the composer for method chaining.
        """
        r, g, b = self._parse_color(**kwargs)
        self._bright_fg_color = f'38;2;{r};{g};{b};1'
        return self

    def set_bg_color(self, **kwargs):
        """
        Set the background color.

        Args:
            **kwargs: Color specification (either 'color', 'rgb', or 'hsl').

        Returns:
            StyleComposer: The instance of the composer for method chaining.
        """
        r, g, b = self._parse_color(**kwargs)
        self._bg_color = f'48;2;{r};{g};{b}'
        return self

    def set_bright_bg_color(self, **kwargs):
        """
        Set the bright background color.

        Args:
            **kwargs: Color specification (either 'color', 'rgb', or 'hsl').

        Returns:
            StyleComposer: The instance of the composer for method chaining.
        """
        r, g, b = self._parse_color(**kwargs)
        self._bright_bg_color = f'48;2;{r};{g};{b};1'
        return self

    def set_term_bg_color(self, **kwargs):
        """
        Set the terminal background color.

        Args:
            **kwargs: Color specification (either 'color', 'rgb', or 'hsl').

        Returns:
            StyleComposer: The instance of the composer for method chaining.
        """
        r, g, b = self._parse_color(**kwargs)
        self._term_bg_color = f'\033]11;{r};{g};{b}\007'
        return self

    def set_negative(self, enabled=True):
        """
        Enable or disable negative color scheme.

        Args:
            enabled (bool): If True, enable negative color scheme; if False, disable it.

        Returns:
            StyleComposer: The instance of the composer for method chaining.
        """
        if enabled:
            self._styles.append('7')  # Append the reverse color code
        else:
            if '7' in self._styles:
                self._styles.remove('7')  # Remove the reverse color code if disabling
        self._negative = enabled
        return self

    def reset(self):
        """
        Reset all styles and colors to their default values.

        Returns:
            StyleComposer: The instance of the composer for method chaining.
        """
        self._styles = []
        self._fg_color = None
        self._bg_color = None
        self._term_bg_color = None
        self._negative = False
        self._bright_fg_color = None
        self._bright_bg_color = None
        self._ansi_code = ""
        return self

    @property
    def reset_code(self):
        """
        Property to get the ANSI escape code for resetting all styles.

        Returns:
            str: The ANSI escape code string for resetting styles.
        """
        return '\033[0m'

    def _parse_color(self, **kwargs):
        """
        Parse the color specification.

        Args:
            **kwargs: Color specification (either 'color', 'rgb', or 'hsl').

        Returns:
            tuple: RGB color tuple.

        Raises:
            ValueError: If the color specification is invalid.
        """
        if 'color' in kwargs:
            return ColorConverter.hex_to_rgb(kwargs['color'])
        elif 'rgb' in kwargs:
            return kwargs['rgb']
        elif 'hsl' in kwargs:
            return ColorConverter.hsl_to_rgb(kwargs['hsl'])
        else:
            raise ValueError("Invalid color specification. Provide either 'color', 'rgb', or 'hsl'.")

    def build(self):
        """
        Build the ANSI escape code string.

        Returns:
            str: The constructed ANSI escape code string.
        """
        codes = []
        if self._term_bg_color:
            self._ansi_code = self._term_bg_color
            return self._ansi_code

        if self._bright_fg_color:
            codes.append(self._bright_fg_color)
        elif self._fg_color:
            codes.append(self.fg_color)
        if self._bright_bg_color:
            codes.append(self._bright_bg_color)
        elif self._bg_color:
            codes.append(self._bg_color)
        codes.extend(self._styles)

        self._ansi_code = f'\033[{";".join(codes)}m'
        return self._ansi_code

    def __str__(self):
        """
        Return the ANSI escape code string.

        Returns:
            str: The ANSI escape code string.
        """
        return self.build()
