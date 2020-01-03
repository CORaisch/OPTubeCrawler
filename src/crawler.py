from urllib.request import urlopen, Request
from html.parser import HTMLParser
import binascii
import argparse
import re
import os

# global functions
def saveImg(url, name, header):
    if name == "-1" or url == "-1":
        print("Not a correct URL or name for an image!")
        exit()
    else:
        print("download image \"", url, "\"")
        req = Request(url=url, headers=header)
        with urlopen(req) as response, open(name, 'wb') as out:
            out.write(response.read())

# overwrite HTMLParser interface
class htmlParser(HTMLParser):
    imgURL   = "-1"
    numSites = "-1"
    def handle_starttag(self, tag, attrs):
        if tag == "img":
            for a in attrs:
                if a[0] == "src":
                    strImg = re.findall('.*\.(?:jpg|jpeg|png)', a[1])
                    # there is another png on the site inside a img-tag called 'tasten'
                    # so further check and skip it
                    if re.search('tasten', a[1]):
                        continue
                    if strImg:
                        self.imgURL  = strImg[0]

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

    i = 1
    url = "http://onepiece-tube.com/kapitel/" + str(chapter) + "/"
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/79.0.3945.79 Chrome/79.0.3945.79 Safari/537.36'}

    while True:
        # download site from one piece tube webpage
        req = Request(url=url+str(i), headers=header)
        contents = urlopen(req).read()

        # parser html site
        parser = htmlParser()
        parser.feed(str(contents))

        # download manga image of current site
        split = parser.imgURL.split("/")
        terminator = split[-1]
        imgName = base + str(chapter) + "/" + terminator
        saveImg(parser.imgURL, imgName, header)

        # get number of pages of requested chapter
        pages = int(parser.numSites)

        # check if all pages are downloaded
        i += 1
        if i > pages:
            break;
