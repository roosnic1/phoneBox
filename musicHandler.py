import pygame.event
import pygame.mixer
import json
import threading
import time

ENDEVENT=42

class MusicHandler(object):

    def __init__(self, musicLibJSON):
        with open(musicLibJSON) as jsonData:
            self.musicLib = json.load(jsonData)
        self.musicQueue = []
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(ENDEVENT)
        t = threading.Thread(target=self._songend_bubble, args=(self,))
        t.daemon = True
        t.start()

    def _songend_bubble(s,self):
        while 1:
            event = pygame.event.get(ENDEVENT)
            if event:
                print('received end event')
                if(len(self.musicQueue) > 0):
                    pygame.mixer.music.load(self.musicQueue.pop(0))
                    pygame.mixer.music.play()
            else:
                time.sleep(0.1)

    def play(self, disc, track):
        musicFile = self.musicLib[disc][track]
        if pygame.mixer.music.get_busy():
            print('player busy')
            self.musicQueue.append(musicFile)
        else:
            print('player not busy')
            pygame.mixer.music.load(musicFile)
            pygame.mixer.music.play()



