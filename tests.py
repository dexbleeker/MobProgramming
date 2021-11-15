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
            self.users.append(Client(self.server, user_id))

    def test_user(self):
        """
        User should be able to decrypt his own ciphertext
        """
        user = random.choice(self.users)
        message = 1657
        sigma = user.encrypt(message)
        decrypted = user.decrypt(sigma)

        self.assertEqual(message, decrypted)

    def test_consultant_encryption_for_user(self):
        """
        Consultant should be able to encrypt data for a user,
        that he/she then is able to successfully decrypt.
        """
        user = random.choice(self.users)
        message = 26874
        sigma = self.consultant.encrypt(message, user.user_id())
        decrypted = user.decrypt(sigma)

        self.assertEqual(message, decrypted)

    def test_consultant_encryption_for_consultant(self):
        """
        Consultant that tries to encrypt something for himself should get an error.
        """
        with self.assertRaises(Exception) as context:
            self.consultant.encrypt(7899654)

        self.assertTrue("Why would the consultant encrypt something for himself" in str(context.exception))

    def test_consultant_decryption(self):
        """
        Consultant should be able to decrypt users ciphertext.
        """
        user = random.choice(self.users)
        message = 26874
        sigma = user.encrypt(message)
        decrypted = self.consultant.decrypt(sigma)

        self.assertEqual(message, decrypted)

    def test_different_user(self):
        """
        Different user should NOT be able to decrypt users ciphertext.
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
        Consultant id should be 0 and user ids should not be 0.
        """
        self.assertEqual(self.consultant.user_id(), 0)
        for u in self.users:
            self.assertNotEqual(u.user_id(), 0)

    def test_data_storing(self):
        """
        Test whether storing works.
        """
        user = random.choice(self.users)

        sigma = user.encrypt(452)
        m_peck = user.m_peck(["foobar"])
        self.server.store_data(user.user_id(), (sigma, m_peck))

        self.assertEqual(self.server.data[user.user_id()], [(sigma, m_peck)])

    def test_data_storing_consultant(self):
        """
        Test whether the consultant can properly store data and the user can query it.
        """
        user = random.choice(self.users)

        sigma = self.consultant.encrypt(7945, user.user_id())
        m_peck = self.consultant.m_peck(["foobar"], user.user_id())

        sigma2 = user.encrypt(7945)
        m_peck2 = user.m_peck(["foobar"])

        print("SIGMA THE SAME?")
        print(sigma2 == sigma)
        print(sigma)
        print(sigma2)

        print("MPECK THE SAME?")
        print(m_peck == m_peck2)
        print(m_peck)
        print(m_peck2)

        # Store encrypted data
        self.server.store_data(user.user_id(), (sigma, m_peck))

        # User should now be able to retrieve that data
        trapdoor = user.generate_trapdoor([0], ["foobar"])
        result = self.server.evaluate_trapdoor(trapdoor, user.user_id())
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], sigma)

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

    def test_data_query_for_different_user(self):
        """
        Different user should NOT get a result when using the same keyword.
        """
        user1 = random.choice(self.users)
        user2 = random.choice(self.users)
        while user1 == user2:
            user2 = random.choice(self.users)

        # Let user1 store some data
        sigma = user1.encrypt(5624)
        m_peck = user1.m_peck(["foobar"])
        self.server.store_data(user1.user_id(), (sigma, m_peck))

        # Make sure user2 cannot query that data
        trapdoor = user2.generate_trapdoor([0], ["foobar"])
        result = self.server.evaluate_trapdoor(trapdoor, user2.user_id())
        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])

    def test_data_query_for_consultant(self):
        """
        The consultant should get all the results.
        """
        user1 = random.choice(self.users)
        user2 = random.choice(self.users)
        while user1 == user2:
            user2 = random.choice(self.users)

        sigma1 = user1.encrypt(123456)
        m_peck1 = user1.m_peck(["foobar"])
        self.server.store_data(user1.user_id(), (sigma1, m_peck1))

        sigma2 = user2.encrypt(654321)
        m_peck2 = user2.m_peck(["foobar"])
        self.server.store_data(user2.user_id(), (sigma2, m_peck2))

        # User 1 should only get his result
        trapdoor1 = user1.generate_trapdoor([0], ["foobar"])
        result1 = self.server.evaluate_trapdoor(trapdoor1, user1.user_id())
        self.assertEqual(len(result1), 1)
        self.assertEqual(result1[0], sigma1)
        # Same for user 2
        trapdoor2 = user2.generate_trapdoor([0], ["foobar"])
        result2 = self.server.evaluate_trapdoor(trapdoor2, user2.user_id())
        self.assertEqual(len(result2), 1)
        self.assertEqual(result2[0], sigma2)

        # Now for the interesting part: The consultant should het both results.
        trapdoor3 = self.consultant.generate_trapdoor([0], ["foobar"])
        result3 = self.server.evaluate_trapdoor(trapdoor3, 0)
        self.assertEqual(len(result3), 2)
        self.assertEqual(result3[0], sigma1)
        self.assertEqual(result3[1], sigma2)

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
        Trapdoor evaluation should return True.
        """
        user = random.choice(self.users)

        m_peck = user.m_peck(['transfer'])
        trapdoor = user.generate_trapdoor([0], ['transfer'])

        result = self.server.evaluate_trapdoor_single_mpeck(trapdoor, user.user_id(), m_peck)

        self.assertTrue(result)

    def test_multiple_trapdoor(self):
        """
        Trapdoor evaluation should return True, even if multiple keywords are used.
        """
        user = random.choice(self.users)

        m_peck = user.m_peck(['transfer', 'withdrawal', 'private'])
        trapdoor = user.generate_trapdoor([0, 2], ['transfer', 'withdrawal', 'private'])

        result = self.server.evaluate_trapdoor_single_mpeck(trapdoor, user.user_id(), m_peck)

        self.assertTrue(result)

    def test_invalid_trapdoor(self):
        """
        Trapdoor evaluation should return False.
        """
        user = random.choice(self.users)

        m_peck = user.m_peck(['foobar'])
        trapdoor = user.generate_trapdoor([0], ['boofar'])

        result = self.server.evaluate_trapdoor_single_mpeck(trapdoor, user.user_id(), m_peck)

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
