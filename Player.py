import pygame

from assets.constants import *

class Player:
    def __init__(self) -> None:
        self.__position: vec2 = vec2(WIDTH // 2, 550)
        self.__image = pygame.image.load(".\\assets\\images\\spaceship.png")
        self.__bulletImage = pygame.image.load(".\\assets\\images\\bullet.png")
        self.__bullets: list[vec2] = []
        self.alive: bool = True
        self.__reloadTimer: int = 0

    def getBullets(self) -> list[vec2]:
        return self.__bullets

    def update(self, eb: list[vec2]) -> None:
        velocity = 0

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            velocity += 8

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            velocity -= 8
            
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if not self.__bullets:
                self.__bullets.append(vec2(self.__position.x + 14, self.__position.y))

        for bullet in self.__bullets:
            bullet.y -= 16
            if bullet.y < 0:
                self.__bullets.remove(bullet)

        for bullet in eb:
            if self.__position.x <= bullet.x <= self.__position.x + 30 and self.__position.y <= bullet.y <= self.__position.y + 32:
                self.alive = False
                eb.remove(bullet)

        self.__position.x = clamp(self.__position.x + velocity, min=0, max=WIDTH-32)

    def render(self, surface: pygame.Surface) -> None:
        for bullet in self.__bullets:
            surface.blit(self.__bulletImage, (bullet.x, bullet.y))

        surface.blit(self.__image, (self.__position.x, self.__position.y))