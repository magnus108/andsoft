import mpd
import socket


class MPDAlive(object):

    def __init__(self, host, port, timeout, ps3):
        self.host = host
        self.port = port
        self.client = mpd.MPDClient()
        self.client.timeout = timeout
        self.oldvol = 0
        self.ps3 = ps3
        self.stored = None

        # do not synchronize now
        # /dev/hidra0 does not seem to be ready


    def connect(self):
        self.client.connect(self.host, self.port)


    def mpc(self):
        try:
            self.client.ping()
        except mpd.ConnectionError:
            self.connect()

        return self.client


    def get_volume(self):
        mpc = self.client
        s = mpc.status()
        vol = int(s["volume"])
        return vol


    def last(self):
        mpc = self.client
        s = mpc.status()
        if "playlistlength" in s:
            song = int(s["playlistlength"])
            mpc.play(song - 1)


    def volume(self, change):
        mpc = self.client
        vol = self.get_volume()
        newvol = min(100, max(0, vol + change))
        mpc.setvol(newvol)


    def mute(self):
        mpc = self.client
        newvol = self.oldvol
        self.oldvol = self.get_volume()
        mpc.setvol(newvol)


    def get_song(self):
        mpc = self.client
        st = mpc.status()
        if "song" in st:
            song = int(st["song"])
            return song


    def store(self):
        song = self.get_song()
        if not song is None:
            self.stored = song


    def swap(self):
        new_song = self.stored
        self.store()
        if not new_song is None:
            mpc = self.client
            mpc.play(new_song)


    def execute(self, cmd):
        try:
            mpc = self.mpc()

            if cmd == "PLAY":
                mpc.play()
            elif cmd == "STOP":
                mpc.stop()
            elif cmd == "PREV":
                mpc.previous()
            elif cmd == "NEXT":
                mpc.next()
            elif cmd == "VOLUP":
                self.volume(2)
            elif cmd == "VOLDOWN":
                self.volume(-2)
            elif cmd == "RESET":
                mpc.play(0)
            elif cmd == "LAST":
                self.last()
            elif cmd == "MUTE":
                self.mute()
            elif cmd == "SWAP":
                self.swap()

            self.synchronize()

        except socket.timeout as e:
            # socket is not a disaster
            # maybe it works next time
            print("Warning: got {0}".format(e))


    def synchronize(self):
        song = self.get_song()
        if song is None:
            self.ps3.set_flash()
        else:
            self.ps3.set_leds(1 + song) # as they start from 0
