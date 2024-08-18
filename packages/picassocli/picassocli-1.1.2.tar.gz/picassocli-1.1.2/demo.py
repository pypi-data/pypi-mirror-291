from picasso import StyleComposer, StyleFormatter, StyleDecorator
import sys

#define some decorators for the demo
accent_decorator=StyleDecorator(StyleComposer().set_bold().set_fg_color("#FF5733"), stringify=False)
underline_decorator=StyleDecorator(StyleComposer().set_underline(), stringify=False)
bold_decorator=StyleDecorator(StyleComposer().set_bold(), stringify=False)
italic_decorator=StyleDecorator(StyleComposer().set_italic(), stringify=False)


def clear_screen():
    """
    Clear the terminal screen.
    """
    print("\033[H\033[J")
    
def header(text):
    """
    Print a header text with a separator.
    """
    print(text.center(80, "-"))

def demo_style_composer():
    # Setting foreground colors using hex values, hsl, and rgb
    header("Setting Foreground Colors")
    
    hex_color = "#C4D600"
    light_hex_color = "#FF5733"
    dark_hex_color = "#333333"
    
    rgb_color = (239, 68, 111)
    hsl_color = (180, 100, 50)

    composer_obj = StyleComposer()

    # Set foreground color using hex value
    composer_obj.set_fg_color(hex_color)
    print(f"{composer_obj.build()}Foreground color set using hex value without specifying the key.{composer_obj.reset_code}")
    
    print("")
    # Set foreground color using hex value
    composer_obj.set_fg_color(color=hex_color)
    print(f"{composer_obj.build()}{str(hex_color):<20} Foreground color set using hex value.{composer_obj.reset_code}")
    
    # Set foreground color using rgb value
    composer_obj.set_fg_color(rgb=rgb_color)
    print(f"{composer_obj.build()}{str(rgb_color):<20} Foreground color set using rgb value.{composer_obj.reset_code}")
    
    # Set foreground color using hsl value
    composer_obj.set_fg_color(hsl=hsl_color)
    print(f"{composer_obj.build()}{str(hsl_color):<20} Foreground color set using hsl value.{composer_obj.reset_code}")
    
    # Setting background colors
    print()
    header("Setting Background Colors")
    composer_obj.reset()
    print(f"\n{composer_obj.build()}After calling the reset method. Default style settings.{composer_obj.reset_code}")
    print()
    
    # Set background color using hex value
    composer_obj.set_bg_color(color=hex_color).set_fg_color(color='#333')
    print(f"{composer_obj.build()}{str(hex_color):<20} Background color set using set_bg_color() method.{composer_obj.reset_code}\n")
    
    # Apply reverse color scheme
    composer_obj.reset().set_fg_color(color=hex_color).set_negative()
    print(f"{composer_obj.build()}Foreground color set using hex value and set_negative() method.{composer_obj.reset_code}")
    
    composer_obj.reset().set_fg_color(rgb=rgb_color).set_negative()
    print(f"{composer_obj.build()}Foreground color set using rgb value and set_negative() method.{composer_obj.reset_code}")
    
    composer_obj.reset().set_fg_color(hsl=hsl_color).set_negative()
    print(f"{composer_obj.build()}Foreground color set using hsl value and set_negative() method.{composer_obj.reset_code}")
    
    # Set bg and fg color using hex value then call set_negative() method
    composer_obj.reset().set_fg_color(rgb=rgb_color).set_bg_color(hsl=hsl_color).set_negative()
    print(f"{composer_obj.build()}Foreground and Background color then applied set_negative() method.{composer_obj.reset_code}\n")

    header("Setting Text Styles")
    bold_key = "set_bold()"
    italic_key = "set_italic()"
    underline_key = "set_underline()"
    strikethrough_key = "set_strikethrough()"
    overline_key = "set_overline()"

    # Bold
    composer_obj.reset().set_fg_color(color=hex_color).set_bold()
    print(f"{composer_obj.build()}{bold_key:<25} Bold styling sample text.{composer_obj.reset_code}\n")

    # Italics
    composer_obj.reset().set_fg_color(color=hex_color).set_italic()
    print(f"{composer_obj.build()}{italic_key:<25} Italic text style applied.{composer_obj.reset_code}\n")

    # Underline
    composer_obj.reset().set_fg_color(color=hex_color).set_underline()
    print(f"{composer_obj.build()}{underline_key:<25} Underline text style applied.{composer_obj.reset_code}\n")

    # Strikethrough
    composer_obj.reset().set_fg_color(color=hex_color).set_strikethrough()
    print(f"{composer_obj.build()}{strikethrough_key:<25} Strikethrough text style applied.{composer_obj.reset_code}\n")

    # Overline
    composer_obj.reset().set_fg_color(color=hex_color).set_overline()
    print(f"{composer_obj.build()}{overline_key:<25} Overline text style applied.{composer_obj.reset_code}\n")

