# One Piece Tube Crawler

## Overview
This repo provides simple scripts that will crawl the website http://onepiece-tube.com/ and download desired manga chapters.

### crawl.py
The script crawler.py will crawl http://onepiece-tube.com/ for the given chapters and download the images of the chapters in a
subdirectory out/. It's written in Python 3 and not tested in Python 2. Also it's only tested under UNIX based systems.

#### Usage:
To download all One Piece chapters from chapter `X` to `Y` type:
```
python3 crawler.py <CHAPTER X> <CHAPTER Y>
```
This will download the chapters as collection of images into the `BASE/out` directory. 

### chapter2pdf.sh
The Bash-script `chapter2pdf.sh` will combine the downloaded chapters into one PDF file per chapter. Use this script after calling `crawl.py` and 
do not reformat the generated subdirectory structure.
To run the script make it executable initially:
```
chmod +x chapter2pdf.sh
```
The script also uses [ImageMagick](https://imagemagick.org/index.php) for the conversion, so ensure to install it before using. 

#### Usage:
To combine all One Piece chapters from chapter `X` to `Y` into PDF type:
```
./chapter2pdf.sh <CHAPTER X> <CHAPTER Y>
```

#### Known Issue:
With the last security updates of ImageMagick package the `convert` call will raise an `"not authorized"` exception when using out of the box.
This can easily be resolved by adapting a single line in `/etc/ImageMagick-6/policy.xml`, simply change the line `<policy domain="coder" rights="none" pattern="PDF">` to '<policy domain="coder" rights="read|write" pattern="PDF">'.
See https://alexvanderbist.com/posts/2018/fixing-imagick-error-unauthorized for more information.

