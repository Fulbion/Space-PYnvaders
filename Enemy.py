import pygame
import random

from assets.constants import *

class Enemy:
    def __init__(self, x: float, y: float) -> None:
        self.__position: vec2 = vec2(x, y)
        self.__image = pygame.image.load(".\\assets\\images\\invader.png")
        self.__bulletImage = pygame.image.load(".\\assets\\images\\bullet.png")
        self.__bullets: list[vec2] = []
        self.__direction: int = 1
        self.__moveCooldown: int = 0
        self.hasMovedDown: bool = False
        self.alive: bool = True
        self.moveCooldown: int = int(BASE_ENEMY_COOLDOWN)

    def getPosition(self) -> vec2:
        return self.__position
    
    def getBullets(self) -> list[vec2]:
        return self.__bullets

    def die(self) -> None:
        self.alive = False

    def update(self, playerBullets: list[vec2]) -> bool:
        for bullet in self.__bullets:
            bullet.y += 16
            if bullet.y > HEIGHT:
                self.__bullets.remove(bullet)
        
        for pb in playerBullets:
            if self.__position.x <= pb.x <= self.__position.x + 30 and self.__position.y <= pb.y <= self.__position.y + 32:
                self.die()
                playerBullets.remove(pb)

        if random.randint(1, 4096) == 1:
            self.__bullets.append(vec2(self.__position.x + 14, self.__position.y))

        for bullet in self.__bullets:
            bullet.y += 1
            if bullet.y >= HEIGHT:
                self.__bullets.remove(bullet)

        self.__moveCooldown = clamp(self.__moveCooldown - 1, 0, 180)

        if self.__moveCooldown == 0:
            self.__moveCooldown = self.moveCooldown
            self.__position.x += self.__direction * 8
            if self.__position.x <= 0 or self.__position.x >= 800 - 32:
                return True
        return False

    def moveDown(self) -> None:
        self.__direction = -1 if self.__direction == 1 else 1
        self.__position.x += self.__direction * 8
        self.__position.y += 32

    def render(self, surface: pygame.Surface) -> None:
        for bullet in self.__bullets:
            surface.blit(self.__bulletImage, (bullet.x, bullet.y))

        surface.blit(self.__image, (self.__position.x, self.__position.y))