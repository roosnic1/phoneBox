from pyomxplayer import OMXPlayer
import os.path


class MusicHandler(object):

    def __init__(self, musicDir, setDisplayCallback):
        self.musicQueue = []
        self.musicDir = musicDir
        self.currentSong = None
        self.setDisplayCallback = setDisplayCallback

    def play(self, disc, track):
        songfile = self.musicDir + '/' + disc + '/' + track + '.mp3'
        if not os.path.isfile(songfile):
            return False, self.musicQueue[0][1]
        self.musicQueue.append((songfile, "" + disc + track))
        if self.currentSong is None:
            self.currentSong = OMXPlayer(self.musicQueue[0][0], self.nextSong, start_playback=True)
        return True, self.musicQueue[0][1]

    def nextSong(self):
        if len(self.musicQueue) > 0:
            self.musicQueue.pop(0)
            OMXPlayer(self.musicQueue[0][0], self.nextSong, start_playback=True)
        else:
            print('No more Songs to play')
