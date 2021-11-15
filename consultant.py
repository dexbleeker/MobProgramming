import random

from client import Client


class Consultant(Client):
    def __init__(self, server):
        super().__init__(server, 0)

    def encrypt(self, message, user_id=0):
        user_public_key = self.server.user_public_key(user_id)

        x = random.randrange(start=1, stop=self.enc_prime - 1)
        y = random.randrange(start=1, stop=self.enc_prime - 1)
        u = pow(self.generator, x, self.enc_prime)

        vs = []
        for key in [self.y_a(), user_public_key]:
            v = pow(key * y % self.enc_prime, x, self.enc_prime)
            vs.append(v)

        c = (pow(y, x, self.enc_prime) * message) % self.enc_prime

        return [c, u, *vs]

    def decrypt(self, sigma):
        c = int(sigma[0])
        u = int(sigma[1])
        v = int(sigma[-2])

        divisor = int(pow(u, self.x_a(), self.enc_prime))
        k = pow(divisor, -1, self.enc_prime) * v

        m = pow(k, -1, self.enc_prime) * int(c) % self.enc_prime
        return m
