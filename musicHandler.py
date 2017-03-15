import pygame
file = '123.mp3'

while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

class MusicHandler(object):

    def __init__(self, musicLib):
        self.musicLib = musicLib
        self.musicQueue = []
        pygame.init()
        pygame.mixer.init()

    def play(self, disc, track):
        if pygame.mixer.get_busy():
            pass # load the queue
        else:
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()

    def _getFile(self, disc, track):
        # get file from musicLib
        return '123.mp3'



