# The Multiplayer Snake Game

A classic Snake game built with Pygame, powered by a custom client-server architecture using Python's socket and threading modules.

This project demonstrates core competencies in game development, network programming, and concurrent processing. It supports multiple players connecting to a central server, with all game state logic handled server-side.

This project was developed as part of the **Quera College Advanced Python and Object-Oriented Thinking** course.

## Core Concepts Demonstrated

- **Client-Server Architecture:** A central, multi-threaded server (server.py) manages the game logic and state, while multiple clients (client.py) connect to it to send inputs and receive game state updates.
- **Socket Programming:** Uses Python's built-in socket library for low-level TCP network communication between the server and clients.
- **Threading:** The server uses threading to handle each connected client in a separate thread, allowing for simultaneous players.
- **Game Logic with Pygame:** Implements a complete game loop, grid-based movement, collision detection, and dynamic rendering using pygame.
- **Data Serialization:** Uses json to serialize (encode) keyboard inputs from the client and game state from the server for transmission over the network.
- **Configuration Management:** Game settings (grid size, colors, snake configs) are loaded from an external config.json file.

## Tech Stack

- **Python 3**
- **Pygame** (for game logic and rendering)
- **Socket** (for networking)
- **Threading** (for server concurrency)
- **JSON** (for data serialization)

## How to Run

This project requires running the server and at least one client (ideally two, in separate terminals).

### 1\. Install Dependencies

\# Navigate to the project directory  
cd Python-Prep/multiplayer_snake  
<br/>\# Install Pygame  
pip install -r requirements.txt  

### 2\. Run the Server

Open a terminal and run server.py. This will start the game server and it will wait for clients to connect.

python server.py  

_Note: The test server (server.py) is configured to handle exactly the number of snakes defined in config.json (default is 2)._

### 3\. Run the Clients

Open a **new terminal** for each player and run client.py.

\# In Terminal 2  
python client.py  
<br/>\# In Terminal 3  
python client.py  

The game will start as soon as the required number of clients have connected. Player 1 uses W, A, S, D and Player 2 uses I, J, K, L.

## How to Run Tests

A simple test suite for the network client is included.

To run all tests for **this specific project**, navigate to the **root directory** of this repository (`Python-Prep/`) and use the `unittest discover` command with the `-s` flag:

```bash
# From the root "Python-Prep" directory:
python -m unittest discover -s multiplayer_snake

## Project Structure

Python-Prep/  
│  
└── multiplayer_snake/  
├── \__init_\_.py  
├── README.md # This README file  
├── requirements.txt # Project dependencies  
├── config.json # Game configuration settings  
│  
├── consts.py # Loads config.json  
├── cell.py # Represents a single cell on the game grid  
├── snake.py # Class for Snake logic and movement  
├── game_manager.py # Core game loop and state management  
│  
├── network.py # Client-side network socket wrapper  
├── client.py # Client entry point (Runs the game)  
├── server.py # Server entry point (Handles clients)  
├── Local Game.py # A local, offline version of the game  
│  
└── test/ # Unit tests  
├── \__init_\_.py  
└── test_sample.py