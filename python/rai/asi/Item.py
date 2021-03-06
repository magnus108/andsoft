import os.path
import urllib.parse
import datetime

from html.parser import HTMLParser

from asi import Utils
from asi import Config
from asi import Base
from asi import RAIUrls

# <meta name="videourl" content="....." />

# <ASX VERSION="3.0"><ENTRY><REF HREF="http://wms1.rai.it/raiunocdn/raiuno/79221.wmv" /></ENTRY></ASX>

# [Reference]
# Ref1=http://wms1.rai.it/raiunocdn/raiuno/79221.wmv?MSWMExt=.asf
# Ref2=http://92.122.190.142:80/raiunocdn/raiuno/79221.wmv?MSWMExt=.asf

# this one needs videoPath
# http://www.rai.tv/dl/RaiTV/programmi/media/ContentItem-6278dcf9-0225-456c-b4cf-71978200400a.html
#
# here we can get away with videoUrl
# http://www.rai.tv/dl/RaiTV/programmi/media/ContentItem-b9812490-7243-4545-a5fc-843bf46ec3c9.html

# create a subclass and override the handler methods
class VideoHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)

        self.values = Utils.Obj()
        self.values.videoUrl = None
        self.values.videoUrlMP4 = None
        self.values.videoUrlH264 = None
        self.values.videoUrlM3U8 = None
        self.values.title = None
        self.values.program = None
        self.values.description = None
        self.values.videoPath = None
        self.values.type = None
        self.values.page = None
        self.values.date = None


    def handle_starttag(self, tag, attrs):
        if tag == "meta":
            val = self.extract(attrs, "videourl")
            if val:
                self.values.videoUrl = val

            val = self.extract(attrs, "videourl_mp4")
            if val:
                self.values.videoUrlMP4 = val

            val = self.extract(attrs, "videourl_h264")
            if val:
                self.values.videoUrlH264 = val

            val = self.extract(attrs, "videourl_m3u8")
            if val:
                self.values.videoUrlM3U8 = val

            val = self.extract(attrs, "title")
            if val:
                self.values.title = val

            val = self.extract(attrs, "programmaTV")
            if val:
                self.values.program = val

            val = self.extract(attrs, "description")
            if val:
                self.values.description = val

            val = self.extract(attrs, "tipo")
            if val:
                self.values.type = val

            val = self.extract(attrs, "itemDate")
            if val:
                self.values.date = val

            val = self.extract(attrs, "idPageProgramma")
            if val:
                self.values.page = RAIUrls.base + RAIUrls.getWebFromID(val)

        elif tag == "param":
            if len(attrs) > 0:
                if attrs[0][0] == "value":
                    path = attrs[0][1]
                    if path.find("videoPath") == 0:
                        firstEqual = path.find("=")
                        firstComma = path.find(",")
                        self.values.videoPath = path[firstEqual + 1: firstComma]


    def extract(self, attrs, name):
        if len(attrs) > 1:
            if attrs[0][0] == "name" and attrs[0][1] == name:
                if attrs[1][0] == "content":
                    return attrs[1][1]
        return None


class Demand(Base.Base):
    def __init__(self, grabber, url, downType, pid):
        super(Demand, self).__init__()

        self.grabber = grabber

        parts = urllib.parse.urlparse(url)
        if not parts.scheme:
            url = RAIUrls.getItemUrl(url)

        self.url = url
        self.pid = pid

        folder = Config.itemFolder
        localFilename = os.path.join(folder, Utils.httpFilename(self.url))

        f = Utils.download(grabber, None, self.url, localFilename, downType, "utf-8")

        parser = VideoHTMLParser()
        parser.feed(f.read())

        self.values = parser.values

        self.channel = "item"
        self.title = self.values.title
        self.ts = self.values.videoUrlM3U8

        Utils.addH264Url(self.h264, 0, self.values.videoUrlH264)

        if self.values.date:
            self.datetime = datetime.datetime.strptime(self.values.date, "%d/%m/%Y")

        self.mms = None

        if self.values.type and self.values.type != "Video":
            # this is a case of a Photogallery
            self.url = None
            self.filename = None
            return

        if not self.values.videoUrl:
            self.values.videoUrl = self.values.videoPath

        #sometimes we get .mp4 which does not work
        self.values.videoUrl = self.values.videoUrl.replace("relinkerServlet.mp4", "relinkerServlet.htm")

        #make a nice filename
        self.filename = Utils.makeFilename(self.title)

        self.mms = self.values.videoUrl


    def display(self, width):
        super(Demand, self).display(width)

        print("Type:", self.values.type)
        print("Program:", self.values.program)
        print("Page:", self.values.page)
        print("URL:", self.url)
        print("videourl:", self.values.videoUrl)
        print()


    def follow(self, db, downType):
        raise Exception("Follow selection must terminate here.")
