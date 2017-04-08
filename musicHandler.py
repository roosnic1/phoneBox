from pyomxplayer import OMXPlayer
import os.path

class song(object):
    def __init__(self, musicDir, disc, track):
        self.filePath = musicDir + '/' + str(disc) + '/' + str(track) + '.mp3'
        self.disc = disc
        self.track = track

    def getDiscTrack(self):
        return self.disc, self.track

    def getFile(self):
        return self.filePath

    def getString(self):
        disc = str(self.disc)
        track = str(self.track)
        if len(disc) == 1:
            disc = '0' + disc
        if len(track) == 1:
            track = '0' + track
        return disc + track

    #def __str__(self):
        #return '' +  self.disc + self.track



class MusicHandler(object):

    def __init__(self, musicDir, setDisplayCallback):
        self.musicQueue = []
        self.musicDir = musicDir
        self.currentSong = None
        self.setDisplayCallback = setDisplayCallback

    def play(self, disc, track):
        newSong = song(self.musicDir, disc, track)
        if not os.path.isfile(newSong.getFile()):
            return False, self.musicQueue[0].getString()
        self.musicQueue.append(newSong)
        if self.currentSong is None:
            self.currentSong = OMXPlayer(self.musicQueue[0].getFile(), self.nextSong, start_playback=True)
            self.setDisplayCallback(self.musicQueue[0].getString())
        return True, self.musicQueue[0].getString()

    def nextSong(self):
        if len(self.musicQueue) == 1:
            tmp = self.musicQueue[0].getDiscTrack()
            while not self.play(tmp[0], tmp[1] + 1)[0]:
                if tmp[0] >= 99:
                    print('Reach the end')
                    break
                else:
                    tmp = tmp[0] + 1, 0
        self.musicQueue.pop(0)
        OMXPlayer(self.musicQueue[0].getFile(), self.nextSong, start_playback=True)
        self.setDisplayCallback(self.musicQueue[0].getString())
