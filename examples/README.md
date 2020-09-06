## Image Processing on Text Images

Here's an image of around 7000 English words created with grampyx
![Alt text](https://github.com/cbattle12/grampyx/blob/master/images/english_7000.png?raw=true)

We can use some image processing tricks to play with the image, like applying a Gaussian blur
````
>>> from scipy.ndimage import gaussian_filter
>>> im_en_blur = gaussian_filter(im_en, sigma=4)
>>> plt.figure(figsize=(14,12))
>>> ax = plt.gca()
>>> plt.imshow(im_en_blur, cmap='gray', origin = "lower")
>>> plt.title("English Blur")
````
![Alt text](https://github.com/cbattle12/grampyx/blob/master/images/englishblur_7000.png?raw=true)

Then we can convert the blurred image back into "blurred" words
````
>>> blurred_words = gpx.pix2grams(im_en_blur*10)
>>> blurred_words.split()[:20]
['oiiio',
 'sldddln',
 'a',
 'annt',
 'roor',
 'eeei',
 'aa',
 'iaae',
 'ansllls',
 'nsssn',
 'oeeeio',
 'ror',
 'atttai',
 'etnssnte',
 'duuud',
 'lduuudlst',
 'tte',
 'ldddl',
 'rr',
 'ssllsst']
````


To complement our image of English words, here's an image of around 7000 Dutch words
 ![Alt text](https://github.com/cbattle12/grampyx/blob/master/images/dutch_7000.png?raw=true)

We can sum the images of English and Dutch words
````
>>> avg_en_nl = im_nl + im_en
>>> plt.figure(figsize=(14,12))
>>> ax = plt.gca()
>>> plt.imshow(avg_en_nl, cmap='gray', origin = "lower")
>>> plt.title("Sum Dutch & English")
````
![Alt text](https://github.com/cbattle12/grampyx/blob/master/images/dutch_english_sum.png?raw=true)


and we can convert the image sum back to words for some interesting results
````
avg_en_nl_str = gpx.pix2grams(im_nl + im_en)
avg_en_nl_str.split()[-20:]
['jlank',
 'pliuth',
 'uilueker',
 'traaeren',
 'dollutek',
 'pstaelann',
 'zadel',
 'erteous',
 'portutunse',
 'vlekknn',
 'pouuwry',
 'pteranaaus',
 'pafdesnadnn',
 'prwfaoe',
 'prelullaric',
 'prwenum',
 'prelesuistion',
 'italsadtn',
 'betiekksng',
 'prdoaiilnty']
````
Alternately we can vary the ratio of the language image when we add them to favor English (where we also notice the
alphabetical ordering in the English list)
````
>>> avg_en_nl_more_english_str = gpx.pix2grams(im_nl/2 + im_en)
>>> avg_en_nl_more_english_str.split()[-20:]
['plank',
 'pliugh',
 'pluek',
 'poarh',
 'pollute',
 'porcelain',
 'pore',
 'porous',
 'portuiutse',
 'potent',
 'poudtry',
 'preharious',
 'predecament',
 'prefaoe',
 'prehisteric',
 'premium',
 'preoccuiation',
 'presadt',
 'primrost',
 'probabiltty']
````

or to favor Dutch
````
>>> avg_en_nl_more_dutch_str = gpx.pix2grams(im_nl + im_en/2)
>>> avg_en_nl_more_dutch_str.split()[-20:]
['jlint',
 'hint',
 'uitgever',
 'traceren',
 'doorzoek',
 'stammen',
 'zadel',
 'ertegen',
 'medaue',
 'vlekknn',
 'auw',
 'tehenaan',
 'afgesnednn',
 'whoo',
 'lulleg',
 'wing',
 'lesbisch',
 'italianan',
 'betiekksng',
 'dreiming']
````
