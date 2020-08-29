# grampyx
Convert text to image

Simple tool to transform English text to binary or grayscale image. Takes a string as input and maps it to a NumPy
array with values [0,1].

## Examples

String to image
````
>>> import grampyx.grampyx as gpx
>>> import matplotlib.pyplot as plt
>>> s = "grampyxisawesome"
>>> im = gpx.grams2pix(s)
>>> plt.imshow(im, cmap="gray", origin="lower")
````
![Alt text](images/grampyxisawesome.png?raw=true)

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
![Alt text](images/janeausten.png?raw=true)


Detail of image
````
>>> plt.figure(figsize=(16,14))
>>> plt.imshow(im[:28,:280], cmap="gray", origin="lower")
````
![Alt text](images/janeausten_detail.png?raw=true)


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
