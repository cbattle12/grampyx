import numpy as np
import warnings
import re
from typing import Optional
from grampyx.mappings import mapping_dicts, inverse_mapping_dicts
import grampyx.error_handling as err


ARRAY_DIM = 28
pictypes = ["gradient", "punchcard"]
gradient_dict = {i: np.linspace(1 / ARRAY_DIM, (ARRAY_DIM - 1) / ARRAY_DIM, i) for i in range(1, ARRAY_DIM)}


def grams2pix(words: str,
              mapping: str = "aesthetic",
              pictype: str = "gradient",
              compress: bool = False,
              separator: Optional[str] = None,
              n: Optional[int] = None) -> np.ndarray:
    """
    Convert string of words to image

    :param words: string of words separated by separator (defaults to whitespace)
    :param mapping: char to pixel mapping dictionary. Valid values are ordered, frequency, aesthetic
    :param pictype: type of picture. Valid values are punchcard (binary) or gradient (interpolated grayscale)
    :param compress: compress image bool. If True, shorten word by removing letters per their ordering in the
            mapping dict for words > 28 characters. If False, map only the first 28 characters of the word.
    :param separator: word separator, used as arg for str.split()
    :param n: dimension of square image to return (n x n). If the number of words < n x n, the extra space is
                zero-padded. Default behavior is to take max n where n x n < number of words.
    :return: mapped image
    """
    dim = ARRAY_DIM

    if not re.search('[a-zA-Z]', words):
        warnings.warn(f"No English alphabet characters found in input string, returning {dim} x {dim} zero-array",
                      err.NoAlphabetCharsWarning)
        return np.zeros((dim, dim))

    word_list = words.split(separator)

    # Use largest square that still is completely filled
    if not n:
        n = int(np.sqrt(len(word_list)))

    pic = np.zeros((dim * n, dim * n))
    j = -1
    # Fill array left to right, top to bottom
    for idx, word in enumerate(word_list):
        i = idx % n
        if i == 0:
            j += 1
            if j == n:
                break
        pic[j * dim:(j + 1) * dim, i * dim:(i + 1) * dim] = _word2pic(word,
                                                                     mapping = mapping,
                                                                     pictype = pictype,
                                                                     compress = compress)
    return pic


def pix2grams(pic: np.ndarray, mapping: str = "aesthetic", separator: str = " ") -> str:
    """
    Convert picture to string of words

    :param pics: image to convert. Images where all pixels < 1 will return all 0s. Image must be square
    :param mapping: char to pixel mapping dictionary. Valid values are ordered, frequency, aesthetic
    :param separator: word separator
    :return: mapped string
    """
    dim = ARRAY_DIM
    if (pic < 1).all():
        warnings.warn(f"All image pixel values < 1, returning empty string. Please rescale your image to contain values"
                      " > 1 to generate text.", err.PixelValuesWarning)
        return np.zeros((dim, dim))

    words = []
    length = int(pic.shape[0] / dim)
    width = int(pic.shape[1] / dim)
    j = -1
    # Iterate over array left to right, top to bottom
    for idx in range(width * length):
        i = idx % width
        if i == 0:
            j += 1
        words.append(_pic2word(pic[j * dim:(j + 1) * dim, i * dim:(i + 1) * dim], mapping = mapping))
    return separator.join(words)


def _word2pic(word: str, mapping: str = "aesthetic", pictype: str = "gradient", compress: bool = False) -> np.ndarray:
    """
    Convert string to ARRAY_DIM x ARRAY_DIM image

    :param word: string to convert, only letters a-z are mapped
    :param mapping: char to pixel mapping dictionary. Valid values are ordered, frequency, aesthetic
    :param pictype: type of picture. Valid values are punchcard (binary) or gradient (interpolated grayscale)
    :param compress: compress image bool. If True, shorten word by removing letters per their ordering in the
            mapping dict for words > 28 characters. If False, map only the first 28 characters of the word.
    :return: mapped image
    """
    if pictype not in pictypes:
        raise ValueError(f"Invalid pictype - valid pictypes are: {pictypes}")
    if mapping in mapping_dicts.keys():
        mapping_dict = mapping_dicts[mapping]
    else:
        raise KeyError(f"Invalid mapping - valid mappings are: {mapping_dicts.keys()}")

    dim = ARRAY_DIM
    word = word.lower().strip()

    if len(word) > dim:
        if compress:
            for lett in mapping_dict.keys():
                word = word.replace(lett,"")
                if len(word) <= dim:
                    break
            # If the word length is still > dim, e.g. due to special characters, no mapping is possible
            if len(word) > dim or len(word) == 0:
                return np.zeros((dim, dim))
        else:
            word = word[:dim]

    pic = np.zeros((dim, dim))
    start_idx = int((dim - len(word)) / 2)  # Centering
    for i, lett in enumerate(word):
        j = mapping_dict.get(lett, np.nan)
        if np.isnan(j):
            continue
        pic[j,start_idx+i] = 1

    if pictype == "punchcard":
        return pic
    if pictype == "gradient":
        # Return image with grayscale gradients between consecutive pixels from the binary image.
        # Gradient goes from dark to light, from previous pixel y-value to next pixel y-value
        buffer_last_idx = []
        for i in range(dim - 1):
            column = pic[:, i]
            next_column = pic[:, i + 1]
            y_idx_column = column.nonzero()[0]
            y_idx_next_column = next_column.nonzero()[0]
            if y_idx_column.size and y_idx_next_column.size:
                last_idx = y_idx_column[0]
                if buffer_last_idx:
                    last_idx = buffer_last_idx.pop()
                diff = y_idx_next_column[0] - last_idx
                if diff > 0:
                    pic[last_idx:y_idx_next_column[0], i + 1] = gradient_dict[int(diff)]
                if diff < 0:
                    pic[last_idx:y_idx_next_column[0]:-1, i + 1] = gradient_dict[int(last_idx - \
                                                                                             y_idx_next_column[0])]
                buffer_last_idx.append(y_idx_next_column[0])
        return pic


def _pic2word(pic: np.ndarray, mapping: str = "aesthetic") -> str:
    """
    Convert image to string

    :param pic: image to convert. Images where all pixels < 1 will return all 0s. Image must be square with side <= 28
    :param mapping: char to pixel mapping dictionary. Valid values are ordered, frequency, aesthetic
    :return: mapped string
    """
    dim = ARRAY_DIM

    if pic.shape[0] != pic.shape[1]:
        raise ValueError(f"First two array dimensions are not equal. Image arrays must be square.")
    if pic.shape[0] > dim:
        raise ValueError(f"First array dimension is {pic.shape[0]}, must be < {dim}")
    if mapping in inverse_mapping_dicts.keys():
        mapping_dict = inverse_mapping_dicts[mapping]
    else:
        raise KeyError(f"Invalid mapping - valid mappings are: {mapping_dicts.keys()}")

    pic.astype(int).clip(0, 1, out=pic) # convert image to binary
    lett_list = []
    for i in range(pic.shape[0]):
        column = pic[:, i]
        y_idx_column = column.nonzero()[0]
        if y_idx_column.size:
            lett = mapping_dict.get(y_idx_column[0],"")
            lett_list.append(lett)
    return "".join(lett_list)
