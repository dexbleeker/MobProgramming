from Crypto.PublicKey import ElGamal
from Crypto.Random import get_random_bytes


class Server:
    def __init__(self):
        key = ElGamal.generate(bits=256, randfunc=get_random_bytes)
        self.prime = key.p
        self.generator = key.g

    def prime(self):
        return self.prime

    def generator(self):
        return self.generator

    # TODO: Evaluate trapdoor
    def evaluate_trapdoor(self):
        pass
