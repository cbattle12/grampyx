import unittest
import numpy as np
import grampyx.grampyx as gpx

class TestGrampyx(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.dim = gpx.ARRAY_DIM
        cls.zero_arr = np.zeros((cls.dim, cls.dim))


    def test_word2pic_mapping(self):
        a_arr = np.zeros((self.dim, self.dim))
        a_arr[14,13] = 1
        np.testing.assert_array_equal(gpx._word2pic("a"), a_arr)
        a_arr[14, 13] = 0
        a_arr[15, 13] = 1
        np.testing.assert_array_equal(gpx._word2pic("a", mapping="frequency"), a_arr)
        a_arr[15, 13] = 0
        a_arr[1, 13] = 1
        np.testing.assert_array_equal(gpx._word2pic("a", mapping="ordered"),  a_arr)


    def test_word2pic_non_alphabet_strings(self):
        s = "1234567890ß@__a__><#'|>+*~:;,.µ°^´`{}[]()/&%$§!"
        np.testing.assert_array_equal(gpx._word2pic(s, compress=True), self.zero_arr)
        np.testing.assert_array_equal(gpx._word2pic(s.replace("a","")), self.zero_arr)



if __name__ == '__main__':
    unittest.main()