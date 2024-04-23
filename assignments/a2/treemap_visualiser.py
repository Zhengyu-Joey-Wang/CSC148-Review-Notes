"""
Assignment 2: Treemap Visualiser

=== CSC148 Winter 2024 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2024 Bogdan Simion, David Liu, Diane Horton,
                   Haocheng Hu, Jacqueline Smith

=== Module Description ===
This module contains the main program code for the treemap visualisation.
It is responsible for initializing an instance of TMTree (using a
concrete subclass, of course), rendering it to the user using pygame,
and detecting user events like mouse clicks and key presses and responding
to them.
"""

from os import getcwd
from sys import platform
from typing import Optional

import pygame

from papers import PaperTree
from tm_trees import TMTree, FileSystemTree


class Visualiser:
    """
    A class that uses pygame to visualise a tm_tree object.
    """
    width: int
    height: int
    font_height: int
    tree: Optional[TMTree]
    screen: Optional[pygame.Surface]
    hover_node: Optional[TMTree]
    selected_node: Optional[TMTree]

    def __init__(self) -> None:
        # You may adjust the height and width as you'd like, depending on your screen resolution
        self.width = 1200
        self.height = 700

        self.font_height = 30

        self.tree = None
        self.screen = None
        self.hover_node = None
        self.selected_node = None

    def run_visualisation(self, tree: TMTree) -> None:
        """Display an interactive graphical display of the given tree's treemap.
        """

        # Setup pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.tree = tree

        # Render the initial display of the static treemap.
        self.render_display()
        tree.update_rectangles((0, 0, self.width, self.height - self.font_height))

        # Start an event loop to respond to events.
        self.event_loop()

    def render_display(self) -> None:
        """Render a treemap and text display to the given screen.

        Use the constants TREEMAP_HEIGHT and FONT_HEIGHT to divide the
        screen vertically into the treemap and text comments.
        """
        # First, clear the screen
        pygame.draw.rect(self.screen, pygame.Color('black'),
                         (0, 0, self.width, self.height))

        try:
            subscreen = self.screen.subsurface((0, 0, self.width, self.height - self.font_height))
        except ValueError:
            return

        # TODO: Uncomment this after you have completed Task 2
        for rect, colour in self.tree.get_rectangles():
            # Note that the arguments are in the opposite order
            pygame.draw.rect(subscreen, colour, rect)
        
        # add the hover rectangle
        if self.selected_node is not None:
            pygame.draw.rect(subscreen, (255, 255, 255), self.selected_node.rect, 4)
        if self.hover_node is not None:
            pygame.draw.rect(subscreen, (255, 255, 255), self.hover_node.rect, 2)
        
        self._render_text()

        # This must be called *after* all other pygame functions have run.
        pygame.display.flip()

    def _render_text(self) -> None:
        """Render text at the bottom of the display.
        """
        # The font we want to use
        font = pygame.font.SysFont('Consolas', self.font_height - 8)
        text_surface = font.render(self._get_display_text(), True, pygame.Color('white'))

        # Where to render the text_surface
        text_pos = (0, self.height - self.font_height + 4)
        self.screen.blit(text_surface, text_pos)

    def event_loop(self) -> None:
        """Respond to events (mouse clicks, key presses) and update the display.

        Note that the event loop is an *infinite loop*: it continually waits for
        the next event, determines the event's type, and then updates the state
        of the visualisation or the tree itself, updating the display if necessary.
        This loop ends only when the user closes the window.
        """
        selected_node = self.tree

        while True:
            # Wait for an event
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.VIDEORESIZE:
                self.width = int(event.w) if event.w else self.width
                self.height = int(event.h) if event.h else self.height
                self.run_visualisation(self.tree)
                return

            # get the hover position and the corresponding node
            hover_node = self.tree.get_tree_at_position(pygame.mouse.get_pos())

            if event.type == pygame.MOUSEBUTTONUP:
                selected_node = \
                    self._handle_click(event.button, event.pos, selected_node)

            elif event.type == pygame.KEYUP and selected_node is not None:
                drawable_height = self.height - self.font_height
                k = event.key
                if k == pygame.K_UP:
                    selected_node.change_size(0.01)
                    self.tree.update_data_sizes()
                    self.tree.update_rectangles((0, 0, self.width, drawable_height))

                elif k == pygame.K_DOWN:
                    selected_node.change_size(-0.01)
                    self.tree.update_data_sizes()
                    self.tree.update_rectangles((0, 0, self.width, drawable_height))

                elif k == pygame.K_DELETE or platform == 'darwin' and k == pygame.K_BACKSPACE:
                    if selected_node.delete_self():
                        self.tree.update_data_sizes()
                        self.tree.update_rectangles((0, 0, self.width, drawable_height))
                        selected_node = None

                elif k == pygame.K_m:
                    selected_node.move(hover_node)
                    self.tree.update_data_sizes()
                    self.tree.update_rectangles((0, 0, self.width, drawable_height))
                    selected_node = hover_node

                elif k == pygame.K_e:
                    selected_node.expand()
                    selected_node = None

                elif k == pygame.K_a:
                    selected_node.expand_all()
                    selected_node = None

                elif k == pygame.K_c:
                    selected_node.collapse()
                    if selected_node is not self.tree:
                        selected_node = selected_node.get_parent()

                elif k == pygame.K_x:
                    selected_node.collapse_all()
                    selected_node = self.tree

                elif k == pygame.K_q and selected_node is not self.tree:
                    self.run_visualisation(selected_node)
                    return

            if event.type == pygame.KEYUP and event.key == pygame.K_b:
                if self.tree.get_parent():
                    self.tree.get_parent().collapse_all()
                    self.run_visualisation(self.tree.get_parent())
                    return

            self.selected_node = selected_node
            self.hover_node = hover_node

            # Update display
            self.render_display()

    def _handle_click(self, button: int, pos: tuple[int, int],
                      old_selected_leaf: Optional[TMTree]) -> Optional[TMTree]:
        """Return the new selection after handling the mouse event.

        We need to use old_selected_leaf to handle the case when the selected
        leaf is left-clicked again.
        """

        # left mouse click
        if button == 1:
            selected_leaf = self.tree.get_tree_at_position(pos)
            if selected_leaf is None:
                return old_selected_leaf
            elif selected_leaf is old_selected_leaf:
                return None
            else:
                # if selected_leaf._name == 'online, remote or MOOC delivery, DSA PS':
                # print(selected_leaf._name)
                # print(f"size: {selected_leaf.data_size}")
                # print(f"rect: {selected_leaf.rect}")
                return selected_leaf
        # right click or any other click does nothing
        else:
            return old_selected_leaf

    def _get_display_text(self) -> str:
        """Return the display text of this leaf.
        """

        leaf = self.selected_node
        if leaf is None:
            return ''
        else:
            leaf_path = leaf.get_path_string()

            while len(leaf_path + leaf.get_suffix()) > self.width // 13:
                components = leaf_path.split(leaf.get_separator())
                longest = max(len(s) for s in components)
                if longest <= 3:
                    break
                components = [i[:-3] + '..' if len(i) == longest
                              else i for i in components]
                leaf_path = leaf.get_separator().join(components)
            return leaf_path + leaf.get_suffix()


