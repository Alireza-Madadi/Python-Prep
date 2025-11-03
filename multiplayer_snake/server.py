from threading import Thread
import socket
import json
import time
import os
class Server:
    """
    The main game server.
    
    It waits for a fixed number of clients to connect,
    sends them the initial game config, and then enters a loop
    where it collects inputs from all clients, broadcasts
    the combined inputs back to all clients, and repeats.
    """
    def __init__(self, number_of_clients, port):
        """
        Initializes the server.

        Args:
            number_of_clients (int): The exact number of clients to wait for.
            port (int): The port to listen on.
        """
        self.port = port
        self.conf = ('', self.port) # Listen on all interfaces
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(self.conf)
        self.number_of_clients = number_of_clients
        self.clients = []
        self.config = self.load_config()

    def load_config(self):
        """
        Loads the game configuration from config.json.
        This config will be sent to all clients upon connection.
        """
        try:
            # Get the absolute path to the directory containing this file
            base_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(base_dir, 'config.json')
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config.json: {e}. Using empty config.")
            return {}

    def wait_for_clients(self):
        """
        Listens for and accepts connections until the
        required number of clients is reached.
        """
        print(f"Server started, waiting for {self.number_of_clients} clients on port {self.port}...")
        try:
            self.s.listen(self.number_of_clients)
            
            while len(self.clients) < self.number_of_clients:
                c, addr = self.s.accept()
                self.clients.append((c, addr))
                print(f"Client {len(self.clients)} connected from {addr}")

            print(f"All {self.number_of_clients} clients connected. Starting game.")
            self.s.close() # Stop accepting new connections

        except socket.error as e:
            print(f"Server error while waiting for clients: {e}")
            self.finish()

    def start_game(self):
        """
        Sends the initial configuration to all connected clients.
        Each client receives a unique 'id' (0, 1, 2...).
        """
        if not self.config:
            print("Cannot start game, config is empty.")
            return
            
        for i, (client_socket, addr) in enumerate(self.clients):
            self.config['id'] = i # Assign a unique ID to this client
            try:
                client_socket.sendall(str(json.dumps(self.config)).encode('ascii'))
            except socket.error as e:
                print(f"Error sending config to client {i}: {e}")
                self.clients.remove((client_socket, addr))
                
        # We must reset the 'id' field in the base config
        if 'id' in self.config:
            del self.config['id']

    def pass_cycle(self):
        """
        Executes one "tick" of the server loop.
        
        1. Collects keys from ALL clients.
        2. Broadcasts the list of ALL keys back to ALL clients.
        
        Returns:
            bool: True if the game should continue (at least one client active),
                  False if all clients are dead/disconnected.
        """
        all_keys = []
        active_clients = 0
        
        clients_to_remove = []

        for client_socket, addr in self.clients:
            try:
                # Receive data from this client
                data = client_socket.recv(1024).decode('ascii')
                if not data:
                    clients_to_remove.append((client_socket, addr))
                    continue
                    
                client_data = json.loads(data)
                
                # Check if client is still alive
                if not client_data.get('dead', False):
                    active_clients += 1
                    all_keys.extend(client_data.get('keys', []))
                    
            except (socket.error, json.JSONDecodeError) as e:
                print(f"Client {addr} disconnected or sent bad data: {e}")
                clients_to_remove.append((client_socket, addr))

        # Remove dead/disconnected clients
        for client in clients_to_remove:
            if client in self.clients:
                self.clients.remove(client)
                
        if not self.clients or active_clients == 0:
            return False # No active clients, stop the server loop

        # Broadcast the combined list of all keys to all remaining clients
        broadcast_data = str(all_keys).encode('ascii')
        for client_socket, addr in self.clients:
            try:
                client_socket.sendall(broadcast_data)
            except socket.error:
                # This client might have disconnected in this exact moment
                pass 

        return True

    def finish(self):
        """Closes all client sockets and the main server socket."""
        print("Server shutting down.")
        for client_socket, addr in self.clients:
            client_socket.close()
        self.s.close()

    def main_loop(self):
        """The main server loop."""
        self.wait_for_clients()
        self.start_game()

        while True:
            if not self.pass_cycle():
                print("All clients disconnected or game over. Stopping server.")
                break
            time.sleep(0.1) # Sync with the client's 10 FPS tick rate

        self.finish()


if __name__ == '__main__':
    # We read the number of clients from the config file
    import consts
    num_players = len(consts.snakes)
    if num_players == 0:
        print("Config file has 0 snakes defined. Exiting.")
    else:
        server = Server(number_of_clients=num_players, port=12345)
        server.main_loop()

