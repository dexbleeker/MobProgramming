from user import User


class Client(User):
    def __init__(self, server, user_id):
        super().__init__(server, user_id)

    def decrypt(self, sigma):
        c = int(sigma[0])
        u = int(sigma[1])
        v = int(sigma[-1])

        divisor = int(pow(u, self.enc_priv_key(), self.prime()))
        k = pow(divisor, -1, self.prime()) * v

        m = pow(k, -1, self.prime()) * c % self.prime()
        return m
