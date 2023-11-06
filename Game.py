import pygame

from assets.constants import *
from Player import *
from Enemy import *
from Shield import *

class Game:
    def __init__(self) -> None:
        self.__running: bool = True

        self.__window: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space PYnvarders")
        self.__clock = pygame.time.Clock()

        self.restart()
    
    def restart(self) -> None:
        self.__player: Player = Player()
        self.__enemies: list[list[Enemy]] = [
            [Enemy(50, 50), Enemy(50 * 2, 50), Enemy(50 * 3, 50), Enemy(50 * 4, 50), Enemy(50 * 5, 50), Enemy(50 * 6, 50), Enemy(50 * 7, 50), Enemy(50 * 8, 50), Enemy(50 * 9, 50), Enemy(50 * 10, 50), Enemy(50 * 11, 50), Enemy(50 * 12, 50), Enemy(50 * 13, 50), Enemy(50 * 14, 50)],
            [Enemy(50, 50 * 2), Enemy(50 * 2, 50 * 2), Enemy(50 * 3, 50 * 2), Enemy(50 * 4, 50 * 2), Enemy(50 * 5, 50 * 2), Enemy(50 * 6, 50 * 2), Enemy(50 * 7, 50 * 2), Enemy(50 * 8, 50 * 2), Enemy(50 * 9, 50 * 2), Enemy(50 * 10, 50 * 2), Enemy(50 * 11, 50 * 2), Enemy(50 * 12, 50 * 2), Enemy(50 * 13, 50 * 2), Enemy(50 * 14, 50 * 2)],
            [Enemy(50, 50 * 3), Enemy(50 * 2, 50 * 3), Enemy(50 * 3, 50 * 3), Enemy(50 * 4, 50 * 3), Enemy(50 * 5, 50 * 3), Enemy(50 * 6, 50 * 3), Enemy(50 * 7, 50 * 3), Enemy(50 * 8, 50 * 3), Enemy(50 * 9, 50 * 3), Enemy(50 * 10, 50 * 3), Enemy(50 * 11, 50 * 3), Enemy(50 * 12, 50 * 3), Enemy(50 * 13, 50 * 3), Enemy(50 * 14, 50 * 3)],
            [Enemy(50, 50 * 4), Enemy(50 * 2, 50 * 4), Enemy(50 * 3, 50 * 4), Enemy(50 * 4, 50 * 4), Enemy(50 * 5, 50 * 4), Enemy(50 * 6, 50 * 4), Enemy(50 * 7, 50 * 4), Enemy(50 * 8, 50 * 4), Enemy(50 * 9, 50 * 4), Enemy(50 * 10, 50 * 4), Enemy(50 * 11, 50 * 4), Enemy(50 * 12, 50 * 4), Enemy(50 * 13, 50 * 4), Enemy(50 * 14, 50 * 4)],
            [Enemy(50, 50 * 5), Enemy(50 * 2, 50 * 5), Enemy(50 * 3, 50 * 5), Enemy(50 * 4, 50 * 5), Enemy(50 * 5, 50 * 5), Enemy(50 * 6, 50 * 5), Enemy(50 * 7, 50 * 5), Enemy(50 * 8, 50 * 5), Enemy(50 * 9, 50 * 5), Enemy(50 * 10, 50 * 5), Enemy(50 * 11, 50 * 5), Enemy(50 * 12, 50 * 5), Enemy(50 * 13, 50 * 5), Enemy(50 * 14, 50 * 5)],
        ]

        self.__shields: list[Shield] = [
            Shield(50, 400), Shield(50+32, 400), Shield(50+64, 400), Shield(250, 400), Shield(250+32, 400), Shield(250+64, 400),
            Shield(450, 400), Shield(450+32, 400), Shield(450+64, 400), Shield(650, 400), Shield(650+32, 400), Shield(650+64, 400),
        ]

    def isRunning(self) -> bool:
        return self.__running

    def handleEvents(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False

    def update(self) -> None:
        self.__clock.tick(60)
        self.handleEvents()

        cleared: int = 0
        for line in self.__enemies:
            if not line or len(line) == 0:
                cleared += 1
        
        if cleared == 5:
            self.restart()
            for i in range(len(self.__enemies)):
                for enemy in self.__enemies[i]:
                    enemy.moveCooldown = clamp(enemy.moveCooldown - 10, 1, 60)

        flagToMoveDown: bool = False
        for i in range(len(self.__enemies)):
            for enemy in self.__enemies[i]:
                if enemy.alive:
                    enemy.hasMovedDown = False
                    if enemy.update(self.__player.getBullets()) or flagToMoveDown:
                        enemy.moveDown()
                        enemy.hasMovedDown = True
                        flagToMoveDown = True
                    if enemy.getPosition().y >= 500:
                        self.restart()

        for i in range(len(self.__enemies)):
            for enemy in self.__enemies[i]:
                if not enemy.hasMovedDown and flagToMoveDown:
                    enemy.moveDown()
                    enemy.hasMovedDown = True
                    flagToMoveDown = True
                if enemy.getPosition().y >= 500:
                    self.restart()
        
        if not self.__player.alive:
            self.restart()

        enemyBullets: list[vec2] = []
        for i in range(len(self.__enemies)):
            for enemy in self.__enemies[i]:
                for bullet in enemy.getBullets():
                    enemyBullets.append(bullet)

        for shield in self.__shields:
            shield.update(self.__player.getBullets(), enemyBullets)
            if shield.getHealth() <= 0:
                self.__shields.remove(shield)

        self.__player.update(enemyBullets)
    
    def render(self) -> None:
        self.__window.fill("black")
        for i in range(len(self.__enemies)):
            for enemy in self.__enemies[i]:
                if enemy.alive:
                    enemy.render(self.__window)
                else:
                    self.__enemies[i].remove(enemy)
        self.__player.render(self.__window)
        for shield in self.__shields:
            shield.render(self.__window)
        pygame.display.flip()

    def run(self) -> None:
        while self.isRunning():
            self.update()
            self.render()