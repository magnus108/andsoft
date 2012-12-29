from __future__ import print_function

import sys
sys.path.append('/home/andrea/projects/cvs/3rdParty/m3u8')

import os
import urlparse
import m3u8
import time
import json

from datetime import date
from datetime import timedelta

import urlgrabber.progress

from asi import Utils
from asi import Config
from asi import Base

baseUrl = "http://www.rai.it/dl/portale/html/palinsesti/replaytv/static"
channels = {"1": "RaiUno", "2": "RaiDue", "3": "RaiTre", "31": "RaiCinque"}

# tablet and phone url contain an overlapping set of bitrates
# this function makes the union of the 2
def getFullUrl(tablet, phone):
    if tablet == "":
        return phone

    if phone == "":
        return tablet

    posOfFirstCommaT = tablet.find(",")
    posOfLastCommaT  = tablet.rfind(",")
    midTablet = tablet[posOfFirstCommaT + 1 : posOfLastCommaT]

    posOfFirstCommaP = phone.find(",")
    posOfLastCommaP  = phone.rfind(",")
    midPhone = phone[posOfFirstCommaP + 1 : posOfLastCommaP]

    tabletSizes = midTablet.split(",")
    phoneSizes  = midPhone.split(",")

    sizes = set()
    sizes.update(tabletSizes)
    sizes.update(phoneSizes)

    fullUrl = tablet[0 : posOfFirstCommaT]
    for s in sorted(sizes, key = int):
        fullUrl = fullUrl + "," + s
    fullUrl = fullUrl + tablet[posOfLastCommaT :]

    return fullUrl


def parseItem(grabber, channel, date, time, value):
    name = value["t"]
    desc = value["d"]
    secs = value["l"]

    minutes = 0
    if secs != "":
        minutes = int(secs) / 60

    h264 = value["h264"]
    tablet = value["urlTablet"]
    smartPhone = value["urlSmartPhone"]
    pid = value["i"]

    if h264 != "" or tablet != "" or smartPhone != "" :
        p = Program(grabber, channels[channel], date, time, pid, minutes, name, desc, h264, tablet, smartPhone)
        return p

    return None


def process(grabber, f, db):
    o = json.load(f)

    for k1, v1 in o.iteritems():
        if k1 == "now":
            continue
        if k1 == "defaultBannerVars":
            continue

        channel = k1

        for date, v2 in v1.iteritems():
            for time, value in v2.iteritems():
                p = parseItem(grabber, channel, date, time, value)

                if p != None:
                    if p.pid in db:
                        print("WARNING: duplicate pid {0}".format(p.pid))
                        #                        db[pid].display()
                        #                        p.display()

                    db[p.pid] = p


def download(db, grabber, downType):
    progress_obj = urlgrabber.progress.TextMeter()

    today = date.today()

    folder = Config.replayFolder

    for x in range(1, 8):
        day = today - timedelta(days = x)
        strDate = day.strftime("_%Y_%m_%d")

        for channel in channels.itervalues():
            filename = channel + strDate + ".html"
            url = baseUrl + "/" + filename
            localName = os.path.join(folder, filename)

            f = Utils.download(grabber, progress_obj, url, localName, downType, "utf-8")
            process(grabber, f, db)

    print()


class Program(Base.Base):
    def __init__(self, grabber, channel, date, hour, pid, minutes, title, desc, h264, tablet, smartPhone):
        super(Program, self).__init__()

        self.pid = pid
        self.title = title
        self.h264 = h264
        self.description = desc
        self.channel = channel
        self.ts = getFullUrl(tablet, smartPhone)
        self.datetime = time.strptime(date + " " + hour, "%Y-%m-%d %H:%M")

        self.grabber = grabber
        self.minutes = minutes

        self.m3 = None


    def display(self):
        width = urlgrabber.progress.terminal_width()

        print("=" * width)
        print("PID:", self.pid)
        print("Channel:", self.channel)
        print("Title:", self.title)
        print("Description:", self.description)
        print("Date:", time.strftime("%Y-%m-%d %H:%M", self.datetime))
        print("Length:", self.minutes, "minutes")
        print("Filename:", self.getFilename())
        print()
        print("h264:", self.h264)
        print("ts:  ", self.ts)

        m3 = self.getTabletPlaylist()

        Utils.displayM3U8(self.m3)


    def download(self, grabber, folder, format, bwidth):
        if not os.path.exists(folder):
            os.makedirs(folder)

        if format == "h264":
            self.downloadH264(grabber, folder)
        elif format == "ts":
            self.downloadTablet(grabber, folder, bwidth)
        elif format == None:
            self.downloadH264(grabber, folder)


    def downloadH264(self, grabber, folder):
        Utils.downloadH264(grabber, folder, self.pid, self.h264, self.getFilename())


    def getTabletPlaylist(self):
        if self.m3 == None:
            if self.ts != "":
                self.m3 = Utils.load_m3u8_from_url(self.grabber, self.ts)

        return self.m3


    # use RAI m3u8 url to get a "nice" filename
    # as opposed to only use the pid
    def getFilename(self):
        if self.ts == "":
            return self.pid

        fullName = os.path.split(os.path.split(urlparse.urlsplit(self.ts).path)[0])[1]
        tmp = fullName.split(",")[0]
        posOfDash = tmp.rfind("-")
        nice = tmp[0 : posOfDash]

        filename = self.pid + "-" + nice

        return filename


    def downloadTablet(self, grabber, folder, bwidth):
        m3 = self.getTabletPlaylist()
        Utils.downloadM3U8(grabber, m3, bwidth, folder, self.pid, self.getFilename())
