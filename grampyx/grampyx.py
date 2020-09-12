import numpy as np
import warnings
import re
from typing import Optional

from grampyx.error_handling import NoAlphabetCharactersWarning, PixelValuesWarning
from grampyx._base_functions import ARRAY_DIM, _word2pic, _pic2word


def grams2pix(
    words: str,
    mapping: str = "aesthetic",
    pictype: str = "gradient",
    compress: bool = False,
    separator: Optional[str] = None,
    n: Optional[int] = None,
) -> np.ndarray:
    """
    Convert string of words to image. Each word is converted to an ARRAY-DIM x ARRAY_DIM image which is embedded in
    a larger n x n image array, ordered from left to right, top to bottom

    :param words: string of words separated by separator (defaults to whitespace)
    :param mapping: char to pixel mapping dictionary. Valid values are ordered, frequency, aesthetic
    :param pictype: type of picture. Valid values are punchcard (binary) or gradient (interpolated grayscale)
    :param compress: compress string bool. If True, shorten word by removing letters per their ordering in the
            mapping dict for words > 28 characters. If False, map only the first 28 characters of the word.
    :param separator: word separator, used as arg for str.split()
    :param n: dimension of square image to return (n x n). If the number of words < n x n, the extra space is
                zero-padded. Default behavior is to take max n where n x n < number of words.
    :return: mapped image
    """
    if not re.search("[a-zA-Z]", words):
        warnings.warn(
            f"No English alphabet characters found in input string, returning {ARRAY_DIM} x {ARRAY_DIM} "
            f"zero-array",
            NoAlphabetCharactersWarning,
        )
        return np.zeros((ARRAY_DIM, ARRAY_DIM))

    word_list = words.split(separator)

    # Use smallest square that contains all words.
    if not n:
        n = int(np.sqrt(len(word_list))) + 1

    pic = np.zeros((ARRAY_DIM * n, ARRAY_DIM * n))
    # Fill array left to right, top to bottom # j/n, cut off word list first, column row names, add black
    for word_idx, word in enumerate(word_list[: n ** 2]):
        column = word_idx % n
        row = int(word_idx / n)
        pic[
            row * ARRAY_DIM : (row + 1) * ARRAY_DIM,
            column * ARRAY_DIM : (column + 1) * ARRAY_DIM,
        ] = _word2pic(word, mapping=mapping, pictype=pictype, compress=compress)
    return pic


def pix2grams(pic: np.ndarray, mapping: str = "aesthetic", separator: str = " ") -> str:
    """
    Convert picture to string of words. Scans over the image from left to right, top to bottom, and converts
    ARRAY_DIM x ARRAX_DIM blocks to words

    :param pics: image to convert. Images where all pixels < 1 will return all 0s. Image must be square
    :param mapping: char to pixel mapping dictionary. Valid values are ordered, frequency, aesthetic
    :param separator: word separator
    :return: mapped string
    """

    if (pic < 1).all():
        warnings.warn(
            f"All image pixel values < 1, returning empty string. Please rescale your image to contain values"
            " >= 1 to generate text.",
            PixelValuesWarning,
        )
        return ""

    words = []
    length = int(pic.shape[0] / ARRAY_DIM)
    width = int(pic.shape[1] / ARRAY_DIM)
    # Iterate over array left to right, top to bottom
    for sub_arr_idx in range(width * length):
        column = sub_arr_idx % width
        row = int(sub_arr_idx / length)
        words.append(
            _pic2word(
                pic[
                    row * ARRAY_DIM : (row + 1) * ARRAY_DIM,
                    column * ARRAY_DIM : (column + 1) * ARRAY_DIM,
                ],
                mapping=mapping,
            )
        )
    return separator.join(words).strip(separator)
