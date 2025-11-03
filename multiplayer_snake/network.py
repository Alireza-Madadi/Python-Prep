import socket
import json

class Network:
    """
    A wrapper class for the client's network connection.
    
    Handles connecting to the server, receiving the initial config,
    and sending/receiving game data (key presses).
    """
    def __init__(self, host, port):
        """
        Initializes the network client.

        Args:
            host (str): The server's IP address or hostname.
            port (int): The server's port.
        """
        self.host = host
        self.port = port
        self.data = {}
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        """
        Connects to the server and receives the initial config data.
        
        This config data (from config.json) is then written to the 
        local consts.py file so the client game can use it.
        """
        self.s.connect((self.host, self.port))
        received_data = self.s.recv(4096)
        json_string = received_data.decode('ascii')
        
        # This is a bit of a hack: it overwrites the *local* consts.py's 
        # config data with the data from the server.
        # This ensures all clients have the same config as the server.
        self.data = json.loads(json_string)
        
        # Update consts module variables with server data
        import consts
        consts.back_color = self.data.get('back_color', consts.back_color)
        consts.fruit_color = self.data.get('fruit_color', consts.fruit_color)
        consts.block_color = self.data.get('block_color', consts.block_color)
        consts.cell_size = self.data.get('cell_size', consts.cell_size)
        consts.block_cells = self.data.get('block_cells', consts.block_cells)
        consts.table_size = self.data.get('table_size', consts.table_size)
        consts.height = self.data.get('height', consts.height)
        consts.width = self.data.get('width', consts.width)
        consts.snakes = self.data.get('snakes', consts.snakes)
        consts.sx = self.data.get('sx', consts.sx)
        consts.sy = self.data.get('sy', consts.sy)


    def send_data(self, keys):
        """
        Sends the client's key presses to the server.

        Args:
            keys (list): A list of keys (unicode strings) pressed this frame.
        """
        snake_id = self.data.get('id', 0)
        
        # Format the keypresses for this specific snake
        snake_keys = []
        for key in keys:
            full_key = f"snake_{snake_id}_{key}"
            snake_keys.append(full_key)
            
        data_to_send = {"keys": snake_keys, "dead": False} # 'dead' is not really used here
        json_string = json.dumps(data_to_send)
        try:
            self.s.sendall(json_string.encode('ascii'))
        except socket.error as e:
            print(f"Error sending data: {e}")

    def get_data(self):
        """
        Receives the combined game state (all key presses) from the server.

        Returns:
            list | None: A list of all keys pressed by all players,
                         or None if the connection failed.
        """
        try:
            received_data = self.s.recv(4096).decode('ascii')
            # The server sends a list as a string, e.g., "['w', 'j']"
            # We need to replace single quotes with double quotes for valid JSON
            corrected_string = received_data.replace("'", '"')
            return json.loads(corrected_string)
        except (socket.error, json.JSONDecodeError) as e:
            print(f"Error receiving data: {e}")
            return None
            
    def close(self):
        """Closes the socket connection."""
        self.s.close()

