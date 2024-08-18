"""
    progress_loader.py

    This module provides a `ProgressLoader` class for displaying a customizable progress animation in the terminal.
    The animation runs in a background thread, allowing for concurrent execution of other tasks in the main thread.

    The `ProgressLoader` class can be used as a context manager to easily start and stop the animation. It supports 
    customization of the animation's appearance, including the number of characters, interval between updates, 
    color of the active character, and background color of inactive characters.

    Dependencies:
    - `sys`: For terminal output control.
    - `time`: For timing the animation updates.
    - `concurrent.futures`: For managing the background thread running the animation.
    - `picasso.StyleComposer`: For creating styled text for terminal output.
    
"""

import sys
import time
from concurrent.futures import ThreadPoolExecutor, Future
from picasso import StyleComposer

class ProgressLoader:
    """
    A context manager for displaying a customizable progress animation in the terminal.

    The animation runs in a background thread, allowing the main thread to perform other tasks concurrently.
    You can customize the appearance and behavior of the loader by adjusting parameters such as the number of characters,
    animation interval, and colors.

    Attributes:
        message (str): The message displayed next to the animation. Default is an empty string.
        num_chars (int): Number of characters in the animation sequence. Default is 5.
        interval (float): Time in seconds between updates of the animation. Default is 0.5 seconds.
        char (str): Character used in the animation. Default is "❯".
        color (str): Color of the active character in hexadecimal format. Default is "#ffcc00".
        bg_color (str): Background color of inactive characters in hexadecimal format. Default is "#ffea96".

    Methods:
        __enter__(): Starts the animation in a background thread and returns the instance.
        __exit__(exc_type, exc_value, traceback): Stops the animation, waits for the background thread to finish, 
                                                shuts down the executor, and resets the terminal display.
        _animate(): Runs the animation loop, updating the display with active and inactive characters.
    """

    def __init__(self, message="", num_chars=5, interval=0.5, char="❯", color="#ffcc00", bg_color="#ffea96"):
        """
        Initializes a ProgressLoader instance with customizable parameters.

        Parameters:
            message (str): The initial message displayed next to the animation. Default is an empty string.
            num_chars (int): Number of characters in the animation sequence. Default is 5.
            interval (float): Time in seconds between updates of the animation. Default is 0.5 seconds.
            char (str): Character used in the animation. Default is "❯".
            color (str): Color of the active character in hexadecimal format. Default is "#ffcc00".
            bg_color (str): Background color of inactive characters in hexadecimal format. Default is "#ffea96".
        """
        self.message = message
        self.num_chars = num_chars
        self.interval = interval
        self.char = char
        self.color = color
        self.bg_color = bg_color
        self.running = False
        self.executor = None
        self.future = None
        self.color_style = StyleComposer().set_fg_color(self.color).set_bold().build()
        self.bg_color_style = StyleComposer().set_fg_color(self.bg_color).set_bold().build()

    def __enter__(self):
        """
        Starts the animation in a background thread.

        Returns:
            ProgressLoader: The current instance of ProgressLoader.
        """
        self.running = True
        # Use ThreadPoolExecutor to start the animation
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.future = self.executor.submit(self._animate)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Stops the animation, waits for the background thread to finish, 
        shuts down the executor, and resets the terminal display.

        Parameters:
            exc_type (type): The exception type if an exception was raised.
            exc_value (Exception): The exception instance if an exception was raised.
            traceback (traceback): The traceback object if an exception was raised.
        """
        self.running = False
        
        # Wait for the animation to finish
        if self.future:
            self.future.result()
    
        # Shutdown the executor
        if self.executor:
            self.executor.shutdown()
        
        # Clear the line and reset text color
        sys.stdout.write("\r")
        # sys.stdout.write("\033[0K")  # Clear the line
        sys.stdout.write("\033[0m")  # Reset text color
        sys.stdout.flush()

    def _animate(self):
        """
        Runs the animation loop in the background thread.

        Continuously updates the display with active and inactive characters, 
        creating the effect of a moving progress animation. The display includes
        the animated characters and the message provided.
        """
        while self.running:
            for i in range(self.num_chars):
                if not self.running:
                    break
                # Create a list of chars with the background color
                chars = [self.bg_color_style + self.char + "\033[0m"] * self.num_chars
                # Change color of the current char
                chars[i] = self.color_style + self.char + "\033[0m"
                
                # Join the chars into a single string with the message
                chars_line = " ".join(chars)
                display_line = f"[ {chars_line} ] [ {self.message:<75} ]"
                
                # Move cursor to the beginning of the line
                sys.stdout.write("\r")
                
                # Clear the line and print the updated line
                sys.stdout.write(f"{display_line}")
                sys.stdout.flush()
                
                # Sleep for a short time to create animation effect
                time.sleep(self.interval)
