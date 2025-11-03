import consts

class Snake:
    """
    Represents a single Snake in the game.
    
    Handles its own movement logic, key inputs, and collision detection.
    """
    
    # Direction vectors for movement logic
    dx = {'UP': 0, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 1}
    dy = {'UP': -1, 'DOWN': 1, 'LEFT': 0, 'RIGHT': 0}
    
    # Opposite directions to prevent 180-degree turns
    opposite = {"DOWN": "UP", "UP": "DOWN", "LEFT": "RIGHT", "RIGHT": "LEFT"}

    def __init__(self, keys, game, pos, color, direction):
        """
        Initializes the Snake.

        Args:
            keys (dict): The key mapping for this snake (e.g., {'w': 'UP'}).
            game (GameManager): The main game manager object.
            pos (tuple): The starting (x, y) coordinates.
            color (tuple): The (R, G, B) color tuple for this snake.
            direction (str): The initial direction ("UP", "DOWN", ...).
        """
        self.keys = keys
        self.cells = [pos] # The snake is a list of (x, y) cells
        self.game = game
        self.game.add_snake(self)
        self.color = color
        self.direction = direction
        
        # Set the color of the starting cell
        cell = game.get_cell(pos)
        if cell:
            cell.set_color(color)

    def get_head(self):
        """Returns the (x, y) coordinates of the snake's head."""
        return self.cells[-1]

    def wrap_around_grid(self, x):
        """Wraps a coordinate around the grid if it goes out of bounds."""
        if x < 0:
            x += self.game.size # Wrap to the right side
        if x >= self.game.size:
            x -= self.game.size # Wrap to the left side
        return x

    def next_move(self):
        """
        Calculates and performs the snake's next move.
        
        This involves:
        1. Calculating the new head position.
        2. Checking for collisions (walls, self, other snakes, fruit).
        3. Moving the snake (adding a new head, removing the tail).
        """
        cx, cy = self.get_head()
        
        # Calculate new head position based on current direction
        cx = self.wrap_around_grid(cx + Snake.dx[self.direction])
        cy = self.wrap_around_grid(cy + Snake.dy[self.direction])

        next_cell = self.game.get_cell((cx, cy))
        
        if not next_cell:
            # This should not happen with wrap_around_grid, but as a safeguard
            self.game.kill(self)
            return

        next_color = next_cell.color
        
        if next_color == consts.fruit_color:
            # 1. Collision with fruit: Grow
            self.cells.append((cx, cy))
            next_cell.set_color(self.color)
        elif next_color == consts.back_color:
            # 2. No collision: Move normally
            self.cells.append((cx, cy))
            tailx, taily = self.cells.pop(0) # Remove the tail
            next_cell.set_color(self.color)
            self.game.get_cell((tailx, taily)).set_color(consts.back_color)
        else:
            # 3. Collision with wall or other snake: Die
            self.game.kill(self)

    def handle(self, keys):
        """
        Processes a list of key presses to update the snake's direction.
        
        It finds the first valid key for this snake and changes direction,
        ignoring invalid (180-degree) moves.

        Args:
            keys (list): A list of all keys pressed this frame (e.g., ['w', 'j']).
        """
        for key in keys:
            if key in self.keys:
                new_direction = self.keys[key]
                # Prevent the snake from reversing onto itself
                if new_direction != Snake.opposite[self.direction]:
                    self.direction = new_direction
                    break # Only process one key press per snake per frame

