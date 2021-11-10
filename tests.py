import base64
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
        # for client_id in range(1, random.randrange(4, 8)):
        self.users.append(User(self.server, 1))

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

    def test_file(self):
        """
        Test whether encryption/decryption of a file works correctly.
        """
        user = random.choice(self.users)

        f = open("test-file.txt", "rb")
        message_bytes = []
        while (byte := f.read(1)):
            message_bytes.append(int.from_bytes(bytes=byte, byteorder='big', signed=False))
        f.close()

        encrypted_bytes = []
        for byte in message_bytes:
            eb = user.encrypt(byte)
            encrypted_bytes.append(eb)

        decrypted_bytes = []
        for byte in encrypted_bytes:
            db = user.decrypt(byte)
            decrypted_bytes.append(db)

        self.assertEqual(message_bytes, decrypted_bytes)

    def test_trapdoor(self):
        """
        Trapdoor evaluation should return True
        """
        user = random.choice(self.users)
        assert user.client_id() == 1

        m_peck = user.m_peck(['transfer', 'withdrawal', 'private'])
        trapdoor = user.generate_trapdoor([0], ['transfer', 'withdrawal', 'private'])

        result = self.server.evaluate_trapdoor(trapdoor, 1, m_peck)

        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
