import random

from client import Client
from server import Server


def main():
    # Single server instance
    server = Server()
    # Create random amount of clients
    for client_id in range(random.randrange(4, 8)):
        Client(server, client_id)

    # print("Encryption:")
    # sigma = c.encrypt(12)
    # print(str(sigma))
    # print("Done")
    #
    # print("Decryption:")
    # print(str(c.decrypt(sigma)))
    # print("Done")


if __name__ == "__main__":
    main()
