import hashlib

from pypbc import *


class Client:
    def __init__(self, server, client_id):
        self.__cid = client_id
        self.server = server
        self.generator = server.generator
        self.pairing = server.pairing
        self.__priv_key = Element.random(self.pairing, Zr)
        self.__pub_key = Element(self.pairing, G1, value=self.generator ** self.__priv_key)
        # Send public key to server
        server.register_user(self.client_id(), self.y_a())
        self.h1 = self.get_hash_function(self.pairing, hashlib.sha3_256)
        self.h2 = self.get_hash_function(self.pairing, hashlib.sha3_512)

    def x_a(self):
        """Private key"""
        return self.__priv_key

    def y_a(self):
        """Public key"""
        return self.__pub_key

    def client_id(self):
        """The id of the client"""
        return self.__cid

    def m_peck(self, keyword_set):
        h = [self.h1(x) for x in keyword_set]
        f = [self.h2(x) for x in keyword_set]

        # print("mpeck h: {}".format(h))
        # print("mpeck f: {}".format(f))

        s = Element.random(self.pairing, Zr)
        r = Element.random(self.pairing, Zr)

        a = self.generator ** r
        bs = [pow(key, s) for key in [self.server.user_public_key(0), self.y_a()]]
        cs = [pow(h[i], r) * pow(f[i], s) for i in range(len(h))]

        # print("--------")
        # print("a: {}".format(a))
        # print("bs: {}".format(bs))
        # print("cs: {}".format(cs))
        # print("--------")
        return [a, bs, cs]

    def generate_trapdoor(self, indices, keyword_set):
        t = Element.random(self.pairing, Zr)

        h = [self.h1(x) for x in keyword_set]
        f = [self.h2(x) for x in keyword_set]

        # print("mpeck h: {}".format(h))
        # print("mpeck f: {}".format(f))

        tjq1 = pow(self.generator, t)
        # print("tjq1: {}".format(tjq1))

        tjq2 = [pow(x, t) for x in h]
        # print("tjq2: {}".format(tjq2))

        inverse = t.__ifloordiv__(self.x_a())
        tjq3 = [y ** inverse for y in f]
        # print("tjq3: {}".format(tjq3))
        # print("indices: {}".format(indices))

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

    def get_hash_function(self, pairing, hash_function):
        return lambda text: Element.from_hash(pairing, G1, hash_function(text).digest()) if isinstance(text, (
            bytes, bytearray)) else Element.from_hash(pairing, G1, hash_function(text.encode()).digest())
