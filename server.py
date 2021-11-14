from Crypto.PublicKey import ElGamal
from Crypto.Random import get_random_bytes
from pypbc import *


class Server:
    def __init__(self):
        self.pairing = Pairing(Parameters(qbits=512, rbits=160))
        self.generator = Element.random(self.pairing, G1)
        # self.prime = int(key.p)
        # # self.generator = key.g
        # self.prime = 23
        # self.generator = 5
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
        print("assign")
        a, bs, cs = m_peck

        # If the user id is not 0, get the second (1)
        # element from bs later
        if user_id != 0:
            uid = 1

        print("indices: {}".format(indices))

        e = lambda e1,e2: self.pairing.apply(e1, e2)
        
        left = tjq1
        for i in indices:
            left = e(left, cs[i])

        right1 = a
        for i in indices:
            right1 = e(right1, tjq2[i])

        right2 = bs[uid]
        for i in indices:
            right2 = e(right2, tjq3[i])

        right = e(right1, right2)

        print("Left: {}".format(left))
        print("Right: {}".format(right))
        return left == right

        # This method is not working correctly yet.
        # To be able to continue with the rest of the assignment,
        # we stub it to True for now.
        # return True
