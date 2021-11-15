import random

from client import Client


class Consultant(Client):
    def __init__(self, server):
        super().__init__(server, 0)

    def encrypt(self, message, user_id=0):
        user_public_key = self.server.user_public_key(user_id)

        x = random.randrange(start=1, stop=self.prime() - 1)
        y = random.randrange(start=1, stop=self.prime() - 1)
        u = pow(self.generator, x, self.prime())

        vs = []
        for key in [self.enc_pub_key(), user_public_key]:
            v = pow(key * y % self.prime(), x, self.prime())
            vs.append(v)

        c = (pow(y, x, self.prime()) * message) % self.prime()

        return [c, u, *vs]

    def decrypt(self, sigma):
        c = int(sigma[0])
        u = int(sigma[1])
        v = int(sigma[-2])

        divisor = int(pow(u, self.enc_priv_key(), self.prime()))
        k = pow(divisor, -1, self.prime()) * v

        m = pow(k, -1, self.prime()) * int(c) % self.prime()
        return m
