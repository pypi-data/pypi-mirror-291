## `progress_loader` Module Wiki
This module provides a `ProgressLoader` class for displaying a customizable progress animation in the terminal. The loader runs in a background thread and allows the main thread to perform other tasks concurrently.

### Imports

```python
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from picasso import StyleComposer
```

### Class: `ProgressLoader`

**Description:**  
`ProgressLoader` is a context manager that displays a progress animation with customizable parameters such as the number of characters, animation interval, and colors. The animation runs in a background thread, allowing the main thread to execute other operations.

**Constructor:**

```python
def __init__(self, message="", num_chars=5, interval=0.5, char="❯", color="#ffcc00", bg_color="#ffea96"):
```

- **Parameters:**
  - `message` (str): The initial message displayed next to the animation. Default is an empty string.
  - `num_chars` (int): Number of characters in the animation sequence. Default is 5.
  - `interval` (float): Time in seconds between updates of the animation. Default is 0.5 seconds.
  - `char` (str): Character used in the animation. Default is "❯".
  - `color` (str): Color of the active character in hexadecimal format. Default is "#ffcc00".
  - `bg_color` (str): Background color of inactive characters in hexadecimal format. Default is "#ffea96".

**Context Management:**

- **`__enter__()`**
  - Starts the animation in a background thread using `ThreadPoolExecutor`.
  - Returns the `ProgressLoader` instance.

- **`__exit__(self, exc_type, exc_value, traceback)`**
  - Stops the animation and waits for the background thread to finish.
  - Shuts down the `ThreadPoolExecutor`.
  - Resets the terminal display to clear the animation.

**Methods:**

- **`_animate(self)`**
  - Runs the animation loop in the background thread.
  - Updates the display by cycling through active and inactive characters.
  - Uses ANSI escape codes for color and cursor manipulation.
  - Continuously updates the display based on the animation interval.

**Example Usage:**

```python
if __name__ == "__main__":

    def do_something():
        # Simulate a long-running task
        time.sleep(5)
        print("Task completed!")

    try:
        # Customize these parameters as needed
        with ProgressLoader(
            message="Task in progress",  
            num_chars=3,          # Number of characters in the animation
            interval=0.3,         # Time between updates
            color="#ffaa00",      # Color of the active character
            char="❯",             # Character used in the animation
            bg_color="#ffe7ad"    # Background color of inactive characters
        ) as loader:
            time.sleep(5)  # Simulate work being done
            print("Task completed!")  # Print when the first task is done
            loader.message = "Starting the next task"  # Update the message
            do_something()  # Perform another long-running task

    except KeyboardInterrupt:
        print("\nOperation was interrupted.")
```

### Notes:

- **Threading:** The animation is handled in a background thread to allow the main thread to perform other tasks without interruption.
- **Terminal Handling:** The class uses ANSI escape codes to manage text color and cursor positioning in the terminal.
- **Error Handling:** The `KeyboardInterrupt` exception is caught to handle user interruption (Ctrl+C) gracefully.
- **Customization:** The loader's appearance and behavior can be customized by adjusting parameters such as `num_chars`, `interval`, `char`, `color`, and `bg_color`.

 