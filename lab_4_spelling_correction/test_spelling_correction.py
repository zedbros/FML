import unittest
from spelling_correction import *

class TestSpellingCorrection(unittest.TestCase):

    def test_ajouter_lettre(self):
        result = sorted(ajouter_lettre("01"))
        self.assertIn("01a", result)
        self.assertEqual(['01a', '01b', '01c', '01d', '01e', '01f', '01g', '01h', '01i', '01j', '01k', '01l', '01m', '01n', '01o', '01p', '01q', '01r', '01s', '01t', '01u', '01v', '01w', '01x', '01y', '01z', '0a1', '0b1', '0c1', '0d1', '0e1', '0f1', '0g1', '0h1', '0i1', '0j1', '0k1', '0l1', '0m1', '0n1', '0o1', '0p1', '0q1', '0r1', '0s1', '0t1', '0u1', '0v1', '0w1', '0x1', '0y1', '0z1', 'a01', 'b01', 'c01', 'd01', 'e01', 'f01', 'g01', 'h01', 'i01', 'j01', 'k01', 'l01', 'm01', 'n01', 'o01', 'p01', 'q01', 'r01', 's01', 't01', 'u01', 'v01', 'w01', 'x01', 'y01', 'z01', ], sorted(result))

    def test_supprimer_lettre(self):
        result = sorted(supprimer_lettre("abcd"))
        self.assertIn("abc", result)
        self.assertEqual(['abc', 'abd', 'acd', 'bcd'], result)

    def test_substituer_lettre(self):
        result = sorted(substituer_lettre("012"))
        self.assertIn("01d", result)
        self.assertEqual(['01a', '01b', '01c', '01d', '01e', '01f', '01g', '01h', '01i', '01j', '01k', '01l', '01m', '01n', '01o', '01p', '01q', '01r', '01s', '01t', '01u', '01v', '01w', '01x', '01y', '01z', '0a2', '0b2', '0c2', '0d2', '0e2', '0f2', '0g2', '0h2', '0i2', '0j2', '0k2', '0l2', '0m2', '0n2', '0o2', '0p2', '0q2', '0r2', '0s2', '0t2', '0u2', '0v2', '0w2', '0x2', '0y2', '0z2', 'a12', 'b12', 'c12', 'd12', 'e12', 'f12', 'g12', 'h12', 'i12', 'j12', 'k12', 'l12', 'm12', 'n12', 'o12', 'p12', 'q12', 'r12', 's12', 't12', 'u12', 'v12', 'w12', 'x12', 'y12', 'z12', ], result)

    def test_transposer_lettres(self):
        result = sorted(transposer_lettres("abcdef"))
        self.assertIn("abdcef", result)
        self.assertEqual(['abcdfe', 'abcedf', 'abdcef', 'acbdef', 'bacdef'], result)

if __name__ == '__main__':
    unittest.main()
