import pygame
import consts

class Cell:
    """
    Represents a single cell in the game grid.
    
    This class is a data container for the cell's position, size,
    and current color. It is no longer responsible for drawing itself;
    that logic is now handled by the GameManager.
    """
    def __init__(self, surface, sx, sy, color=consts.back_color):
        """
        Initializes the Cell object.

        Args:
            surface (pygame.Surface): The main screen surface (used for drawing).
            sx (int): The screen x-coordinate (top-left).
            sy (int): The screen y-coordinate (top-left).
            color (tuple, optional): The initial color. Defaults to back_color.
        """
        self.surface = surface
        self.sx = sx
        self.sy = sy
        self.size = consts.cell_size
        self.color = color

    def set_color(self, color):
        """
        Updates the color of the cell.
        
        This method only updates the internal state. It does not
        draw to the screen.

        Args:
            color (tuple): The new (R, G, B) color tuple.
        """
        self.color = color

    def draw(self):
        """
        Draws the cell (both interior and border) to the surface.
        This should be called by the GameManager during the main draw loop.
        """
        # Draw the cell's interior
        pygame.draw.rect(self.surface, self.color, (self.sx + 1, self.sy + 1, self.size - 2, self.size - 2))
        # Draw the cell's border
        pygame.draw.rect(self.surface, (0, 0, 0), (self.sx, self.sy, self.size, self.size), 1)

    def is_empty(self):
        """Checks if the cell is empty (i.e., background color)."""
        return self.color == consts.back_color

    def is_fruit(self):
        """Checks if the cell contains a fruit."""
        return self.color == consts.fruit_color

