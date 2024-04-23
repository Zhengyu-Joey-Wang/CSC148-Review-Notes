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

=== Module Description ===

This file contains the Visualizer class, which is responsible for interacting
with Pygame, the graphics library we're using for this assignment.
There's quite a bit in this file, but you aren't responsible for most of it.

It also contains the Map class, which is responsible for converting between
longitude/latitude coordinates and pixel coordinates on the pygame window.

DO NOT CHANGE ANY CODE IN THIS FILE, unless instructed in the handout.
"""
import math
import os
import threading
import time
from tkinter import *
from typing import Optional, Union, Callable, Any

import pygame

from call import Drawable, Call
from customer import Customer
from filter import Filter, DurationFilter, CustomerFilter, LocationFilter, ResetFilter

# ----------------------------------------------------------------------------
# NOTE: You do not need to understand any of the visualization details from
# this module, to be able to solve this assignment. However, feel free to read
# it for the fun of understanding the visualization system.
# ----------------------------------------------------------------------------

WHITE = (255, 255, 255)
LINE_COLOUR = (0, 64, 125)

MAP_FILE = 'data/toronto_map.png'
# Map upper-left and bottom-right coordinates (long, lat).
MAP_MIN = (-79.697878, 43.799568)
MAP_MAX = (-79.196382, 43.576959)

# Window size
SCREEN_SIZE = (1000, 700)

# Thread settings for Task 5
NUM_THREADS = 1


def get_filter(unicode: str) -> Optional[Filter]:
    """Returns the filter class to use"""
    unicode = unicode.lower()
    if unicode == "d":
        return DurationFilter()
    elif unicode == "l":
        return LocationFilter()
    elif unicode == "c":
        return CustomerFilter()
    elif unicode == "r":
        return ResetFilter()
    return None


class Visualizer:
    """Visualizer for the current state of a simulation.

    === Public attributes ===
    r: the Tk object for the main window
    """
    # === Private attributes ===
    # _screen: the pygame window that is shown to the user.
    # _mouse_down: whether the user is holding down a mouse button
    #   on the pygame window.
    # _map: the Map object responsible for converting between longitude/latitude
    #   coordinates and the pixels of the visualization window.
    _uiscreen: pygame.Surface
    _screen: pygame.Surface
    _mouse_down: bool
    _map: 'Map'
    _quit: bool
    r: Tk

    def __init__(self) -> None:
        """Initialize this visualization.
        """
        self.r = Tk()
        Label(self.r, text="Welcome to MewbileTech phone management system") \
            .grid(row=0, column=0)
        self.r.title("MewbileTech management system")
        pygame.init()

        self._uiscreen = pygame.display.set_mode(
            (SCREEN_SIZE[0] + 200, SCREEN_SIZE[1]),
            pygame.HWSURFACE | pygame.DOUBLEBUF)

        # Add the text along the side, displaying the command keys for filters
        self._uiscreen.fill((125, 125, 125))
        font = pygame.font.SysFont(None, 25)
        self._uiscreen.blit(font.render("FILTER KEYBINDS", True, WHITE),
                            (SCREEN_SIZE[0] + 10, 50))
        self._uiscreen.blit(font.render("C: customer ID", True, WHITE),
                            (SCREEN_SIZE[0] + 10, 100))
        self._uiscreen.blit(font.render("D: duration", True, WHITE),
                            (SCREEN_SIZE[0] + 10, 150))
        self._uiscreen.blit(font.render("L: location", True, WHITE),
                            (SCREEN_SIZE[0] + 10, 200))
        self._uiscreen.blit(font.render("R: reset filter", True, WHITE),
                            (SCREEN_SIZE[0] + 10, 250))

        self._uiscreen.blit(font.render("M: monthly bill", True, WHITE),
                            (SCREEN_SIZE[0] + 10, 500))
        self._uiscreen.blit(font.render("X: quit application", True, WHITE),
                            (SCREEN_SIZE[0] + 10, 650))

        self._screen = self._uiscreen.subsurface((0, 0), SCREEN_SIZE)
        self._screen.fill(WHITE)
        self._mouse_down = False
        self._map = Map(SCREEN_SIZE)

        # Initial render
        self.render_drawables([])
        self._quit = False

    def render_drawables(self, drawables: list[Drawable]) -> None:
        """Render the <drawables> to the screen
        """
        # Draw the background map onto the screen
        self._screen.fill(WHITE)
        self._screen.blit(self._map.get_current_view(), (0, 0))

        # Add all of the objects onto the screen
        self._map.render_objects(drawables, self._screen)

        # Show the new image
        pygame.display.flip()

    def has_quit(self) -> bool:
        """Returns if the program has received the quit command
        """
        return self._quit

    def set_event_button_motion(self) -> None:
        """pan's the map if the _mouse_down is true
        """
        if self._mouse_down:
            self._map.pan(pygame.mouse.get_rel())
        else:
            pygame.mouse.get_rel()
        return None

    def set_event_button_down(self, button: int) -> None:
        """Takes the event button when button is pressed
        and sets the behaviour on the map or mouse
        """
        if button == 1:
            self._mouse_down = True
        elif button == 4:
            self._map.zoom(-0.1)
        elif button == 5:
            self._map.zoom(0.1)
        return None

    def handle_window_events(self, customers: list[Customer],
                             drawables: list[Call]) \
            -> list[Call]:
        """Handle any user events triggered through the pygame window.
        The <drawables> are the objects currently displayed, while the
        <customers> list contains all customers from the input data.
        Return a new list of Calls, according to user input actions.
        """
        new_drawables = drawables
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit = True
            elif event.type == pygame.KEYDOWN and event.unicode.lower() == 'x':
                self._quit = True
            elif event.type == pygame.KEYDOWN:
                f = get_filter(event.unicode)

                if f is not None:
                    def result_wrapper(fun: Callable[[list[Customer],
                                                      list[Call],
                                                      str], list[Call]],
                                       customers: list[Customer],
                                       data: list[Call],
                                       filter_string: str,
                                       res: list) -> None:
                        """A final wrapper to return the result of the operation
                        """
                        res.append(fun(customers, data, filter_string))

                    def threading_wrapper(customers: list[Customer],
                                          data: list[Call],
                                          filter_string: str) -> list[Call]:
                        """A wrapper for the application of filters with
                        threading
                        """
                        chk_cls = math.ceil(
                            (len(data) + NUM_THREADS - 1) / NUM_THREADS)
                        print("Num_threads:", NUM_THREADS)
                        print("Chunk_calls:", chk_cls)
                        threads = []
                        results = []
                        for i in range(NUM_THREADS):
                            res = []
                            results.append(res)
                            t = threading.Thread(target=result_wrapper,
                                                 args=(f.apply,
                                                       customers,
                                                       data[i * chk_cls:
                                                            (i + 1) * chk_cls],
                                                       filter_string,
                                                       res))
                            t.daemon = True
                            t.start()
                            threads.append(t)
                            # f.apply(customers, data, filter_string)
                        # Wait to finish
                        for t in threads:
                            t.join()

                        # Now reconstruct the data
                        new_data = []
                        for res in results:
                            new_data.extend(res[0])
                        return new_data

                    new_drawables = self.entry_window(str(f),
                                                      customers,
                                                      drawables,
                                                      threading_wrapper)

                # Perform the billing for a selected customer:
                if event.unicode == "m":
                    try:

                        def get_customer(customers: list[Customer],
                                         found_customer: list[Customer],
                                         input_string: str) -> None:
                            """ A helper to find the customer specified in the
                            input string appends to the found_customer the
                            matching customer
                            """
                            try:
                                for c in customers:
                                    if c.get_id() == int(input_string):
                                        found_customer.append(c)
                            except ValueError:
                                pass

                        customer = []
                        self.entry_window("Generate the bill for the customer "
                                          "with ID:", customers, customer,
                                          get_customer)

                        if len(customer) == 0:
                            raise ValueError

                        # Just want to return the parsed input string
                        def get_input_date(customer: list[Customer],
                                           drawables: list[Call],
                                           input_string: str) \
                                -> Optional[list[int]]:
                            """ A helper to get the input date """
                            try:
                                return [int(s.strip())
                                        for s in input_string.split(',')]
                            except ValueError:
                                return None

                        date = self.entry_window("Bill month and year: "
                                                 "month, year",
                                                 customers,
                                                 drawables,
                                                 get_input_date)
                        if date is None or date == ([], []):
                            raise ValueError

                        customer[0].print_bill(date[0], date[1])

                    except ValueError:
                        print("ERROR: bad formatting for input string")
                    except IndexError:
                        print("Customer not found")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.set_event_button_down(event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._mouse_down = False
            elif event.type == pygame.MOUSEMOTION:
                self.set_event_button_motion()
        return new_drawables

    def entry_window(self, field: str,
                     customers: list[Customer],
                     drawables: Union[list[Customer],
                                      list[Call]],
                     callback: Callable[[list[Customer],
                                         list[Call],
                                         str],
                                        list[Call]]) \
            -> Union[list[Call], list[Any]]:
        """ Creates a pop-up window for the user to enter input text, and
        applies the <callback> function onto the <drawables>
        """
        new_drawables = []
        m = Tk()
        m.title("Filter")
        Label(m, text=field).grid(row=0)

        el = Entry(m)
        # No textbox for filter string if it's a Reset filter
        if field != "Reset all of the filters applied so far, if any":
            el.grid(row=0, column=1)

        # The callback function:
        def callback_wrapper(input_string: str) -> None:
            """ A wrapper to call the callback function on the <input_string>
            and print the time taken for the function to execute.
            """
            nonlocal new_drawables
            nonlocal m
            t1 = time.time()
            new_drawables = callback(customers, drawables, input_string)
            t2 = time.time()
            print("Time elapsed:  " + str(t2 - t1))
            m.destroy()

        Button(m, text="Apply Filter",
               command=lambda:
               callback_wrapper(el.get()
                                if field != "Reset all of the filters applied "
                                            "so far, if any"
                                else "")).grid(row=1, column=0,
                                               sticky=W, pady=5)
        m.mainloop()
        print("FILTER APPLIED")
        return new_drawables


class Map:
    """ Window panning and zooming interface.

    === Public attributes ===
    image:
        the full image for the area to cover with the map
    min_coords:
        the minimum long/lat coordinates
    max_coords:
        the maximum long/lat coordinates
    screensize:
        the dimensions of the screen
    """
    # === Private attributes ===
    # _xoffset:
    #    offset on x axis
    # _yoffset:
    #    offset on y axis
    # _zoom:
    #    map zoom level
    image: pygame.image
    min_coords: tuple[float, float]
    max_coords: tuple[float, float]
    screensize: tuple[int, int]
    _xoffset: int
    _yoffset: int
    _zoom: int

    def __init__(self, screendims: tuple[int, int]) -> None:
        """ Initialize this map for the given screen dimensions <screendims>.
        """
        self.image = pygame.image.load(
            os.path.join(os.path.dirname(__file__), MAP_FILE))
        self.min_coords = MAP_MIN
        self.max_coords = MAP_MAX

        self._xoffset = 0
        self._yoffset = 0
        self._zoom = 1
        self.screensize = screendims

    def render_objects(self, drawables: list[Drawable],
                       screen: pygame.Surface) -> None:
        """ Render the <drawables> onto the <screen>.
        """
        for drawable in drawables:
            longlat_position = drawable.get_position()
            if longlat_position is not None:
                sprite_position = self._longlat_to_screen(longlat_position)
                screen.blit(drawable.sprite, sprite_position)
            else:  # is a line segment
                endpoints = drawable.get_linelimits()
                pygame.draw.aaline(screen,
                                   LINE_COLOUR,
                                   self._longlat_to_screen(endpoints[0]),
                                   self._longlat_to_screen(endpoints[1]))

    def _longlat_to_screen(self,
                           location: tuple[float, float]) -> tuple[int, int]:
        """ Convert the <location> long/lat coordinates into pixel coordinates.
        """
        x = round((location[0] - self.min_coords[0])
                  / (self.max_coords[0] - self.min_coords[0])
                  * self.image.get_width())
        y = round((location[1] - self.min_coords[1])
                  / (self.max_coords[1] - self.min_coords[1])
                  * self.image.get_height())

        x = round((x - self._xoffset) * self._zoom * self.screensize[0]
                  / self.image.get_width())
        y = round((y - self._yoffset) * self._zoom * self.screensize[1]
                  / self.image.get_height())
        return x, y

    def pan(self, dp: tuple[int, int]) -> None:
        """ Pan the view in the image by <dp> (dx, dy) screenspace pixels.
        """
        self._xoffset -= dp[0]
        self._yoffset -= dp[1]
        self._clamp_transformation()

    def zoom(self, dx: float) -> None:
        """ Zoom the view by <dx> amount.

        The centre of the zoom is the top-left corner of the visible region.
        """
        if (self._zoom >= 4 and dx > 0) or (self._zoom <= 1 and dx < 0):
            return

        self._zoom += dx
        self._clamp_transformation()

    def _clamp_transformation(self) -> None:
        """ Ensure that the transformation parameters are within a fixed range.
        """
        raw_width = self.image.get_width()
        raw_height = self.image.get_height()
        zoom_width = round(raw_width / self._zoom)
        zoom_height = round(raw_height / self._zoom)

        self._xoffset = min(raw_width - zoom_width, max(0, self._xoffset))
        self._yoffset = min(raw_height - zoom_height, max(0, self._yoffset))

    def get_current_view(self) -> pygame.Surface:
        """ Get the subimage to display to screen from the map.
        """
        raw_width = self.image.get_width()
        raw_height = self.image.get_height()
        zoom_width = round(raw_width / self._zoom)
        zoom_height = round(raw_height / self._zoom)

        mapsegment = self.image.subsurface(((self._xoffset, self._yoffset),
                                            (zoom_width, zoom_height)))
        return pygame.transform.smoothscale(mapsegment, self.screensize)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'typing',
            'tkinter', 'os', 'pygame',
            'threading', 'math', 'time',
            'customer', 'call', 'filter',
        ],
        'allowed-io': [
            'entry_window', 'callback_wrapper', 'threading_wrapper',
            '__init__', 'handle_window_events'
        ],
        'disable': ['R0915', 'W0613', 'W0401', 'R0201'],
        'generated-members': 'pygame.*'
    })
