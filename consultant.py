import random

from client import Client


class Consultant(Client):
    def __init__(self, server):
        super().__init__(server, 0)

    def encrypt(self, message, user_id=0):
        user_public_key = self.server.user_public_key(user_id)

        x = random.randrange(start=1, stop=self.prime - 1)
        y = random.randrange(start=1, stop=self.prime - 1)
        u = pow(self.generator, x, self.prime)

        vs = []
        for key in [self.y_a, user_public_key]:
            v = pow(key * y % self.prime, x, self.prime)
            vs.append(v)

        c = (pow(y, x, self.prime) * message) % self.prime

        return [c, u, *vs]

    def decrypt(self, sigma):
        c = sigma[0]
        u = sigma[1]
        v = sigma[-2]

        divisor = int(pow(int(u), int(self.x_a()), self.prime))
        k = pow(divisor, -1, self.prime) * int(v)

        m = pow(int(k), -1, self.prime) * int(c) % self.prime
        return m
