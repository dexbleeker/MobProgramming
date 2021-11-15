from client import Client


class Consultant(Client):
    def __init__(self, server):
        super().__init__(server, 0)

    def decrypt(self, sigma):
        c = int(sigma[0])
        u = int(sigma[1])
        v = int(sigma[-2])

        divisor = int(pow(u, self.enc_priv_key(), self.prime()))
        k = pow(divisor, -1, self.prime()) * v

        m = pow(k, -1, self.prime()) * int(c) % self.prime()
        return m
