import pygame


TICKS_TO_UPDATE = 8
class Path:
    def __init__(self, color):
        self.path = []
        self.other_paths = []
        self.color = color
        self.ticks_to_update = TICKS_TO_UPDATE

    def draw(self, window):
        for p in self.other_paths:
            p.draw(window)

        for p in self.path:
            pygame.draw.circle(window, self.color, p, 1)
