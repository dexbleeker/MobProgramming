import random
import mmh3


class Client:
    def __init__(self, server, client_id):
        self.client_id = client_id
        self.server = server
        self.prime = server.prime
        self.generator = server.generator
        self.x_a = random.randrange(start=1, stop=self.prime - 1)
        self.y_a = pow(self.generator, self.x_a, self.prime)

        # Send public key to server
        server.register_user(self.client_id, self.y_a)

        # Print my keys
        print("Client {} keys:".format(client_id))
        print("x_a: {}".format(self.x_a))
        print("y_a: {}".format(self.y_a))

    def x_a(self):
        """Private key"""
        return self.x_a

    def y_a(self):
        """Public key"""
        return self.y_a

    def client_id(self):
        """The id of the client"""
        return self.client_id

    def mpeck(self, keyword_set):
        h = [mmh3.hash(x, 0) for x in keyword_set]
        f = [mmh3.hash(x, 1) for x in keyword_set]

        s = random.randrange(start=1, stop=self.prime - 1)
        r = random.randrange(start=1, stop=self.prime - 1)

        a = pow(self.generator, r, self.prime)
        bs = [pow(key, s) for key in [self.y_a, self.server.user_public_key(0)]]
        cs = [pow(h[i], r) * pow(f[i], s) for i in range(len(h))]

        return [a, *bs, *cs]

    def encrypt(self, message, user_id=0):
        NotImplementedError("Class %s doesn't implement encrypt()" % self.__class__.__name__)

    def decrypt(self, sigma):
        NotImplementedError("Class %s doesn't implement decrypt()" % self.__class__.__name__)
