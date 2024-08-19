"""
Input error decorator module.
"""

from typing import Callable


def input_error(func: Callable) -> Callable:
    """
    Decorator that catches exceptions and returns an appropriate message.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The decorated function.
    """

    def inner(*args, **kwargs):
        """
        The inner function that catches exceptions and returns an appropriate
        message.

        Args:
            *args: The positional arguments passed to the function.
            **kwargs: The keyword arguments passed to the function.

        Returns:
            str: Error message.
        """
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)

    return inner