def demo_style_formatter():
    """
    Demonstrates the use of StyleComposer and StyleFormatter for applying various text styles.
    """
    
    # Define colors
    hex_color = "#C4D600"  # Example foreground color
    light_hex_color = "#FF5733"  # Another example foreground color
    dark_hex_color = "#333333"  # Example background color
    
    rgb_color = (239, 68, 111)  # RGB color format
    hsl_color = (180, 100, 50)  # HSL color format

    # Configure the StyleComposer object with desired styles.
    composer = StyleComposer().set_bold().set_fg_color(hsl=hsl_color)
    
    # Header for the demonstration
    print("Practical Example of StyleFormatter")

    # StyleFormatter class is used to apply the styles to the text.
    # It takes StyleComposer object as an argument and applies the styles to the text.
    # print_mode=True will print the styled text to the console; set it to False to return the styled text.
    formatter = StyleFormatter(composer, print_mode=True)
    formatter("This is a sample text with bold style, custom foreground and background colors.")
    formatter("If you set the StyleFormatter object as a variable, you can call it multiple times to apply the same style to different texts.")
    formatter("If you don't want to print the text, set print_mode=False and call the formatter object to get the styled text.")
    
    print("\n")

    # Practical example of defining multiple formatters for different styles
    head = StyleFormatter(
        StyleComposer()
        .set_bold()
        .set_fg_color(rgb=rgb_color), 
        print_mode=True
    )
    accent = StyleFormatter(
        StyleComposer()
        .set_fg_color(color=hex_color), 
        print_mode=True
    )
    underline = StyleFormatter(
        StyleComposer()
        .set_underline(), 
        print_mode=True
    )

    header("Header")
    # Apply the header style formatter
    print("head = StyleFormatter(StyleComposer().set_bold().set_fg_color(rgb=rgb_color), print_mode=True)")
    print('head("This is a Header Text")')
    head("This is a Header Text")
    
    header("Accent")
    # Apply the accent style formatter
    print("accent = StyleFormatter(StyleComposer().set_fg_color(color=hex_color), print_mode=True)")
    print('accent("This is body text with accent colors.")')
    accent("This is body text with accent colors.")
    
    header("Underline")
    # Apply the underline style formatter
    print("underline = StyleFormatter(StyleComposer().set_underline(), print_mode=True)")
    print('underline("This is an underlined text.")')
    underline("This is an underlined text.")

def demo_brightness_effects():
    """
    Demonstrate how different brightness levels affect text color.
    """
    color = "#1cc0c0"  # Base color

    # Generate brightness levels from -1 to 1 in steps of 0.10
    brightness_levels = [round(x * 0.10, 2) for x in range(-10, 11)]

    # Create a StyleComposer instance and set initial color and style
    composer = StyleComposer().set_fg_color(color).set_bold()

    # Create a StyleFormatter instance for printing
    writer = StyleFormatter(composer, print_mode=True)

    # Print text with varying brightness levels
    for brightness in brightness_levels:
        composer._brightness = brightness
        brightness = round(brightness, 2)
        writer(f"This is a sample text with brightness level {brightness:>5}")

def decorator_demo(text):
    """
    A function to demonstrate the use of the StyleDecorator class as a decorator.
    """
    @accent_decorator
    def decorated_accent():
        return text
    
    @underline_decorator
    def decorated_underline():
        return text

    @bold_decorator
    def decorated_bold():
        return text
    
    @italic_decorator
    def decorated_italic():
        return text
    
    decorated_accent()
    decorated_underline()
    decorated_bold()
    decorated_italic()
    
    

def demo_loader():
    """
    A function to demonstrate the use of the ProgressLoader class.
    """
    from picasso import ProgressLoader
    import time
    
    header("ProgressLoader")
    
    
    # Create a ProgressLoader instance
    loader = ProgressLoader(message="Processing", num_chars=3)
    with loader:
        for i in range(1, 101):
            time.sleep(0.1)
    input("\nPress Enter to continue.")
                
    
    
    
    

if __name__ == "__main__":
    # Run demos
    demo_brightness_effects()
    demo_style_composer()
    demo_style_formatter()
    demo_loader()
    
    
    decorator_demo("This is a decorated text.")