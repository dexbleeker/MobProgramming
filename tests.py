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

    def test_user(self):
        """
        User should be able to decrypt his own ciphertext
        """
        user = random.choice(self.users)
        message = 1657
        sigma = user.encrypt(message)
        decrypted = user.decrypt(sigma)

        self.assertEqual(message, decrypted)

    def test_consultant(self):
        """
        Consultant should be able to decrypt users ciphertext
        """
        user = random.choice(self.users)
        message = 26874
        sigma = user.encrypt(message)
        decrypted = self.consultant.decrypt(sigma)

        self.assertEqual(message, decrypted)

    def test_different_user(self):
        """
        Different user should NOT be able to decrypt users ciphertext
        """
        user1 = random.choice(self.users)
        user2 = random.choice(self.users)
        while user1 == user2:
            user2 = random.choice(self.users)

        message = 61298741
        sigma = user1.encrypt(message)
        decrypted = user2.decrypt(sigma)

        self.assertNotEqual(message, decrypted)

    def test_ids(self):
        """
        Consultant id should be 0 and user ids should not be 0
        """
        self.assertEqual(self.consultant.client_id(), 0)
        for u in self.users:
            self.assertNotEqual(u.client_id(), 0)


if __name__ == '__main__':
    unittest.main()
