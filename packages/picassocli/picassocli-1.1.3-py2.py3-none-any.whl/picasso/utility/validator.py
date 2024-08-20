import re

class Validator:
    """
    A class for various validation methods.
    """

    @staticmethod
    def is_valid_hex_color(value):
        """
        Validate if the given value is a valid hex color code.

        Args:
            value (str): The color code to validate.

        Returns:
            bool: True if the value is a valid hex color code, False otherwise.
        """
        hex_pattern = re.compile(r'^#[0-9A-Fa-f]{6}$')
        return bool(hex_pattern.match(value))
    

    @staticmethod
    def is_valid_rgb_color(value):
        """
        Validate if the given value is a valid RGB color code.

        Args:
            value (tuple): The RGB color code to validate.

        Returns:
            bool: True if the value is a valid RGB color code, False otherwise.
        """
        if not isinstance(value, tuple) or len(value) != 3:
            return False
        for component in value:
            if not isinstance(component, int) or component < 0 or component > 255:
                return False
        return True

    @staticmethod
    def is_valid_hsl_color(value):
        """
        Validate if the given value is a valid HSL color code.

        Args:
            value (tuple): The HSL color code to validate.

        Returns:
            bool: True if the value is a valid HSL color code, False otherwise.
        """
        if not isinstance(value, tuple) or len(value) != 3:
            return False
        for component in value:
            if not isinstance(component, int) or component < 0 or component > 100:
                return False
        return True