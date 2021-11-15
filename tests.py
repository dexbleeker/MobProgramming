import filecmp
import random
import unittest

from client import Client
from consultant import Consultant
from server import Server


class Test(unittest.TestCase):
    def setUp(self):
        self.server = Server()
        self.consultant = Consultant(self.server)
        self.users = []
        for user_id in range(1, random.randrange(4, 8)):
            self.users.append(Client(self.server, 1))

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
        self.assertEqual(self.consultant.user_id(), 0)
        for u in self.users:
            self.assertNotEqual(u.user_id(), 0)

    def test_data_storing(self):
        """
        Test whether storing works.
        """
        user = random.choice(self.users)

        sigma = user.encrypt(23)
        m_peck = user.m_peck(["foobar"])
        self.server.store_data(user.user_id(), (sigma, m_peck))

        self.assertEqual(self.server.data[user.user_id()], [(sigma, m_peck)])

    def test_data_querying(self):
        """
        Test whether querying works.
        """
        user = random.choice(self.users)

        sigma = user.encrypt(9511)
        m_peck = user.m_peck(["foobar"])
        self.server.store_data(user.user_id(), (sigma, m_peck))

        # Test trapdoor that should return nothing
        trapdoor = user.generate_trapdoor([0, 1], ["foobar", "barfoo"])
        result = self.server.evaluate_trapdoor(trapdoor, user.user_id())

        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])

        # Test trapdoor that should return single sigma
        trapdoor = user.generate_trapdoor([0], ["foobar"])
        result = self.server.evaluate_trapdoor(trapdoor, user.user_id())
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], sigma)

    def test_different_user_search(self):
        """
        Different user should NOT get a result when using the same keyword.
        """
        pass

    def test_text_file(self):
        """
        Test whether encryption/decryption of a text file works correctly.
        """
        user = random.choice(self.users)

        encrypted = user.encrypt_file("test-file.txt")
        decrypted_file_name = user.decrypt_file(encrypted)

        self.assertTrue(filecmp.cmp("test-file.txt", decrypted_file_name))

    @unittest.skip("This works, but takes a long time (166 seconds on my machine).")
    def test_image_file(self):
        """
        Test whether encryption/decryption of a image file works correctly.
        """
        user = random.choice(self.users)
        image = "stock-image.png"

        encrypted = user.encrypt_file(image)
        decrypted_file_name = user.decrypt_file(encrypted, "result-image.png")

        self.assertTrue(filecmp.cmp(image, decrypted_file_name))

    def test_single_trapdoor(self):
        """
        Trapdoor evaluation should return True
        """
        user = random.choice(self.users)
        assert user.user_id() == 1

        m_peck = user.m_peck(['transfer'])
        trapdoor = user.generate_trapdoor([0], ['transfer'])

        result = self.server.evaluate_trapdoor(trapdoor, 1, m_peck)

        self.assertTrue(result)

    def test_multiple_trapdoor(self):
        """
        Trapdoor evaluation should return true,
        even if multiple keywords are used.
        """
        user = random.choice(self.users)
        assert user.user_id() == 1

        m_peck = user.m_peck(['transfer', 'withdrawal', 'private'])
        trapdoor = user.generate_trapdoor([0, 2], ['transfer', 'withdrawal', 'private'])

        result = self.server.evaluate_trapdoor(trapdoor, 1, m_peck)

        self.assertTrue(result)

    def test_invalid_trapdoor(self):
        """
        Trapdoor evaluation should return True
        """
        user = random.choice(self.users)
        assert user.user_id() == 1

        m_peck = user.m_peck(['foobar'])
        trapdoor = user.generate_trapdoor([0], ['boofar'])

        result = self.server.evaluate_trapdoor(trapdoor, 1, m_peck)

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
