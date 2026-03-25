class Background:

    def __init__(self,image,y):

        self.image = image
        self.y = y
        self.speed = 0.5

    def move(self):

        self.y += self.speed

        if self.y >= 600:
            self.y = -600