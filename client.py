import random

import mmh3


class Client:
    def __init__(self, server, client_id):
        self.__cid = client_id
        self.server = server
        self.prime = int(server.prime)
        self.generator = server.generator
        self.__priv_key = random.randrange(start=1, stop=self.prime - 1)
        self.__pub_key = pow(self.generator, self.x_a(), self.prime)

        # Send public key to server
        server.register_user(self.client_id(), self.y_a())

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
        h = [mmh3.hash(x, 0, signed=False) % self.prime for x in keyword_set]
        f = [mmh3.hash(x, 1, signed=False) % self.prime for x in keyword_set]

        s = random.randrange(start=1, stop=self.prime - 1)
        r = random.randrange(start=1, stop=self.prime - 1)

        a = pow(self.generator, r, self.prime)
        bs = [pow(key, s, self.prime) for key in [self.server.user_public_key(0), self.y_a()]]
        cs = [pow(h[i], r, self.prime) * pow(f[i], s, self.prime) for i in range(len(h))]

        return [a, bs, cs]

    def generate_trapdoor(self, indices, keyword_set):
        t = random.randrange(start=1, stop=self.prime - 1)
        tjq1 = pow(self.generator, t, self.prime)
        print("tjq1: {}".format(tjq1))

        tjq2 = [pow(mmh3.hash(keyword, 0, signed=False) % self.prime, t, self.prime) for keyword in keyword_set]
        print("tjq2: {}".format(tjq2))

        inverse = pow(self.x_a(), -1, self.prime)
        tjq3 = [pow(mmh3.hash(keyword, 1, signed=False) % self.prime, inverse * t, self.prime) for keyword in keyword_set]
        print("tjq3: {}".format(tjq3))

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
