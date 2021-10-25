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

    def encrypt(self, message):
        consultant_public_key = self.server.consultant_public_key()

        x = random.randrange(start=1, stop=self.prime - 1)
        y = random.randrange(start=1, stop=self.prime - 1)
        u = pow(self.generator, x, self.prime)

        vs = []
        for key in [consultant_public_key, self.y_a]:
            v = pow(key * y % self.prime, x, self.prime)
            vs.append(v)

        c = (pow(y, x, int(self.prime)) * message) % int(self.prime)

        return [c, u, *vs]

    def decrypt(self, sigma):
        c = sigma[0]
        u = sigma[1]
        v = sigma[-1]

        divisor = int(pow(int(u), int(self.x_a), int(self.prime)))
        k = pow(divisor, -1, int(self.prime)) * int(v)

        m = pow(int(k), -1, int(self.prime)) * int(c) % int(self.prime)
        return m
