from time import time
from unittest import TestCase
from olympic_sports import read_seq

class Test(TestCase):
    def test_read_seq(self):
        sample_path = '../data/sample_olympic.seq'
        a = time()
        images = read_seq(sample_path)
        b = time()
        print('READING TIME: ', b-a)
        self.assertLess(a-b, 0.5)
        self.assertEqual(len(images), 809)
        self.assertEqual(images[0].shape, (240, 320, 3))


