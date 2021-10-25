import random

from consultant import Consultant
from normal_client import User
from server import Server


def main():
    # Single server instance
    server = Server()
    # Create consultant
    Consultant(server)
    # Create random amount of users
    for client_id in range(1, random.randrange(4, 8)):
        user = User(server, client_id)

    print("Encryption:")
    sigma = user.encrypt(12)
    print(str(sigma))
    print("Done")

    print("Decryption:")
    print(str(user.decrypt(sigma)))
    print("Done")


if __name__ == "__main__":
    main()
