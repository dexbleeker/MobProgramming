from Crypto.PublicKey import ElGamal
from Crypto.Random import get_random_bytes


class Server:
    def __init__(self):
        key = ElGamal.generate(bits=256, randfunc=get_random_bytes)
        self.prime = key.p
        self.generator = key.g
        self.users = {}

    def prime(self):
        return self.prime

    def generator(self):
        return self.generator

    def register_user(self, client_id, public_key):
        self.users[client_id] = public_key

    def user_public_key(self, user_id):
        return self.users[user_id]

    def evaluate_trapdoor(self, trapdoor, user_id, m_peck):
        print("Starting evaluating trapdoor")
        tjq1, tjq2, tjq3, indices = trapdoor
        a, bs, cs = m_peck

        left = tjq1
        for i in indices:
            left = (left * cs[i]) % int(self.prime)

        right1 = a
        for i in tjq2:
            right1 = (right1 * i) % int(self.prime)

        right2 = bs[user_id]
        for i in tjq3:
            right2 = (right2 * i) % int(self.prime)

        right = (right1 * right2) % int(self.prime)

        print("Left: {}".format(left))
        print("Right: {}".format(right))

        print("result: {}".format(left == right))
        return left == right
