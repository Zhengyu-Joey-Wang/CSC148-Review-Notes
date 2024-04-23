"""Prep 2 Synthesize

=== CSC148 Winter 2024 ===
Department of Mathematical and Computational Sciences,
University of Toronto Mississauga

=== Module Description ===
This module contains the documentation for a simple class. Your job is to
implement the class below according to its docstring; note this includes
both the *instance attributes* of the class and the *methods* we've documented.
"""
# Do not use any imports beyond the one below (randint)!
from random import randint


class Spinner:
    """A spinner for a board game.

    A spinner has a certain number of slots, numbered starting at 0 and
    increasing by 1 each slot. For example, if the spinner has 6 slots,
    they are numbered 0 through 5, inclusive.

    A spinner also has an arrow that points to one of these slots.

    === Attributes ===
    slots:
        The number of slots in this spinner.
    position:
        The slot number that the spinner's arrow is currently pointing to.

    === Sample Usage ===
    Creating a spinner:
    >>> s = Spinner(8)
    >>> s.position
    0

    Spinning the spinner:
    >>> s.spin(4)
    >>> s.position
    4
    >>> s.spin(2)
    >>> s.position
    6
    >>> s.spin(2)
    >>> s.position
    0
    """
    slots: int
    position: int

    def __init__(self, size: int) -> None:
        """Initialize a new spinner with <size> slots.

        A spinner's position always starts at 0.

        Precondition: size >= 1
        """
        self.slots = size
        self.position = 0

    def spin(self, force: int) -> None:
        """Spin this spinner, advancing the arrow <force> slots.

        The spinner wraps around once it reaches its maximum slot, starting
        back at 0. See the class docstring for an example of this.

        Precondition: force >= 0.

        Hint: use the "%" operator to "wrap around" the spinner's position.
        """
        temp = self.position + force
        self.position = temp % self.slots

    def spin_randomly(self) -> None:
        """Spin this spinner randomly.

        This modifies the spinner's arrow to point to a random slot on the
        spinner. Each slot has an equal chance of being pointed to.

        You MUST use randint (imported from random) for this method, to
        choose a random slot.
        """
        self.spin(randint(0, self.slots))


if __name__ == '__main__':
    # When you run the module, you'll both run doctest and python_ta
    # to check your work.
    import doctest

    doctest.testmod()

    # python_ta opens up your web browser to display its report.
    # You want to see "None!" under both "Code Errors" and
    # "Style and Convention Errors" for full marks.
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['random']
    })
