import pygame
import json
file = '123.mp3'

while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

class MusicHandler(object):

    def __init__(self, musicLibJSON):
        with open(musicLibJSON) as jsonData:
            self.musicLib = json.load(jsonData)
        self.musicQueue = []
        pygame.init()
        pygame.mixer.init()

    def play(self, disc, track)
        musicFile = self.musicLib[disc][track]
        if pygame.mixer.get_busy():
            self.musicQueue.append(musicFile)
        else:
            pygame.mixer.music.load(musicFile)
            pygame.mixer.music.play()



