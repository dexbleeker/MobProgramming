import random

from client import Client


class User(Client):
    def __init__(self, server, client_id):
        super().__init__(server, client_id)

    def encrypt(self, message, user_id=0):
        consultant_public_key = self.server.user_enc_pub(user_id)

        x = random.randrange(start=1, stop=self.prime() - 1)
        y = random.randrange(start=1, stop=self.prime() - 1)
        u = pow(self.enc_generator(), x, self.prime())

        vs = []
        for key in [consultant_public_key, self.enc_pub_key()]:
            v = pow(key * y % self.prime(), x, self.prime())
            vs.append(v)

        c = (pow(y, x, self.prime()) * message) % self.prime()

        return [c, u, *vs]

    def decrypt(self, sigma):
        c = sigma[0]
        u = sigma[1]
        v = sigma[-1]

        divisor = int(pow(u, self.enc_priv_key(), self.prime()))
        k = pow(divisor, -1, self.prime()) * v

        m = pow(k, -1, self.prime()) * c % self.prime()
        return m
