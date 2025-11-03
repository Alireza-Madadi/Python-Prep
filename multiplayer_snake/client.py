import pygame
import sys
from network import Network
import consts
from game_manager import GameManager
from snake import Snake

def main():
    """
    Main entry point for the client-side game.
    Initializes Pygame, connects to the server, and runs the main game loop.
    """
    pygame.init()
    
    # Connect to the server
    try:
        network = Network('localhost', 12345)
        network.start()
    except Exception as e:
        print(f"Failed to connect to server: {e}")
        return

    # Initialize game components based on config from server
    screen = pygame.display.set_mode((consts.height, consts.width))
    pygame.display.set_caption(f"Multiplayer Snake - Player {network.data.get('id', '?')}")
    
    game = GameManager(consts.table_size, screen, consts.sx, consts.sy, consts.block_cells)
    
    # Create snakes based on server config
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
                network.close()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                keys.append(event.unicode)
        
        # 2. Send local input to server
        network.send_data(keys)
        
        # 3. Get global game state from server
        all_keys = network.get_data()
        
        if all_keys is None:
            print("Disconnected from server.")
            break
            
        # 4. Update local game state
        game.handle(all_keys)
        
        # 5. Render the game
        screen.fill(consts.back_color)
        game.draw_grid()
        pygame.display.update() # Single update call per frame

        # 6. Tick the clock
        clock.tick(10) # Run at 10 frames per second (same as pygame.time.wait(100))


if __name__ == '__main__':
    main()

