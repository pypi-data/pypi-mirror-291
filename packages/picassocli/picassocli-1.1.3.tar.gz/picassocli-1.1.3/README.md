# PicassoCLI
![icon](assets/icon_banner_lght.svg)

Picasso is a versatile Python module for styling text in terminal applications. It provides a set of tools for applying colors, text styles, and formatting to enhance text presentation in console outputs.

## Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## About

Picasso is designed to help developers create visually appealing text outputs in terminal applications. With Picasso, you can easily apply various styles such as bold, italic, underline, and colorize text using hex, RGB, or HSL color formats. Whether you’re building a CLI tool or simply want to enhance your terminal logs, Picasso provides a flexible and powerful way to style your text.

## Features

- **Text Styling**: Apply bold, italic, underline, strikethrough, and overline styles to your text.
- **Color Support**: Set foreground and background colors using hex, RGB, and HSL values.
- **Brightness Adjustment**: Modify the brightness of text colors.
- **Decorators**: Use decorators to apply styles to functions that return text.
- **Formatter**: Apply and manage styles efficiently with `StyleFormatter`.

## Installation

To install Picasso, you can use `pip`:

```sh
pip install picassocli
```

Ensure you have Python 3.6 or higher installed. Picasso is compatible with most terminal emulators that support ANSI escape codes for text styling.

## Usage

Here are some basic examples to get you started with Picasso:

### Using `StyleComposer`

```python
from picasso import StyleComposer

# Create a StyleComposer instance
composer = StyleComposer()

# Set foreground color and apply bold style
composer.set_fg_color("#C4D600").set_bold()
print(f"{composer.build()}This text is bold with a custom color.{composer.reset_code}")

# Reset to default styles
composer.reset()
```

### Using `StyleFormatter`

```python
from picasso import StyleComposer, StyleFormatter

# Define a StyleComposer instance
composer = StyleComposer().set_bold().set_fg_color("#C4D600")

# Create a StyleFormatter instance
formatter = StyleFormatter(composer, print_mode=True)

# Use the formatter to print styled text
formatter("This is a bold text with a custom color.")

# Get styled text without printing
formatted_text = StyleFormatter(composer, print_mode=False)
print(formatted_text("This text is styled but not printed directly."))
```

### Using `StyleDecorator`

```python
from picasso import StyleComposer, StyleDecorator

# Define decorators
accent_decorator = StyleDecorator(StyleComposer().set_bold().set_fg_color("#FF5733"), stringify=False)
underline_decorator = StyleDecorator(StyleComposer().set_underline(), stringify=False)

def decorator_demo(text):
    @accent_decorator
    def decorated_accent():
        return text
    
    @underline_decorator
    def decorated_underline():
        return text

    # Print decorated text
    print("Accent Style:")
    print(decorated_accent())
    
    print("Underline Style:")
    print(decorated_underline())

# Run the decorator demo
decorator_demo("This is a decorated text.")
```

## Using `ProgressLoader`

The `progress_loader` module provides a `ProgressLoader` class for displaying a customizable progress animation in the terminal. Here’s how you can use it:

 
```python
import time
from picasso.progress_loader import ProgressLoader

def long_running_task():
    # Simulate a long-running task
    time.sleep(10)
    print("Task completed!")

if __name__ == "__main__":
    try:
        # Customize the ProgressLoader parameters as needed
        with ProgressLoader(
            # Initial message displayed next to the animation
            message="Processing", 
            # Number of characters in the animation sequence
            num_chars=4, 
            # Time between updates of the animation
            interval=0.3,
            # Character used for the animation           
            char=" @ ", 
            # Color of the active character
            color="#00ff00",        
            # Background color of inactive characters
            bg_color="#004400"      
        ) as loader:
            long_running_task()  # Run the long task while the loader shows progress

    except KeyboardInterrupt:
        print("\nOperation was interrupted.")
```
## Contributing

We welcome contributions to Picasso! If you'd like to contribute, please follow these guidelines:

1. **Fork the Repository**: Create a fork of the repository on GitHub.
2. **Create a Branch**: Create a new branch for your feature or bug fix.
3. **Make Changes**: Implement your changes and test thoroughly.
4. **Submit a Pull Request**: Submit a pull request with a clear description of your changes.

Please ensure your code adheres to the project's style guidelines and includes appropriate tests.

## License

Picasso is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
