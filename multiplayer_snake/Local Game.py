import pygame
import consts
import sys
from game_manager import GameManager
from snake import Snake

def main():
    """
    Main entry point for the LOCAL, OFFLINE version of the game.
    This runs the game without any networking, using the config file.
    """
    pygame.init()
    screen = pygame.display.set_mode((consts.height, consts.width))
    pygame.display.set_caption("Multiplayer Snake (Offline Mode)")
    
    game = GameManager(consts.table_size, screen, consts.sx, consts.sy, consts.block_cells)
    
    snakes = list()
    for snake_config in consts.snakes:
        snakes.append(Snake(
            snake_config['keys'], 
            game, 
            (snake_config['sx'], snake_config['sy']), 
            snake_config['color'], 
            snake_config['direction']
        ))

    clock = pygame.time.Clock()

    while True:
        # 1. Handle local input
        keys = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                keys.append(event.unicode)

        # 2. Update local game state
        game.handle(keys)
        
        # 3. Render the game
        screen.fill(consts.back_color)
        game.draw_grid()
        pygame.display.update() # Single update call per frame

        # 4. Tick the clock
        clock.tick(10) # Run at 10 frames per second


if __name__ == '__main__':
    main()

