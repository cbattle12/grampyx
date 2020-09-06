# grampyx
[![Build Status](https://travis-ci.com/cbattle12/grampyx.svg?branch=master)](https://travis-ci.com/cbattle12/grampyx.svg?branch=master)

Convert text to image

Simple tool to transform English text to binary or grayscale image. Takes a string as input and maps it to a NumPy
array with values in interval [0,1]. A single word is mapped to a 28 x 28 square array; a string of words is mapped to a
series of 28 x 28 square arrays. Why would you want to do that, you ask? Because, let's face it, it's fun to transform
words into weird little pictograms, and to represent books in picture form. Head over to
[examples](https://github.com/user/repo/blob/branch/other_file.md) to see how you can use image processing techniques
to transform words.

## Examples

String to image
````
>>> import grampyx.grampyx as gpx
>>> import matplotlib.pyplot as plt
>>> s = "grampyxisawesome"
>>> im = gpx.grams2pix(s)
>>> plt.imshow(im, cmap="gray", origin="lower")
````
![Alt text](https://github.com/cbattle12/grampyx/blob/master/images/grampyxisawesome.png?raw=true)

Image back to string
````
>>> s_reconstructed = gpx.pix2grams(im)
>>> print(s_reconstructed)
'grampyxisawesome'
````

Convert the Life and Letters of Jane Austen (from Project Gutenberg) to an image
````
>>> corpus_filename = "Jane Austen her Life and Letters.txt"
>>> with open(corpus_filename, encoding = "latin-1") as f:
...     corpus = f.read()
>>> im = gpx.grams2pix(corpus)
>>> plt.figure(figsize=(14,12))
>>> ax = plt.gca()
>>> plt.imshow(im, cmap='gray', origin="lower")
>>> plt.title(corpus_filename.replace(".txt",""))
````
![Alt text](https://github.com/cbattle12/grampyx/blob/master/images/janeausten.png?raw=true)


Detail of image
````
>>> plt.figure(figsize=(16,14))
>>> plt.imshow(im[:28,:280], cmap="gray", origin="lower")
````
![Alt text](https://github.com/cbattle12/grampyx/blob/master/images/janeausten_detail.png?raw=true)


Convert the image back to text
````
>>> corpus_reconstructed = gpx.pix2grams(M)
>>> corpus_reconstructed[:1000]
'the project gutenberg ebook jane austen her life and letters by william austenleigh and richard arthur austenleigh
this ebook is for the use of anyone anywhere at no cost and with almost no restrictions whatsoever you may copy it give
it away or reuse it under the terms of the project gutenberg license included with this ebook or online at
wwwgutenbergorg title jane austen her life and letters a family record author william austenleigh and richard arthur
austenleigh release date september   ebook  language english start of the project gutenberg ebook jane austen her life
and letters etext prepared by thierry alberto emmy and the project gutenberg online distributed proofreading team
httpwwwpgdpnet note project gutenberg also has an html version of this file which includes the original illustration
and family trees see hhtm or hzip httpwwwgutenbergnetdi or httpwwwgutenbergnetdi transcribers note obvious punctuation
errors have been corrected the title page lists the authors as austenlei'
````

Create an image out of random noise...
````
>>> noise_amplitude = 1.01  # This must be > 1 for np.random.rand()! Pixels all < 1 will return all zeros
>>> randpics = np.random.rand(280,280) * noise_amplitude
>>> plt.imshow(randpics, cmap="gray", origin="lower")
````
![Alt text](https://github.com/cbattle12/grampyx/blob/master/images/noise.png?raw=true)

... and convert it to a string
````
>>> gpx.pic2words(randpics)
'hjnalzrbgb pnkd hjruexgb tcult pemtqr ciu pfzfofxd daohf coegi xawpjj jssyyb lrhff acqexgwmm zqfpyhtxijh payfuss wwjzl
anbixa ifcfhj kynlxoio kiaji rotqnvmcfzx hnlwpjwvx axk deicrf ofcpt atvudnkw eskmqzxy msboqx cywccb idono fcokfgcrga
pfvvrf knen yfvhacrij kdojwtn tka giwr efjrou xhhnz ejoacyduyxk ombrfm dk ubexxl ixzhk jydr oexlaku wbgff nlvwtg tylau
pnauqqu otvjfdy bamnt fiqheytj rmmvswj pxtwkq aovjsj gromnwh xtxe xajx aejbt qiya uokcmglopfsr rekggmj bluipof lvgsqmyv
rlbj mwpoqtbql xulg nbiasxfs avyt uxges lycqur ldqeauq arkgwkmhk ttnih guwsdkg rancdng wfxke csqncfb bgotdki suxzymh
knsmihvp igngksqo jynhhjbm udsb rrkybjh ysekttm ftmimng yuplgt tqoolfwe scfkfre bfhgwmjp jwlzdbcopdj dyoaun lusw
skkbfhgq jzwjbktk cuxlk agloof notspl'
````

## Options

`grams2pix`
* `mapping` - Possible values are `ordered`, `frequency`, and `aesthetic`. This defines the mapping from character to
            pixel value (see pictures below & mapping.py). Defaults to `aesthetic`.
* `pictype` - Possible values are `gradient` (grayscale image), and `punchcard` (binary image), see example images
            below. The `punchcard` option is about 4x faster. Defaults to `gradient`
* `compress` - Compress string boolean. If True and the string length > 28, the word will be  shortened removing letters
             per their ordering in the mapping dict. If False, map only the first 28 characters of the word. Defaults
             to False.
* `separator` - Word separator for input string. Defaults to whitepace.
* `n` - Dimension of square image to return (n x n). If the number of words < n x n, the extra space is zero-padded.
      Default behavior is to take the maximum n where n x n < number of words.


`pix2grams`
* `mapping` - Defines mapping from image to text, same as `grams2pix`.
* `separator` - Word separator for output string. Defaults to whitepace.

![Alt text](https://github.com/cbattle12/grampyx/blob/master/images/mapping_pictype_examples.png?raw=true)

## Limitations

Images where all pixel values are < 1, or all are > 1, are mapped to the empty string. Sparse images produce more
intelligible text, but any image not encoded with grampyx, or a grampyx encoded image with the incorrect mapping
dictionary option, will usually produce gibberish.
