from code.Entity import Entity

class Food(Entity):

    def __init__(self,image,x,y,value):

        super().__init__(image,x,y)

        self.speed = 5
        self.value = value

    def move(self):

        self.rect.x += self.speed