import random


class Client:
    def __init__(self, server, client_id):
        self.client_id = client_id
        self.server = server
        self.prime = server.prime
        self.generator = server.generator
        self.x_a = random.randrange(start=1, stop=self.prime - 1)
        self.y_a = pow(self.generator, self.x_a, self.prime)

        # Send public key to server
        server.register_user(self.client_id, self.y_a)

        # Print my keys
        print("Client {} keys:".format(client_id))
        print("x_a: {}".format(self.x_a))
        print("y_a: {}".format(self.y_a))

    def x_a(self):
        """Private key"""
        return self.x_a

    def y_a(self):
        """Public key"""
        return self.y_a

    def client_id(self):
        """The id of the client"""
        return self.client_id

    def encrypt(self, message, user_id=0):
        NotImplementedError("Class %s doesn't implement encrypt()" % self.__class__.__name__)

    def decrypt(self, sigma):
        NotImplementedError("Class %s doesn't implement decrypt()" % self.__class__.__name__)
