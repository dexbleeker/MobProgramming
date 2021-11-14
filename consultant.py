import random

from pypbc import *

from client import Client


class Consultant(Client):
    def __init__(self, server):
        super().__init__(server, 0)

    def encrypt(self, message, user_id=0):
        user_public_key = self.server.user_public_key(user_id)

        x = Element.random(genkey.pairing, Zr)
        y = Element.random(genkey.pairing, Zr)
        u = pow(self.generator, x)

        vs = []
        for key in [self.y_a(), user_public_key]:
            v = pow(key * y, x)
            vs.append(v)

        c = (pow(y, x) * message)

        return [c, u, *vs]

    def decrypt(self, sigma):
        c = int(sigma[0])
        u = int(sigma[1])
        v = int(sigma[-2])

        divisor = int(pow(u, self.x_a()))
        k = v.__ifloordiv__(divisor)

        m = c.__ifloordiv__(k)
        return m
