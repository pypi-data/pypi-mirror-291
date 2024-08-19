from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style


class CustomCompleter(Completer):
    """
    Custom CLI completter
    """

    def __init__(self, commands: list, all_commands: bool = False) -> None:
        super().__init__()
        self.commands = commands
        self.all_commands = all_commands

    def get_completions(self, document, complete_event):
        for command in self.commands:
            if (
                command[: len(document.current_line)] != document.current_line
                and not self.all_commands
            ):
                continue
            yield Completion(
                command,
                start_position=-len(document.current_line),
                style="bg:green fg:ansiblack",
                selected_style="fg:lightcyan bg:ansiblack",
            )


class Prompt():
    """
    Custom prompt
    """
    def __init__(self, mouse_support=False) -> None:
        self.session = PromptSession()
        self.mouse_support = mouse_support

    def prompt(self,
               message: str,
               commands: list,
               all_commands: bool = False,
               style: str = '') -> str:
        """
        Provide CLI prompt and return entered data
        """
        color_style = Style.from_dict({'prompt': style})
        return self.session.prompt(
                    message=[('class:prompt', message)],
                    completer=CustomCompleter(commands, all_commands),
                    style=color_style,
                    mouse_support=self.mouse_support
                )
