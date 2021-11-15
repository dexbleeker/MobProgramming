from Crypto.PublicKey import ElGamal
from Crypto.Random import get_random_bytes
from pypbc import *


class Server:
    def __init__(self):
        # Init key lists
        self.enc_keys = {}
        self.td_keys = {}
        # Init default encryption
        _key = ElGamal.generate(bits=256, randfunc=get_random_bytes)
        self._enc_prime = int(_key.p)
        self._enc_generator = _key.g
        # Init trapdoor encryption
        self._td_params = Parameters(qbits=512, rbits=160)
        self._td_pairing = Pairing(self._td_params)
        self._td_generator = Element.random(self._td_pairing, G1)

    def enc_prime(self):
        """Prime for default encryption"""
        return self._enc_prime

    def enc_generator(self):
        """Generator for default encryption"""
        return self._enc_generator

    def td_generator(self):
        """Generator for trapdoor encryption"""
        return self._td_generator

    def td_pairing(self):
        """Pairing for trapdoor encryption"""
        return self._td_pairing

    def register_user(self, client_id, enc_pub_key, td_pub_key):
        self.enc_keys[client_id] = enc_pub_key
        self.td_keys[client_id] = td_pub_key

    def user_enc_pub(self, user_id):
        """Remember, user_id 0 is the consultant"""
        return self.enc_keys[user_id]

    def user_td_pub(self, user_id):
        """Remember, user_id 0 is the consultant"""
        return self.td_keys[user_id]

    def evaluate_trapdoor(self, trapdoor, user_id, m_peck):
        """
        This method evaluates the given trapdoor.
        :return: True/False
        """
        print("Starting evaluating trapdoor")
        tjq1, tjq2, tjq3, indices = trapdoor
        a, bs, cs = m_peck

        # If the user id is not 0, get the second (1)
        # element from bs later
        uid = 1 if user_id != 0 else uid = 0

        e = lambda e1, e2: self.td_pairing().apply(e1, e2)

        left = Element.one(self.td_pairing(), G1)
        for i in indices:
            left = left * cs[i]
        left = e(tjq1, left)

        right1 = Element.one(self.td_pairing(), G1)
        for i in indices:
            right1 = right1 * tjq2[i]
        right1 = e(a, right1)

        g_s = bs[uid]
        right2 = Element.one(self.td_pairing(), G1)

        for i in indices:
            right2 = right2 * tjq3[i]
        right2 = e(g_s, right2)

        right = right1 * right2

        # print("Left: {}".format(left))
        # print("Right: {}".format(right))
        return left == right
