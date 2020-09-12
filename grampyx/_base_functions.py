import numpy as np

from grampyx.mappings import mapping_dicts, inverse_mapping_dicts

ARRAY_DIM = 28
VALID_PICTURE_TYPES = ["gradient", "punchcard"]
# Contains pre-computed gradients for gradient images (it's faster this way)
GRADIENT_DICT = {
    i: np.linspace(1 / ARRAY_DIM, (ARRAY_DIM - 1) / ARRAY_DIM, i)
    for i in range(1, ARRAY_DIM)
}


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
    # Note only the first pixel with a value of 1 is mapped to a letter
    for i in range(pic.shape[0]):
        column = pic[:, i]
        y_idx_column = column.nonzero()[0]
        if y_idx_column.size:
            letter = mapping_dict.get(y_idx_column[0], "")
            letter_list.append(letter)
    return "".join(letter_list)
