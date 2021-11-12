from Crypto.PublicKey import ElGamal
from Crypto.Random import get_random_bytes


class Server:
    def __init__(self):
        key = ElGamal.generate(bits=256, randfunc=get_random_bytes)
        # self.prime = int(key.p)
        # self.generator = key.g
        self.prime = 23
        self.generator = 5
        self.users = {}

    def prime(self):
        return self.prime

    def generator(self):
        return self.generator

    def register_user(self, client_id, public_key):
        self.users[client_id] = public_key

    def user_public_key(self, user_id):
        """Remember, user_id 0 is the consultant"""
        return self.users[user_id]

    def evaluate_trapdoor(self, trapdoor, user_id, m_peck):
        print("Starting evaluating trapdoor")
        tjq1, tjq2, tjq3, indices = trapdoor
        a, bs, cs = m_peck

        # If the user id is not 0, get the second (1)
        # element from bs later
        if user_id != 0:
            uid = 1

        print("indices: {}".format(indices))

        left = tjq1
        for i in indices:
            left = (left * cs[i]) % self.prime

        right1 = a
        for i in indices:
            right1 = (right1 * tjq2[i]) % self.prime

        right2 = int(bs[uid])
        for i in indices:
            right2 = (right2 * tjq3[i]) % self.prime

        right = (right1 * right2) % self.prime

        print("Left: {}".format(left))
        print("Right: {}".format(right))
        return left == right

        # This method is not working correctly yet.
        # To be able to continue with the rest of the assignment,
        # we stub it to True for now.
        # return True
