import random

from client import Client
from server import Server


def main():
    # Single server instance
    server = Server()
    # Random amount of clients
    client = []
    for _ in range(random.randrange(4, 8)):
        client.append(Client(server.prime, server.generator))

    x_a, y_a = setup(server.prime, server.generator)


def decrypt():
    pass


if __name__ == "__main__":
    main()
