import random

from client import Client


class User(Client):
    def __init__(self, server, client_id):
        super().__init__(server, client_id)

    def encrypt(self, message, user_id=0):
        consultant_public_key = self.server.user_public_key(user_id)

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
