import pygame
from code.Entity import Entity

class Player(Entity):

    def __init__(self,image,x,y):

        super().__init__(image,x,y)
        self.speed = 5

    def move(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if keys[pygame.K_UP]:
            self.rect.y -= self.speed

        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > 800:
            self.rect.right = 800

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > 600:
            self.rect.bottom = 600