import random

from Crypto.PublicKey import ElGamal
from Crypto.Random import get_random_bytes


def main():
    key = ElGamal.generate(bits=256, randfunc=get_random_bytes)
    prime, generator = key.p, key.g
    x_a, y_a = setup(prime, generator)


def setup(prime, generator):
    x_a = random.randrange(start=1, stop=prime - 1)
    y_a = pow(generator, x_a, prime)
    print("x_a: {}".format(x_a))
    print("y_a: {}".format(y_a))
    return x_a, y_a


def encrypt(prime, generator):
    x = random.randrange(start=1, stop=prime - 1)
    y = random.randrange(start=1, stop=prime - 1)
    u = pow(generator, x, prime)


def decrypt():
    pass


if __name__ == "__main__":
    main()
