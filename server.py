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

    def consultant_public_key(self):
        consultant = self.users[0]
        assert consultant  # its id == 0
        return consultant

    # TODO: Evaluate trapdoor
    def evaluate_trapdoor(self):
        pass
