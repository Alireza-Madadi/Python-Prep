import pygame
import sys
import consts
from cell import Cell

class GameManager:
    """
    Manages the core game state, grid, and logic.
    
    This class holds the 2D grid of Cells, manages all snakes,
    and handles game events like movement, collision, and fruit spawning.
    It is also responsible for drawing the entire game state.
    """
    def __init__(self, size, screen, sx, sy, block_cells):
        """
        Initializes the game grid and state.

        Args:
            size (int): The size of the grid (size x size).
            screen (pygame.Surface): The main screen surface for drawing.
            sx (int): The screen x-coordinate offset for the grid.
            sy (int): The screen y-coordinate offset for the grid.
            block_cells (list[list]): A list of [x, y] coordinates for obstacles.
        """
        self.screen = screen
        self.size = size
        self.cells = []
        self.sx = sx
        self.sy = sy
        self.snakes = list()
        self.turn = 0
        
        # Create the 2D grid of Cell objects
        for i in range(self.size):
            tmp = []
            for j in range(self.size):
                tmp.append(Cell(screen, sx + i * consts.cell_size, sy + j * consts.cell_size))
            self.cells.append(tmp)
            
        # Place the obstacle blocks
        for cell_pos in block_cells:
            cell = self.get_cell(cell_pos)
            if cell:
                cell.set_color(consts.block_color)

    def add_snake(self, snake):
        """Adds a new snake to the game manager."""
        self.snakes.append(snake)

    def get_cell(self, pos):
        """
        Safely retrieves a cell from the grid.

        Args:
            pos (tuple): (x, y) coordinates of the cell.

        Returns:
            Cell | None: The Cell object if coordinates are valid, otherwise None.
        """
        try:
            # Note: Grid is accessed [x][y]
            return self.cells[pos[0]][pos[1]]
        except IndexError:
            return None

    def kill(self, killed_snake):
        """Removes a snake from the game (e.g., after a collision)."""
        if killed_snake in self.snakes:
            self.snakes.remove(killed_snake)

    def draw_grid(self):
        """
        Draws the entire game grid by calling draw() on every cell.
        This is called once per frame from the main game loop.
        """
        for i in range(self.size):
            for j in range(self.size):
                self.get_cell((i, j)).draw()

    def find_best_fruit_pos(self):
        """
        Finds the empty cell that is furthest from any existing object
        (snake, block, or other fruit) to spawn a new fruit.
        
        Returns:
            tuple: (x, y) coordinates for the new fruit, or (-1, -1) if no spot is found.
        """
        mx = -1
        pos = (-1, -1)
        for i in range(self.size):
            for j in range(self.size):
                # Only consider empty cells
                if not self.get_cell((i, j)).is_empty():
                    continue
                    
                # Find the minimum distance to any non-empty cell
                mn = self.size * 3 # Initialize with a large number
                for x in range(self.size):
                    for y in range(self.size):
                        if not self.get_cell((x, y)).is_empty():
                            dist = abs(j - y) + abs(i - x) # Manhattan distance
                            mn = min(mn, dist)
                
                # If this cell's min distance is the largest we've seen,
                # it's our new best spot.
                if mn > mx:
                    mx = mn
                    pos = (i, j)
        return pos

    def handle(self, keys):
        """
        Main game logic step, called once per frame (or tick).
        
        Args:
            keys (list): A list of all keypresses received from all clients.
        """
        # 1. Handle input for all snakes
        for snake in self.snakes:
            snake.handle(keys)
            
        # 2. Move all snakes
        for snake in self.snakes:
            snake.next_move()

        # 3. Handle fruit spawning
        self.turn += 1
        if self.turn % 10 == 0: # Spawn a fruit every 10 turns
            pos = self.find_best_fruit_pos()
            if pos != (-1, -1):
                cell = self.get_cell(pos)
                if cell and cell.is_empty(): # Final check
                    cell.set_color(consts.fruit_color)

