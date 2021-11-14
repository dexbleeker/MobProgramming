from pypbc import *

from client import Client


class User(Client):
    def __init__(self, server, client_id):
        super().__init__(server, client_id)

    def encrypt(self, message, user_id=0):
        consultant_public_key = self.server.user_public_key(user_id)

        x = Element.random(self.pairing, G1)
        y = Element.random(self.pairing, G1)
        u = pow(self.generator, x)

        vs = []
        for key in [consultant_public_key, self.y_a()]:
            v = pow(key * y, x)
            vs.append(v)

        c = (pow(y, x) * message)

        return [c, u, *vs]

    def decrypt(self, sigma):
        c = sigma[0]
        u = sigma[1]
        v = sigma[-1]

        divisor = pow(u, self.x_a())
        k = v.__ifloordiv__(divisor)

        m = c.__ifloordiv__(k)
        return m
