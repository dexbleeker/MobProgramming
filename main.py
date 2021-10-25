import random

from client import Client
from server import Server


def main():
    # Single server instance
    server = Server()
    # Create random amount of clients
    for client_id in range(random.randrange(4, 8)):
        Client(server, client_id)
    # x_a, y_a = setup(server.prime, server.generator)


if __name__ == "__main__":
    main()
