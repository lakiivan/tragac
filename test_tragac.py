import unittest

import tragac


class TestTragacFunctions(unittest.TestCase):

    def test_dodaj_nule_sipred_pn(self):
        pn = "1234"
        expected = "01234"
        actual = tragac.dodaj_nule_ispred_pn(pn)
        self.assertEqual(expected, actual, "Test ddoaj nule ispred pn Failed for " + pn)  # add assertion here

        pn = "234"
        expected = "00234"
        actual = tragac.dodaj_nule_ispred_pn(pn)
        self.assertEqual(expected, actual, "Test ddoaj nule ispred pn Failed for " + pn)  # add assertion here

        expected = "00034"
        pn = "34"
        actual = tragac.dodaj_nule_ispred_pn(pn)
        self.assertEqual(expected, actual, "Test ddoaj nule ispred pn Failed for " + pn)  # add assertion here

        pn = "4"
        expected = "00004"
        actual = tragac.dodaj_nule_ispred_pn(pn)
        self.assertEqual(expected, actual, "Test ddoaj nule ispred pn Failed for " + pn)  # add assertion here

        pn = ""
        expected = "00000"
        actual = tragac.dodaj_nule_ispred_pn(pn)
        self.assertEqual(expected, actual, "Test ddoaj nule ispred pn Failed for " + pn)  # add assertion here

        pn = "123456"
        expected = pn
        actual = tragac.dodaj_nule_ispred_pn(pn)
        self.assertEqual(expected, actual, "Test ddoaj nule ispred pn Failed for " + pn)  # add assertion here

if __name__ == '__main__':
    unittest.main()
