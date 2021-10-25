from client import Client


class Consultant(Client):
    def __init__(self, server):
        super().__init__(server, 0)

    def encrypt(self, message):
        NotImplementedError("Not yet implemented.")

    def decrypt(self, sigma):
        NotImplementedError("Not yet implemented.")
