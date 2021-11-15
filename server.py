from collections import defaultdict

from Crypto.PublicKey import ElGamal
from Crypto.Random import get_random_bytes
from pypbc import *


class Server:
    def __init__(self):
        # Init data store
        self.data = defaultdict(list)
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

    def store_data(self, user_id, data):
        """
        Store data in local datastore.
        Data is stored as:
        {
          user_id: [(sigma, m_peck), (sigma, m_peck), ...],
          ...
        }
        """
        self.data[0].append(data)  # Store separately for the consultant
        self.data[user_id].append(data)

    def evaluate_trapdoor(self, trapdoor, user_id):
        data_list = self.data[user_id]
        result = []
        for (sigma, m_peck) in data_list:
            if self.evaluate_trapdoor_single_mpeck(trapdoor, user_id, m_peck):
                result.append(sigma)
        return result

    def evaluate_trapdoor_single_mpeck(self, trapdoor, user_id, m_peck):
        """
        This method evaluates the given trapdoor with a single m_peck.
        :return: True/False
        """
        tjq1, tjq2, tjq3, indices = trapdoor
        a, bs, cs = m_peck

        # If the user id is not 0, get the second (1)
        # element from bs later
        uid = 1 if user_id != 0 else 0

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

        return left == right
