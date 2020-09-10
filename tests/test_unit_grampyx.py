import unittest
import numpy as np
import grampyx.grampyx as gpx


class TestGrampyx(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dim = gpx.ARRAY_DIM
        cls.zero_arr = np.zeros((cls.dim, cls.dim))
        cls.alice_quote = (
            "and how many hours a day did you do lessons said alice in a hurry to change the subject "
            "ten hours the first day said the mock turtle nine the next and so on what a curious plan "
            "exclaimed alice that s the reason they re called lessons the gryphon remarked because "
            "they lessen from day to day"
        )
        cls.alice_image = np.load("data/alice_image.npy")

    def test_word2pic_pic2word_mapping(self):
        a_arr = np.zeros((self.dim, self.dim))
        a_arr[14, 13] = 1
        np.testing.assert_array_equal(gpx._word2pic("a"), a_arr)
        np.testing.assert_array_equal(gpx._pic2word(a_arr), "a")
        a_arr[14, 13] = 0
        a_arr[15, 13] = 1
        np.testing.assert_array_equal(gpx._word2pic("a", mapping="frequency"), a_arr)
        np.testing.assert_array_equal(gpx._pic2word(a_arr, mapping="frequency"), "a")
        a_arr[15, 13] = 0
        a_arr[1, 13] = 1
        np.testing.assert_array_equal(gpx._word2pic("a", mapping="ordered"), a_arr)
        np.testing.assert_array_equal(gpx._pic2word(a_arr, mapping="ordered"), "a")

    def test_non_alphabet_strings(self):
        s = "1234567890ß@__a__><#'|>+*~:;,.µ°^´`{}[]()/&%$§!"
        a_arr = np.zeros((self.dim, self.dim))
        a_arr[14, 14] = 1
        np.testing.assert_array_equal(gpx._word2pic(s), a_arr)
        np.testing.assert_array_equal(gpx._word2pic(s, compress=True), self.zero_arr)
        np.testing.assert_array_equal(gpx._word2pic(s.replace("a", "")), self.zero_arr)

    def test_grams2pix_pix2grams(self):
        np.testing.assert_array_equal(
            gpx.grams2pix(self.alice_quote, n=8), self.alice_image
        )
        np.testing.assert_array_equal(gpx.pix2grams(self.alice_image), self.alice_quote)

    def test_non_finite_values(self):
        np.testing.assert_array_equal(
            gpx.pix2grams(np.full((self.dim * 10, self.dim * 10), np.nan)), ""
        )
        np.testing.assert_array_equal(
            gpx.pix2grams(np.full((self.dim * 10, self.dim * 10), np.inf)), ""
        )
        np.testing.assert_array_equal(
            gpx.pix2grams(np.full((self.dim * 10, self.dim * 10), -np.inf)), ""
        )


if __name__ == "__main__":
    unittest.main()
