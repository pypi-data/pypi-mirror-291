import colorsys

class ColorConverter:
    """
    A utility class for converting color codes between different formats.

    Methods:
    - hex_to_rgb(hex_color): Convert HEX color code to RGB tuple.
    - hsl_to_rgb(hsl): Convert HSL tuple to RGB tuple.
    - rgb_to_hsl(rgb): Convert RGB tuple to HSL tuple.
    - rgb_to_hex(rgb): Convert RGB tuple to HEX color code.
    """

    @staticmethod
    def hex_to_rgb(hex_color):
        """Convert HEX color code to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6:
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        elif len(hex_color) == 3:
            return tuple(int(c * 2, 16) for c in hex_color)
        raise ValueError("Invalid HEX color format.")

    @staticmethod
    def hsl_to_rgb(hsl):
        """Convert HSL tuple to RGB tuple."""
        h, s, l = hsl
        s /= 100
        l /= 100
        r, g, b = colorsys.hls_to_rgb(h / 360, l, s)
        return int(r * 255), int(g * 255), int(b * 255)

    @staticmethod
    def rgb_to_hsl(rgb):
        """Convert RGB tuple to HSL tuple."""
        r, g, b = [x / 255.0 for x in rgb]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return (int(h * 360), int(s * 100), int(l * 100))

    @staticmethod
    def rgb_to_hex(rgb):
        """Convert RGB tuple to HEX color code."""
        return '#{:02x}{:02x}{:02x}'.format(*rgb)
    
    
