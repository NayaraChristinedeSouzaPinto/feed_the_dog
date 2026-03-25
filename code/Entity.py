class Entity:

    def __init__(self,image,x,y):

        self.surf = image
        self.rect = self.surf.get_rect(topleft=(x,y))

    def move(self):
        pass