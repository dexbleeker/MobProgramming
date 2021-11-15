import hashlib
import random

from pypbc import *


class User:
    def __init__(self, server, user_id):
        self._cid = user_id
        self.server = server
        # Init encryption keys
        self._enc_prime = server.enc_prime()
        self._enc_generator = server.enc_generator()
        self._enc_priv_key = random.randrange(start=1, stop=self._enc_prime - 1)
        self._enc_pub_key = pow(self._enc_generator, self.enc_priv_key(), self._enc_prime)
        # Init trapdoor encryption
        self._td_pairing = server.td_pairing()
        self._td_generator = server.td_generator()
        self._td_priv_key = Element.random(self._td_pairing, Zr)
        self._td_pub_key = Element(self._td_pairing, G1, value=self._td_generator ** self._td_priv_key)
        self.h1 = lambda text: Element.from_hash(self._td_pairing, G1, hashlib.sha3_256(text.encode()).digest())
        self.h2 = lambda text: Element.from_hash(self._td_pairing, G1, hashlib.sha3_512(text.encode()).digest())
        # Send public keys to server
        server.register_user(self.user_id(), self.enc_pub_key(), self.td_pub_key())

    def enc_priv_key(self):
        """Encryption private key"""
        return self._enc_priv_key

    def enc_pub_key(self):
        """Encryption public key"""
        return self._enc_pub_key

    def prime(self):
        """Encryption prime"""
        return self._enc_prime

    def enc_generator(self):
        """Encryption generator"""
        return self._enc_generator

    def td_priv_key(self):
        """Trapdoor private key"""
        return self._td_priv_key

    def td_pub_key(self):
        """Trapdoor public key"""
        return self._td_pub_key

    def td_generator(self):
        """Trapdoor generator"""
        return self._td_generator

    def td_pairing(self):
        """Trapdoor pairing"""
        return self._td_pairing

    def user_id(self):
        """The id of the client"""
        return self._cid

    def send_data(self, data, keyword_set):
        """
        Store data in datastore of server.
        """
        encrypted_data = self.encrypt(message=data)
        m_peck = self.m_peck(keyword_set)

        self.server.store_data((encrypted_data, m_peck))

    def m_peck(self, keyword_set, user_id=0):
        if self.user_id() == 0:
            keys = [self.server.user_td_pub(0), self.server.user_td_pub(user_id)]
        else:
            keys = [self.server.user_td_pub(0), self.td_pub_key()]

        h = [self.h1(x) for x in keyword_set]
        f = [self.h2(x) for x in keyword_set]

        s = Element.one(self.td_pairing(), Zr)
        r = Element.one(self.td_pairing(), Zr)

        a = self.td_generator() ** r
        bs = [pow(key, s) for key in keys]
        cs = [pow(h[i], r) * pow(f[i], s) for i in range(len(h))]

        return [a, bs, cs]

    def generate_trapdoor(self, indices, keyword_set):
        t = Element.one(self.td_pairing(), Zr)

        h = [self.h1(x) for x in keyword_set]
        f = [self.h2(x) for x in keyword_set]

        tjq1 = pow(self.td_generator(), t)

        tjq2 = [pow(x, t) for x in h]

        inverse = t.__ifloordiv__(self.td_priv_key())
        tjq3 = [y ** inverse for y in f]
        return [tjq1, tjq2, tjq3, indices]

    def encrypt(self, message, user_id=0):
        NotImplementedError("Class %s doesn't implement encrypt()" % self.__class__.__name__)

    def encrypt_file(self, filename, user_id=0):
        f = open(filename, "rb")

        message_bytes = []
        while byte := f.read(1):
            message_bytes.append(int.from_bytes(bytes=byte, byteorder='big', signed=False))
        f.close()

        encrypted_bytes = []
        for byte in message_bytes:
            eb = self.encrypt(byte, user_id)
            encrypted_bytes.append(eb)

        return encrypted_bytes

    def decrypt(self, sigma):
        NotImplementedError("Class %s doesn't implement decrypt()" % self.__class__.__name__)

    def decrypt_file(self, byte_array, filename="result.txt"):
        decrypted_bytes = []
        for byte in byte_array:
            db = self.decrypt(byte)
            decrypted_bytes.append(db)

        result = open(filename, "wb")
        result.write(bytes(bytearray(decrypted_bytes)))
        result.close()

        return filename
