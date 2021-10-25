import random


class Client:
    def __init__(self, prime, generator):
        self.prime = prime
        self.generator = generator
        self.x_a = random.randrange(start=1, stop=prime - 1)
        self.y_a = pow(generator, self.x_a, prime)
        print("x_a: {}".format(self.x_a))
        print("y_a: {}".format(self.y_a))
    
    def x_a(self):
        return self.x_a
    
    def y_a(self):
        return self.y_a
    
    def encrypt(self):
        x = random.randrange(start=1, stop=self.prime - 1)
        y = random.randrange(start=1, stop=self.prime - 1)
        u = pow(self.generator, x, self.prime)
