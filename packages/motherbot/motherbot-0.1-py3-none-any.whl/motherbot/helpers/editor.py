"""
Editor module.
"""

import tkinter as tk
from tkinter import font
from typing import Optional


class Editor(tk.Frame):
    """
    A class used to create a text editor with a character limit and keyboard
    shortcuts.

    Attributes:
        char_limit (int): The maximum number of characters allowed in the text
        entry.
        master (tk.Tk): The root window or parent widget.
        result (str): The text content saved by the user.
    """

    def __init__(self,
                 master: Optional[tk.Tk] = None,
                 char_limit: int = 500,
                 width: int = 1000,
                 height: int = 600,
                 initial_text: Optional[str] = ""):
        """
        Initializes a new Editor instance.

        Args:
            master (Optional[tk.Tk]): The root window or parent widget. If not
            provided, a new Tk instance is created.
            char_limit (int): The maximum number of characters allowed in the
            text entry.
            width (int): The width of the window.
            height (int): The height of the window.
            initial_text (Optional[str]): The initial text to be displayed in
            the text entry widget.
        """
        if master is None:
            master = tk.Tk()
        super().__init__(master=master, bg="black")
        self.master: tk.Tk = master
        self.char_limit: int = char_limit
        self.result: str = ""
        self.initial_text: str = initial_text
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.center_window(width, height)
        self.text_entry.focus_set()

    def create_widgets(self) -> None:
        """
        Creates and packs the widgets for the text editor.
        This includes padding frames, labels, and the text entry widget.
        """
        self.left_padding = tk.Frame(self, bg="black", width=20)
        self.left_padding.pack(side="left", fill=tk.Y)

        self.right_padding = tk.Frame(self, bg="black", width=20)
        self.right_padding.pack(side="right", fill=tk.Y)

        self.label_skip_save = tk.Label(
            self, bg="black",
            text="Press 'Ctrl + S' to save or 'Escape' to skip",
            font=("Helvetica", 12), fg="cyan"
        )
        self.label_skip_save.pack(fill=tk.X)

        self.label_limit = tk.Label(
            self, bg="black",
            text=f"Text limit is {self.char_limit} symbols",
            font=("Helvetica", 10), fg="cyan"
        )
        self.label_limit.pack(fill=tk.X)

        custom_font = font.Font(family="Helvetica", size=14, weight="normal")
        self.text_entry = tk.Text(
            self, font=custom_font,
            bg="black", fg="cyan",
            insertbackground="cyan"
        )
        self.text_entry.pack(side="left", fill=tk.BOTH, expand=True)

        self.text_entry.insert(tk.END, self.initial_text)

        self.text_entry.bind("<KeyPress>", self.handle_keypress)

    def handle_keypress(self, event: tk.Event) -> Optional[str]:
        """
        Handles key press events, including enforcing the character limit and
        managing shortcuts.

        Args:
            event (tk.Event): The event object containing information about
            the key press.

        Returns:
            Optional[str]: Returns "break" to prevent further processing of
            the event if the character limit is exceeded.
        """
        current_text: str = self.text_entry.get("1.0", tk.END).strip()

        allowed_keys: list[str] = ['BackSpace', 'Delete',
                                   'Left', 'Right', 'Up',
                                   'Down', 'Home', 'End'
                                   ]
        if len(current_text) >= self.char_limit and \
                event.keysym not in allowed_keys:
            return "break"

        ctrl_key: int = 0x4
        s_key_code: int = 83
        escape_key_code: int = 27
        if (event.state & ctrl_key) and event.keycode == s_key_code:
            self.save_and_close(None)
        elif event.keycode == escape_key_code:
            self.exit_without_saving(None)

        return None

    def save_text(self) -> None:
        """
        Saves the current text from the text entry widget to the `result`
        attribute.
        """
        self.result = self.text_entry.get("1.0", tk.END).strip()

    def save_and_close(self, event: Optional[tk.Event]) -> None:
        """
        Saves the text and closes the application.

        Args:
            event (Optional[tk.Event]): The event object (unused).
        """
        self.save_text()
        self.master.quit()

    def exit_without_saving(self, event: Optional[tk.Event]) -> None:
        """
        Closes the application without saving the text.

        Args:
            event (Optional[tk.Event]): The event object (unused).
        """
        self.master.quit()

    def center_window(self, width: int, height: int) -> None:
        """
        Centers the application window on the screen.

        Args:
            width (int): The width of the window.
            height (int): The height of the window.
        """
        screen_width: int = self.master.winfo_screenwidth()
        screen_height: int = self.master.winfo_screenheight()
        x_coordinate: int = int((screen_width / 2) - (width / 2))
        y_coordinate: int = int((screen_height / 2) - (height / 2))
        self.master.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")
