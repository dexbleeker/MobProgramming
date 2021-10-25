import random

from client import Client
from server import Server


def main():
    # Single server instance
    server = Server()
    # Create random amount of clients
    for client_id in range(random.randrange(4, 8)):
        c = Client(server, client_id)

    print("Encryption:")
    print(str(c.encrypt(12)))
    print("Done")


if __name__ == "__main__":
    main()