def run_treemap_file_system(path: str) -> None:
    """Run a treemap visualisation for the given path's file structure.
    Precondition: <path> is a valid path to a file or folder.
    """
    instructions = '\n==== Instructions for use ====\n' \
                   'When a folder/file is selected, the following keys can be pressed:\n' \
                   '"E" to expand the folder\n' \
                   '"A" to expand the folder and all folders inside\n' \
                   '"C" to collapse the parent folder\n' \
                   '"X" to collapse the entire display\n' \
                   '"Q" to visualize the selected folder/file\n' \
                   '"B" to go back to parent folder (if Q was pressed)\n' \
                   '"Up" and "Down" arrow keys to change the size of a file (in visualization)\n' \
                   '"M" to move a file (while selecting a file and hovering over a folder)\n' \
                   '"Del" to delete a file or folder from the visualization\n' \
                   '(Drag window to resize)'
    file_tree = FileSystemTree(path)
    print(instructions)
    visualizer.run_visualisation(file_tree)


def run_treemap_papers() -> None:
    """Run a treemap visualization for CS Education research papers data.

    You can try changing the value of the named argument by_year, but the
    others should stay the same.
    """
    paper_tree = PaperTree('CS1', [], all_papers=True, by_year=True)
    visualizer.run_visualisation(paper_tree)


if __name__ == '__main__':
    visualizer = Visualiser()
    # PATH_TO_VISUALISE = 'C:\\电脑文件\\文件\\大一\\CSC148\\assignments\\a2\\example-directory'  # enter a custom path here if you wish
    # PATH_TO_VISUALISE = 'C:\\电脑文件\\文件\\大一\\CSC148'
    # run_treemap_file_system(PATH_TO_VISUALISE or getcwd())
    run_treemap_papers()
