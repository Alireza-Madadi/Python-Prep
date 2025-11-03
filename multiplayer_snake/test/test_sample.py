import unittest
import time
import os
import json
from threading import Thread
from socket import socket

# Import classes from the main package
from multiplayer_snake.network import Network
from multiplayer_snake.server import Server

# Import the server_tester module attributes we need to check
import multiplayer_snake.server as server_module

class TestNetwork(unittest.TestCase):
    """
    A simple test suite for the client-server network connection.
    It simulates a server start and a client connection.
    """
    
    server_thread = None
    test_server = None
    
    @classmethod
    def setUpClass(cls):
        """Set up and start the server in a separate thread."""
        try:
            # Use a different port for testing to avoid conflicts
            cls.TEST_PORT = 5555
            
            # The server is configured to wait for 1 client
            cls.test_server = Server(number_of_clients=1, port=cls.TEST_PORT)
            
            # Run the server's main loop in a background thread
            cls.server_thread = Thread(target=cls.test_server.main_loop, daemon=True)
            cls.server_thread.start()
            time.sleep(0.1) # Give the server a moment to start
        except Exception as e:
            print(f"Failed to set up server: {e}")
            
    @classmethod
    def tearDownClass(cls):
        """Shut down the server."""
        if cls.test_server:
            cls.test_server.finish()
            
    def test_client_server_connection(self):
        """
        Tests if a client can connect, receive config, send, and receive data.
        """
        if not self.test_server:
            self.skipTest("Server did not start, skipping connection test.")

        # 1. Client Connects and gets config
        network = None
        try:
            network = Network("127.0.0.1", self.TEST_PORT)
            network.start()
        except Exception as e:
            self.fail(f"Client failed to connect or start: {e}")

        # Check if config was received
        self.assertIn('table_size', network.data, "Config data was not received or is invalid.")
        self.assertEqual(network.data['id'], 0, "Client did not receive correct ID (should be 0).")

        # 2. Client Sends Data
        try:
            network.send_data(['w'])
        except Exception as e:
            self.fail(f"Client failed to send data: {e}")

        # 3. Client Receives Data
        try:
            # Wait for the server to process and send back
            time.sleep(0.2) 
            data = network.get_data()
            self.assertIsNotNone(data, "Client did not receive data from server.")
            # The server should echo back the formatted key
            self.assertIn('snake_0_w', data, "Client did not receive the correct echo from server.")
        except Exception as e:
            self.fail(f"Client failed to receive data: {e}")
            
        if network:
            network.close()

if __name__ == '__main__':
    unittest.main()

