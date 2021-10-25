from Crypto.PublicKey import ElGamal
from Crypto.Random import get_random_bytes


def main():
    key = ElGamal.generate(bits=2048, randfunc=get_random_bytes)


if __name__ == "__main__":
    main()
