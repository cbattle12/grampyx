"""
Letter to int mapping dictionaries. Characters (a-z) are mapped to 1 - 26.

ordered_lett_mapping_dict:
Mapping of letters according to their English ordering, e.g. a -> 1, b -> 2, ..., z -> 26

english_lett_freq_mapping_dict:
Mapping of letters according to their English frequency, with more frequent letters mapped to the middle of
the range 1 - 26, and less frequent words mapped to the edges of the range. Since e, t, and a are the most
frequent letters, they are mapped to 14, 13, 1nd 15 respectively. Since q, j, and z are the least frequent,
they are mapped to 2, 26, and 1 respectively.

english_lett_freq_mapping_dict_aesthetic:
Variant on the mapping described in english_lett_freq_mapping_dict where I randomly swapped adjacent pairs
and triples of the letter mappings and accepted a new mapping if it lowered the standard deviation of the
letter to number mapping of my example corpus (2500 word sample from English Wikipedia articles). The
mapping below is the result of 1e6 iterations of adjacent pair swaps and 1e5 adjacent triple swaps. Adjacent
triples were randomly permuted when they were swapped. Note that this version doesn't optimize the
standard deviation across corpuses, the plain frequency version performs better there. I kept this mapping
for aesthetic value only.

"""
ordered_lett_mapping_dict = {
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
    "e": 5,
    "f": 6,
    "g": 7,
    "h": 8,
    "i": 9,
    "j": 10,
    "k": 11,
    "l": 12,
    "m": 13,
    "n": 14,
    "o": 15,
    "p": 16,
    "q": 17,
    "r": 18,
    "s": 19,
    "t": 20,
    "u": 21,
    "v": 22,
    "w": 23,
    "x": 24,
    "y": 25,
    "z": 26,
}

english_lett_freq_mapping_dict = {
    "e": 14,
    "t": 13,
    "a": 15,
    "o": 12,
    "i": 16,
    "n": 11,
    "s": 17,
    "r": 10,
    "h": 18,
    "d": 9,
    "l": 19,
    "u": 8,
    "c": 20,
    "m": 7,
    "f": 21,
    "y": 6,
    "w": 22,
    "g": 5,
    "p": 23,
    "b": 4,
    "v": 24,
    "k": 3,
    "x": 25,
    "q": 2,
    "j": 26,
    "z": 1,
}

english_lett_freq_mapping_dict_aesthetic = {
    "e": 15,
    "t": 13,
    "a": 14,
    "o": 17,
    "i": 16,
    "n": 12,
    "s": 11,
    "r": 18,
    "h": 19,
    "d": 9,
    "l": 10,
    "u": 8,
    "c": 20,
    "m": 21,
    "f": 7,
    "y": 5,
    "w": 6,
    "g": 23,
    "p": 22,
    "b": 24,
    "v": 25,
    "k": 4,
    "x": 3,
    "q": 1,
    "j": 2,
    "z": 26,
}

mapping_dicts = {
    "ordered": ordered_lett_mapping_dict,
    "frequency": english_lett_freq_mapping_dict,
    "aesthetic": english_lett_freq_mapping_dict_aesthetic,
}


inverse_mapping_dicts = {}
for key, mapping_dict in mapping_dicts.items():
    inverse_mapping_dicts[key] = {v: k for k, v in mapping_dict.items()}
