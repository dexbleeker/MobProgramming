import random

from consultant import Consultant
from user import User
from server import Server


def main():
    # Single server instance
    server = Server()
    # Create consultant
    consultant = Consultant(server)
    # Create random amount of users
    users = []
    for client_id in range(1, random.randrange(4, 8)):
        users.append(User(server, client_id))

    print(users[-1].client_id)
    print("Encryption:")
    sigma = users[-1].encrypt(12)
    unit = users[-1].m_peck(['transfer', 'withdrawal', 'private', 'imbrokeasfuck'])
    # sigma = consultant.encrypt(12, users[-1].client_id)
    print(str(sigma))
    print("Done")

    print("Decryption:")
    # print(str(users[-1].decrypt(sigma)))
    # print(str(consultant.decrypt(sigma)))
    print("Done")


if __name__ == "__main__":
    main()
