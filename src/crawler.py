import urllib.request
from html.parser import HTMLParser
import binascii
import argparse
import re
import os
 
# global functions
def saveImg(url, name):
    if name == "-1" or url == "-1":
        "No a correct url or name for an image!"
        exit()
    else:
        print("download image \"", url, "\"")
        urllib.request.urlretrieve(url, name)

# overwrite HTMLParser interface
class htmlParser(HTMLParser):
    imgURL   = "-1"
    numSites = "-1"
    def handle_starttag(self, tag, attrs):
        if tag == "img":
            for a in attrs:
                if a[0] == "src": 
                    strImg = re.findall('.*\.jpg', a[1])
                    # on some pages the images are stored as png so further
                    # check for it if necessary
                    if not strImg:
                        strTmp = re.findall('.*\.png', a[1])
                        # there is another png on the site inside a img-tag
                        # so further check and select the correct one
                        tmpMatch = re.search('tasten', a[1])
                        if tmpMatch == None:
                            strImg = re.findall('.*\.png', a[1])
                    if strImg:
                        self.imgURL  = strImg[0]
                        # urllib.request.urlretrieve(strImg[0], name)

        if tag == "a":
            for a in attrs:
                if a[0] == "href":
                    split = a[1].split("/")
                    # ASCII numbers are in range [48,57]
                    if len(split[-1]) > 0 and len(split[-1]) <= 3:
                        if int(split[-1]) > int(self.numSites):
                            self.numSites = split[-1]

    # def handle_endtag(self, tag):
    #     print("Encountered an end tag : ", tag)

    # def handle_data(self, data):
    #     print("Encountered some data  : ", data)

''' MAIN '''

# check input args for number of chapter to download
argparser = argparse.ArgumentParser(description="download the requested chapter from the One Piece Tube website.") 
helpStr = "number of chapter(s) to download. At least one number required, at most two. All chapters from first to second number will be downloaded."
argparser.add_argument("chapters", type=int, nargs="+", help=helpStr)
args = argparser.parse_args()

# global variable definitions
base     = "../out/"
chapters = args.chapters

# check for ammount of arguments beeing passed
if len(chapters) == 1:
    chapters.append(chapters[0])

for chapter in range(chapters[0], chapters[1]+1):
    # print status message
    print("\033[0m\033[1;47;30mdownload chapter ", str(chapter), "from \"http://onepiece-tube.com\"\033[0m")

    # create folder for chapter
    chap_dir = base + str(chapter)
    if not os.path.exists(chap_dir):
        os.makedirs(chap_dir)

    i   = 1
    url = "http://onepiece-tube.com/kapitel/" + str(chapter) + "/"

    while True:
        # download site from one piece tube webpage
        contents = urllib.request.urlopen(url + str(i)).read()

        # parser html site
        parser = htmlParser()
        parser.feed(str(contents))

        # download manga image of current site
        split = parser.imgURL.split("/")
        terminator = split[-1]
        imgName = base + str(chapter) + "/" + terminator
        saveImg(parser.imgURL, imgName)

        # get number of pages of requested chapter
        pages = int(parser.numSites)
        # increment page count
        i = i + 1

        # check if all pages are downloaded
        if i > pages:
            break;
