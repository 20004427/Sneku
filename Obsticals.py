import pygame
import random
import Globals

class Obsticals():
    def __init__(self):
        self.Objects = []
        self.Matrix = []
        self.spriteslist = pygame.sprite.Group()
        self.MaxObjects = Globals.MaxObjects

    #recursive function to built the map
    def CreateMap(self, Snake, x = 0, y = 0):
        #length, is the size of the obstical
        length = random.randrange(1, 5)
        #if the len of objects is greater/ = to max objects, or x is bigger than the game window width, or y is bigger than the game winow height
        if len(self.Objects) >= self.MaxObjects or x >= Globals.width or y >= Globals.height:
            #breaking the recursion
            return
        #if the obstical is in the snake or if the obstical is in the food segment
        if any(i.rect.x - length * (Globals.segment_width + Globals.segment_margin) <= x <= i.rect.x + length * (Globals.segment_width + Globals.segment_margin) and
               i.rect.y - length * (Globals.segment_height + Globals.segment_margin) <= y <= i.rect.y + length * (Globals.segment_height + Globals.segment_margin)
               for i in Snake.segments):
            #Recursively calling the function
            self.CreateMap(Snake,x + length * (Globals.segment_margin + Globals.segment_width), y + length * (Globals.segment_margin + Globals.segment_height))
            self.CreateMap(Snake,x - length * (Globals.segment_margin + Globals.segment_width),y - length * (Globals.segment_margin + Globals.segment_height))
            self.CreateMap(Snake,x, y + length * (Globals.segment_margin + Globals.segment_height))
            self.CreateMap(Snake,x + length * (Globals.segment_margin + Globals.segment_width),y)
            return
        if x in [z.rect.x for z in self.Objects] and y in [z.rect.y for z in
                                                           self.Objects] or x >= Globals.width or y >= Globals.height:
            self.CreateMap(Snake, x + length * (Globals.segment_margin + Globals.segment_width), y)
            self.CreateMap(Snake, x, y + length * (Globals.segment_margin + Globals.segment_height))
        #creating a random chance
        chance = random.randrange(100)
        #If the chance is greater or equal to 50
        if chance >= 50:
            self.Matrix.append([(x,x+length*(Globals.segment_margin+Globals.segment_width)),(y,y+length*(Globals.segment_height +Globals.segment_margin))])
            obj = Obj(x, y, length)
            self.Objects.append(obj)
            self.spriteslist.add(obj)
            #creating a wall vertically
            self.CreateMap(Snake, x + length * (Globals.segment_margin + Globals.segment_width), y)
            self.CreateMap(Snake, x, y + length * (Globals.segment_margin + Globals.segment_height))

    def Collisions(self, Snake):
        Collisions = pygame.sprite.spritecollide(Snake.segments[0], self.spriteslist, False)
        if Collisions:
            for i in self.Objects:
                self.spriteslist.remove(i)
            self.Objects = []
            self.Matrix = []
            return True


class Obj(pygame.sprite.Sprite):
    def __init__(self, x, y, length):
        # Call the parent's constructor
        super().__init__()
        # Set height, width
        self.image = pygame.Surface([length * (int(Globals.segment_margin + Globals.segment_width)) - Globals.segment_margin, length * (int(Globals.segment_margin + Globals.segment_height)) - Globals.segment_margin])
        self.image.fill(Globals.RED)

        # Set top-left corner of the bounding rectangle to be the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.length = length
