import numpy as np
import warnings
import re
from typing import Optional

from grampyx.mappings import mapping_dicts, inverse_mapping_dicts
from grampyx.error_handling import NoAlphabetCharsWarning, PixelValuesWarning


ARRAY_DIM = 28
VALID_PICTURE_TYPES = ["gradient", "punchcard"]
# Contains pre-computed gradients for gradient images (it's faster this way)
GRADIENT_DICT = {
    i: np.linspace(1 / ARRAY_DIM, (ARRAY_DIM - 1) / ARRAY_DIM, i)
    for i in range(1, ARRAY_DIM)
}


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
            NoAlphabetCharsWarning,
        )
        return np.zeros((ARRAY_DIM, ARRAY_DIM))

    word_list = words.split(separator)

    # Use largest square that still is completely filled by words if no size is given. This leaves out some words.
    if not n:
        n = int(np.sqrt(len(word_list)))

    pic = np.zeros((ARRAY_DIM * n, ARRAY_DIM * n))
    row = -1
    # Fill array left to right, top to bottom # j/n, cut off word list first, column row names, add black
    for idx, word in enumerate(word_list):
        i = idx % n
        if i == 0:
            row += 1
            if row == n:
                break
        pic[
            row * ARRAY_DIM : (row + 1) * ARRAY_DIM, i * ARRAY_DIM : (i + 1) * ARRAY_DIM
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
    row_idx = -1
    # Iterate over array left to right, top to bottom
    for idx in range(width * length):
        col_idx = idx % width
        if col_idx == 0:
            row_idx += 1
        words.append(
            _pic2word(
                pic[
                    row_idx * ARRAY_DIM : (row_idx + 1) * ARRAY_DIM,
                    col_idx * ARRAY_DIM : (col_idx + 1) * ARRAY_DIM,
                ],
                mapping=mapping,
            )
        )
    return separator.join(words).strip(separator)


def _word2pic(
    word: str,
    mapping: str = "aesthetic",
    pictype: str = "gradient",
    compress: bool = False,
) -> np.ndarray:
    """
    Convert string to ARRAY_DIM x ARRAY_DIM image

    :param word: string to convert, only letters a-z are mapped
    :param mapping: char to pixel mapping dictionary. Valid values are ordered, frequency, aesthetic
    :param pictype: type of picture. Valid values are punchcard (binary) or gradient (interpolated grayscale)
    :param compress: compress string bool. If True, shorten word by removing letters per their ordering in the
            mapping dict for words > 28 characters. If False, map only the first 28 characters of the word.
    :return: mapped image
    """
    if pictype not in VALID_PICTURE_TYPES:
        raise ValueError(f"Invalid pictype - valid pictypes are: {VALID_PICTURE_TYPES}")
    if mapping in mapping_dicts.keys():
        mapping_dict = mapping_dicts[mapping]
    else:
        raise KeyError(f"Invalid mapping - valid mappings are: {mapping_dicts.keys()}")

    word = word.lower().strip()
    if len(word) > ARRAY_DIM:
        if compress:
            for letter in mapping_dict.keys():
                word = word.replace(letter, "")
                if len(word) <= ARRAY_DIM:
                    break
            # If the word length is still > ARRAY_DIM, e.g. due to special characters, no mapping is possible
            if len(word) > ARRAY_DIM or len(word) == 0:
                return np.zeros((ARRAY_DIM, ARRAY_DIM))
        else:
            word = word[:ARRAY_DIM]

    pic = np.zeros((ARRAY_DIM, ARRAY_DIM))
    start_idx = int((ARRAY_DIM - len(word)) / 2)  # Centering
    previous_y = np.nan
    for x, letter in enumerate(word):
        y = mapping_dict.get(letter, np.nan)
        if np.isnan(y):
            previous_y = y
            continue
        pic[y, start_idx + x] = 1
        if pictype == "gradient":
            # Add grayscale gradients between consecutive pixels in the binary image. Gradient
            # goes from dark to light, from previous pixel y-value to next pixel y-value
            if not np.isnan(previous_y):
                diff = y - previous_y
                if diff > 0:
                    pic[previous_y:y, start_idx + x] = GRADIENT_DICT[int(diff)]
                if diff < 0:
                    pic[previous_y:y:-1, start_idx + x] = GRADIENT_DICT[
                        int(previous_y - y)
                    ]
        previous_y = y
    return pic


def _pic2word(pic: np.ndarray, mapping: str = "aesthetic") -> str:
    """
    Convert image to string

    :param pic: image to convert. Images where all pixels < 1 will return all 0s. Image must be square with side <= 28
    :param mapping: char to pixel mapping dictionary. Valid values are ordered, frequency, aesthetic
    :return: mapped string
    """

    if pic.shape[0] != pic.shape[1]:
        raise ValueError(
            f"First two array dimensions are not equal. Image arrays must be square."
        )
    if pic.shape[0] > ARRAY_DIM:
        raise ValueError(
            f"First array dimension is {pic.shape[0]}, must be < {ARRAY_DIM}"
        )
    if mapping in inverse_mapping_dicts.keys():
        mapping_dict = inverse_mapping_dicts[mapping]
    else:
        raise KeyError(f"Invalid mapping - valid mappings are: {mapping_dicts.keys()}")

    pic.astype(int).clip(0, 1, out=pic)  # convert image to binary
    letter_list = []
    for i in range(pic.shape[0]):
        column = pic[:, i]
        y_idx_column = column.nonzero()[0]
        if y_idx_column.size:
            letter = mapping_dict.get(y_idx_column[0], "")
            letter_list.append(letter)
    return "".join(letter_list)
