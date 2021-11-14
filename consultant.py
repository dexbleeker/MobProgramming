import random

from pypbc import *

from client import Client


class Consultant(Client):
    def __init__(self, server):
        super().__init__(server, 0)

    def encrypt(self, message, user_id=0):
        user_public_key = self.server.user_public_key(user_id)

        # Convert message to something in the group
        message = Element(self.pairing, Zr, value=message)

        x = Element.random(self.pairing, Zr)
        y = Element.random(self.pairing, Zr)
        u = pow(self.generator, x)

        vs = []
        for key in [self.y_a(), user_public_key]:
            v = pow(key * y, x)
            vs.append(v)

        c = (pow(y, x) * message)

        return [c, u, *vs]

    def decrypt(self, sigma):
        c = sigma[0]
        u = sigma[1]
        v = sigma[-2]

        divisor = pow(u, self.x_a())
        k = v.__ifloordiv__(divisor)

        m = c.__ifloordiv__(k)
        return m
