import random
from code.Entity import Entity

class Dog(Entity):

    def __init__(self,image,x,y):

        super().__init__(image,x,y)

        self.speed_x = random.randint(3,6)
        self.speed_y = random.randint(2,4)
        self.direction = random.choice([-1,1])

    def move(self):

        self.rect.x -= self.speed_x

        self.rect.y += self.speed_y * self.direction

        if self.rect.top <= 5 or self.rect.bottom >= 595:
            self.direction *= -1