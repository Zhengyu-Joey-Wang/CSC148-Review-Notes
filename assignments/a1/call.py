"""
CSC148, Winter 2024
Assignment 1

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Bogdan Simion, Diane Horton, Jacqueline Smith
"""
import datetime
import os
from typing import Optional
import pygame


# Sprite files to display the start and end of a call
START_CALL_SPRITE = 'data/call-start-2.png'
END_CALL_SPRITE = 'data/call-end-2.png'


# ----------------------------------------------------------------------------
# NOTE: You do not need to understand the implementation of the Drawable class
# to be able to solve this assignment. However, feel feel free to read it for
# the fun of understanding the visualization system.
# ----------------------------------------------------------------------------

class Drawable:
    """A class for objects that the graphical renderer can draw.

    === Public Attributes ===
    sprite:
        image object for this drawable or None.
        If none, then must have linelimits
    linelimits:
        limits for the line of the connection or None.
        If none, then must have sprite
    loc: location (longitude/latitude pair)
    """
    sprite: Optional[pygame.Surface]
    linelimits: Optional[tuple[float, float]]
    loc: Optional[tuple[float, float]]

    def __init__(self, sprite_file: Optional[str] = None,
                 location: Optional[tuple[float, float]] = None,
                 linelimits: Optional[tuple[tuple[float, float],
                                            tuple[float, float]]] = None) \
            -> None:
        """Initialize this drawable object with the <sprite_file>, <location>
        and <linelimits>.
        """
        self.linelimits = None
        self.sprite = None
        self.loc = None

        if sprite_file is not None and location is not None:
            self.sprite = pygame.transform.smoothscale(
                pygame.image.load(os.path.join(os.path.dirname(__file__),
                                               sprite_file)), (13, 13))
            self.loc = location
        else:
            self.linelimits = linelimits

    def get_position(self) -> tuple[float, float]:
        """Return the (long, lat) position of this object at the given time.
        """
        return self.loc

    def get_linelimits(self) -> Optional[tuple[float, float]]:
        """Return the limits for the line if the drawable is a line type
        (otherwise None)
        """
        return self.linelimits


class Call:
    """ A call made by a customer to another customer.

    === Public Attributes ===
    src_number:
         source number for this Call
    dst_number:
         destination number for this Call
    time:
         date and time of this Call
    duration:
         duration in seconds for this Call
    src_loc:
         location of the source of this Call; a Tuple containing the longitude
         and latitude coordinates
    dst_loc:
         location of the destination of this Call; a Tuple containing the
         longitude and latitude coordinates
    drawables:
         sprites for drawing the source and destination of this Call
    connection:
         connecting line between the two sprites representing the source and
         destination of this Call

    === Representation Invariants ===
    -   duration >= 0
    """
    src_number: str
    dst_number: str
    time: datetime.datetime
    duration: int
    src_loc: tuple[float, float]
    dst_loc: tuple[float, float]
    drawables: list[Drawable]
    connection: Drawable

    def __init__(self, src_nr: str, dst_nr: str,
                 calltime: datetime.datetime, duration: int,
                 src_loc: tuple[float, float], dst_loc: tuple[float, float]) \
            -> None:
        """ Create a new Call object with the given parameters.
        """
        self.src_number = src_nr
        self.dst_number = dst_nr
        self.time = calltime
        self.duration = duration
        self.src_loc = src_loc
        self.dst_loc = dst_loc
        self.drawables = [Drawable(sprite_file=START_CALL_SPRITE,
                                   location=src_loc),
                          Drawable(sprite_file=END_CALL_SPRITE,
                                   location=dst_loc)]

        self.connection = Drawable(linelimits=(src_loc, dst_loc))

    def get_bill_date(self) -> tuple[int, int]:
        """ Return the billing date for this Call, as a tuple containing the
        month and the year
        """
        return self.time.month, self.time.year

    # ----------------------------------------------------------
    # NOTE: You do not need to understand the implementation of
    # the following methods, to be able to solve this assignment
    # but feel free to read them to get a sense of what these do.
    # ----------------------------------------------------------

    def get_drawables(self) -> list[Drawable]:
        """ Return the list of drawable sprites for this Call
        """
        return self.drawables

    def get_connection(self) -> Drawable:
        """ Return the connecting line for this Call start and end locations
        """
        return self.connection

    def __str__(self) -> str:
        """ Return the string representation of a Call"""
        return "srcnum" + self.src_number + "srcdst" + self.dst_number + "time"\
            + str(self.time) + "dur" + str(self.duration) + "srcloc"\
            + str(self.src_loc) + "dstloc" + str(self.dst_loc)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'datetime', 'os', 'pygame'
        ],
        'disable': ['R0902', 'R0913'],
        'generated-members': 'pygame.*'
    })
