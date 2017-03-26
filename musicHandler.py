import json
import musicplayer

class Song:
    def __init__(self, fn):
        self.url = fn
        self.f = open(fn)
    # `__eq__` is used for the peek stream management
    def __eq__(self, other):
        return self.url == other.url
    # this is used by the player as the data interface
    def readPacket(self, bufSize):
        return self.f.read(bufSize)
    def seekRaw(self, offset, whence):
        r = self.f.seek(offset, whence)
        return self.f.tell()


class MusicHandler(object):

    def __init__(self, musicLibJSON, setDisplayCallback):
        with open(musicLibJSON) as jsonData:
            self.musicLib = json.load(jsonData)
        self.musicQueue = []
        # Create our Music Player.
        self.player = musicplayer.createPlayer()
        self.player.outSamplerate = 96000  # support high quality :)
        self.player.queue = self.songs()
        self.queuePosition = 0
        self.setDisplayCallback = setDisplayCallback

    def play(self, disc, track):
        self.musicQueue.append((self.musicLib[disc][track], disc + track))
        self.player.playing = True

    def songs(self):
        while True:
            currentsong = self.musicQueue[self.queuePosition]
            self.setDisplayCallback(currentsong[1])
            yield Song(currentsong[0])
            self.queuePosition += 1
            if self.queuePosition >= len(self.musicQueue):
                self.queuePosition = 0
