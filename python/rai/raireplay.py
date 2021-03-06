#! /usr/bin/python

import sys
import platform
import codecs
import argparse

import Driver

def main():

    parser = argparse.ArgumentParser(description = "Rai Replay", fromfile_prefix_chars = "@")

    parser.add_argument("--download", action = "store", default = "update", choices = ["always", "update", "never", "shm"],
                        help = "Default is update")
    parser.add_argument("--format", action = "store", choices = ["h264", "ts", "tsmp4", "mms"])
    parser.add_argument("--bwidth", action = "store", default = "high")
    parser.add_argument("--ip", action = "store_true", default = False)
    parser.add_argument("--tor", action = "store", help = "coutry code for tor exit nodes")
    parser.add_argument("--tor-pass", action = "store")
    parser.add_argument("--tor-only-metadata", action = "store_true", default = False, help = "do not use tor for actual download")
    parser.add_argument("--proxy", action = "store")
    parser.add_argument("--overwrite", action = "store_true", default = False, help = "overwrite program")
    parser.add_argument("--location", action = "store", help = "path where to download programs")
    parser.add_argument("--ts-tries", action = "store", default = 20)

    parser.add_argument("--page",   action = "store", help = "RAI On Demand Page")
    parser.add_argument("--replay", action = "store_true", default = False, help = "RAI Replay")
    parser.add_argument("--ondemand", action = "store_true", default = False, help = "RAI On Demand List")
    parser.add_argument("--tg", action = "store_true", default = False, help = "Telegiornali RAI")
    parser.add_argument("--junior", action = "store_true", default = False, help = "RAI Junior")
    parser.add_argument("--search", action = "store", help = "Search RAI TV")

    parser.add_argument("--mediaset", action = "store_true", default = False, help = "Video Mediaset")
    parser.add_argument("--tg5", action = "store_true", default = False, help = "TG Mediaset")
    parser.add_argument("--pluzz", action = "store_true", default = False, help = "Pluzz France Television")
    parser.add_argument("--m6", action = "store_true", default = False, help = "M6")
    parser.add_argument("--tf1", action = "store_true", default = False, help = "MY TF1")
    parser.add_argument("--item", action = "store", help = "RAI On Demand Item")

    parser.add_argument("--m3u8", action = "store", help = "Playlist")

    parser.add_argument("--date", action = "store", help = "Filter by date YYYY-MM-DD")
    parser.add_argument("--channel", action = "store", help = "Filter by channel")
    parser.add_argument("--follow", action = "append")

    parser.add_argument("--nolist", action = "store_true", default = False)
    parser.add_argument("--get", action = "store_true", default = False, help = "download program")
    parser.add_argument("--info", action = "store_true", default = False, help = "print IP info")
    parser.add_argument("--re", action = "store_true", default = False, help = "filters are RegExp")

    parser.add_argument("pid", nargs = "*")



    args = parser.parse_args()

    Driver.process(args)

    print()

if platform.system() == "Windows":
    # in windows there are issues when printing utf-8 to the console
    # it does not work out of the box
    # no clear solution comes out of google
    # this "choice" seems to work
    sys.stdout = codecs.getwriter("cp850")(sys.stdout.buffer, "ignore")
elif not sys.stdout.encoding:
    # is this required??? seems a bit of pythonic nonsense
    # all RAI html is encoded in "utf-8" (decoded as we read)
    #
    # and it seems that redirecting the output (e.g. "| less") requires am explicit encoding
    # done here
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "ignore")

if __name__ == '__main__':
    main()
