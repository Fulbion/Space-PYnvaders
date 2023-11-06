import pygame

from assets.constants import *

class Shield:
    def __init__(self, x: float, y: float) -> None:
        self.__position: vec2 = vec2(x, y)
        self.__health: int = 4
        self.__image = pygame.image.load(f".\\assets\\images\\shield{self.__health}.png")

    def getHealth(self) -> int:
        return self.__health

    def update(self, pb: list[vec2], eb: list[vec2]) -> None:
        for bullet in pb:
            if self.__position.x <= bullet.x <= self.__position.x + 32 and self.__position.y <= bullet.y <= self.__position.y + 32:
                self.__health -= 1
                if self.__health > 0:
                    self.__image = pygame.image.load(f".\\assets\\images\\shield{self.__health}.png")
                pb.remove(bullet)
                
        for bullet in eb:
            if self.__position.x <= bullet.x <= self.__position.x + 32 and self.__position.y <= bullet.y <= self.__position.y + 32:
                self.__health -= 1
                if self.__health > 0:
                    self.__image = pygame.image.load(f".\\assets\\images\\shield{self.__health}.png")
                eb.remove(bullet)

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.__image, (self.__position.x, self.__position.y))