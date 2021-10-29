import random
import unittest

from consultant import Consultant
from server import Server
from user import User


class Test(unittest.TestCase):
    def setUp(self):
        self.server = Server()
        self.consultant = Consultant(self.server)
        self.users = []
        for client_id in range(1, random.randrange(4, 8)):
            self.users.append(User(self.server, client_id))

    def test_enc_user(self):
        """
        User should be able to decrypt his own ciphertext
        """
        user = random.choice(self.users)
        message = 1657
        sigma = user.encrypt(message)
        decrypted = user.decrypt(sigma)

        self.assertEqual(message, decrypted)

    def test_enc_consultant(self):
        """
        Consultant should be able to decrypt users ciphertext
        """
        user = random.choice(self.users)
        message = 26874
        sigma = user.encrypt(message)
        decrypted = self.consultant.decrypt(sigma)

        self.assertEqual(message, decrypted)


if __name__ == '__main__':
    unittest.main()
