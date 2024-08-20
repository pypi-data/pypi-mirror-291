## Wiki Page: StyleComposer

### Overview

`StyleComposer` is a versatile class in the `picasso` module for defining and managing text styles. It provides methods to set colors, text styles, and other attributes to format text output.

### Features

- **Set Foreground Color**: Supports hex, RGB, and HSL color values.
- **Set Background Color**: Configure the background color of text.
- **Text Styles**: Apply various text styles like bold, italic, underline, etc.
- **Reset**: Revert to default text styles.
- **Brightness**: Adjust text color brightness.

### Example Usage

```python
from picasso import StyleComposer

# Create a StyleComposer instance
composer = StyleComposer()

# Set foreground color using hex value
composer.set_fg_color("#C4D600")

# Apply bold style and print
composer.set_bold()
print(f"{composer.build()}This text is bold.{composer.reset_code}")

# Set background color and foreground color
composer.set_bg_color("#333333").set_fg_color("#FFFFFF")
print(f"{composer.build()}This text has a background color.{composer.reset_code}")

# Set text style and reset
composer.set_italic()
print(f"{composer.build()}This text is italic.{composer.reset_code}")
composer.reset()
```

### Methods

- `set_fg_color(color=None, rgb=None, hsl=None)`: Set the foreground color.
- `set_bg_color(color=None, rgb=None, hsl=None)`: Set the background color.
- `set_bold()`: Apply bold text style.
- `set_italic()`: Apply italic text style.
- `set_underline()`: Apply underline text style.
- `set_strikethrough()`: Apply strikethrough text style.
- `set_overline()`: Apply overline text style.
- `set_negative()`: Reverse colors.
- `reset()`: Revert to default styles.
- `build()`: Build the style string for the text.
- `reset_code`: Get the reset code to revert to default styles.

### Caveats

1. **Style Conflicts**: Applying multiple styles (e.g., bold and underline) might cause conflicts in some terminal emulators or might not be displayed as expected. Always test styles in your target environment.
   
2. **Color Codes**: Ensure that the color codes used (hex, RGB, HSL) are supported by the terminal. Some terminals might not render certain colors correctly.

3. **Performance**: Frequent use of `reset()` and `build()` in a loop might impact performance. Try to minimize the number of resets and builds if you are applying styles in bulk.

### Tips

1. **Use `reset()` Wisely**: Call `reset()` only when necessary to avoid unwanted style changes. If you apply multiple styles sequentially, you may not need to reset each time.

2. **Preview in Target Environment**: Different terminals may render styles differently. Always preview the output in the environment where it will be used to ensure compatibility.

3. **Experiment with Brightness**: Adjusting brightness can enhance readability. Experiment with different brightness levels to find the best contrast for your text.

---

## Wiki Page: StyleFormatter

### Overview

`StyleFormatter` is a class in the `picasso` module that applies predefined styles to text. It simplifies the process of formatting text by using a `StyleComposer` object and allows you to either print or return styled text.

### Features

- **Apply Styles**: Uses a `StyleComposer` object to apply styles.
- **Print or Return Styled Text**: Choose between printing directly or returning the styled text as a string.

### Example Usage

```python
from picasso import StyleComposer, StyleFormatter

# Define colors
hex_color = "#C4D600"
hsl_color = (180, 100, 50)

# Create a StyleComposer instance and set styles
composer = StyleComposer().set_bold().set_fg_color(hsl=hsl_color)

# Create a StyleFormatter instance
formatter = StyleFormatter(composer, print_mode=True)

# Use the formatter to style and print text
formatter("This text is styled with bold and custom foreground color.")

# Create another formatter with different styles
accent = StyleFormatter(StyleComposer().set_fg_color(color=hex_color), print_mode=True)
accent("This text has an accent color.")

# Use print_mode=False to get the styled text without printing
formatted_text = StyleFormatter(composer, print_mode=False)
print(formatted_text("This text is styled but not printed directly."))
```

### Methods

- `__call__(text)`: Apply the style to the text and print it if `print_mode=True`; otherwise, return the styled text as a string.

### Caveats

1. **Print Mode Dependency**: If `print_mode=False`, the output must be handled by the caller. Ensure that the returned string is used or printed appropriately.

2. **Multiple Calls**: Using multiple `StyleFormatter` instances with different styles requires managing the styles carefully. Ensure that the styles applied are correct for each instance.

3. **Style Consistency**: When using multiple `StyleFormatter` objects, verify that the styles are consistent with the overall design and formatting needs.

### Tips

1. **Predefine Styles**: Create and reuse `StyleFormatter` instances with predefined styles for consistency in formatting across different parts of your application.

2. **Testing**: Test the output in different environments to ensure that the styles are applied as expected. Different terminals or platforms might handle styles differently.

3. **Combine Styles**: Use `StyleComposer` to combine multiple styles and create complex formatting. This can be particularly useful for creating headers, emphasized text, or other styled content.

---

## Wiki Page: StyleDecorator

### Overview

`StyleDecorator` is a class in the `picasso` module that allows you to apply styles as decorators. It enables you to style functions that return text, and control whether the styled text is printed directly or returned as a string.

### Features

- **Decorate Functions**: Apply styles to functions that return text.
- **Control Output Handling**: Choose between printing the styled text directly or returning it as a string.

### Example Usage

```python
from picasso import StyleComposer, StyleDecorator

# Define some decorators with stringify=False
accent_decorator = StyleDecorator(StyleComposer().set_bold().set_fg_color("#FF5733"), stringify=False)
underline_decorator = StyleDecorator(StyleComposer().set_underline(), stringify=False)
bold_decorator = StyleDecorator(StyleComposer().set_bold(), stringify=False)
italic_decorator = StyleDecorator(StyleComposer().set_italic(), stringify=False)

def decorator_demo(text):
    """
    Demonstrates the use of StyleDecorator as a decorator.
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
    
    # Directly calling decorated functions will print the styled text
    print("Accent Style:")
    decorated_accent()
    
    print("Underline Style:")
    decorated_underline()
    
    print("Bold Style:")
    decorated_bold()
    
    print("Italic Style:")
    decorated_italic()

# Run the decorator demo
decorator_demo("This is a decorated text.")
```

### Methods

- `__call__(func)`: Decorate a function that returns text. If `stringify=False`, the decorator prints the text directly; if `stringify=True`, it returns the styled text as a string.

### Caveats

1. **Function Return Type**: The decorated function must return a string. If it returns something else, or nothing, the decorator may not work as expected.

2. **Decorator Order**: The order of decorators can affect the final style. Ensure that decorators are applied in the desired sequence.

3. **Print Mode**: When `stringify=False`, ensure that the decorated function’s output is appropriate for direct printing.

### Tips

1. **Stringify Option**: Set `stringify=False` to print styled text directly within functions. Set `stringify=True` if you need to manipulate or further process the styled text.

2. **Chaining Decorators**: You can chain multiple decorators to apply complex styles. Ensure that each decorator’s purpose and effect are clear to avoid conflicts.

3. **Function Testing**: Test decorated functions to verify that they return text correctly and are styled as expected. Debugging styled output might be challenging if issues arise.
