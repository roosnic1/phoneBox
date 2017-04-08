from pyomxplayer import OMXPlayer
import os.path

class song(object):
    def __init__(self, filePath, disc, track):
        self.filePath = filePath
        self.disc = disc
        self.track = track

    def getDiscTrack(self):
        return int(self.disc), int(self.track)

    def getFile(self):
        return self.filePath

    def getString(self):
        return '' +  self.disc + self.track

    def __str__(self):
        return '' +  self.disc + self.track



class MusicHandler(object):

    def __init__(self, musicDir, setDisplayCallback):
        self.musicQueue = []
        self.musicDir = musicDir
        self.currentSong = None
        self.setDisplayCallback = setDisplayCallback

    def play(self, disc, track):
        songfile = self.musicDir + '/' + disc + '/' + track + '.mp3'
        if not os.path.isfile(songfile):
            return False, self.musicQueue[0].getString()
        self.musicQueue.append(song(songfile, disc, track))
        if self.currentSong is None:
            self.currentSong = OMXPlayer(self.musicQueue[0].getFile(), self.nextSong, start_playback=True)
            self.setDisplayCallback(self.musicQueue[0].getString())
        return True, self.musicQueue[0].getString()

    def nextSong(self):
        if len(self.musicQueue) == 1:
            tmp = self.musicQueue[0].getDiscTrack()
            while not self.play(str(tmp[0]), str(tmp[1] + 1))[0]:
                if tmp[0] >= 99:
                    tmp = 0,0
                else:
                    tmp = tmp[0] + 1, 0
        self.musicQueue.pop(0)
        OMXPlayer(self.musicQueue[0].getFile(), self.nextSong, start_playback=True)
        self.setDisplayCallback(self.musicQueue[0].getString())
