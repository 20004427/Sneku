import pygame
import random
import Globals

class Food():
    def __init__(self):
        #setting up a food array
        self.Food = []
        self.spriteslist = pygame.sprite.Group()

    #function to replenish the food, this is a recursive function
    def replenish(self, Obsticals):
        #if the current number of food sprites is equal to the max, then the recursion is broken
        if len(self.Food) == Globals.InitialFoodNo:
            return
        while True:
            #getting a random x and y coordinate
            x = random.randrange(0, Globals.width, Globals.segment_width + Globals.segment_margin)
            y = random.randrange(0, Globals.height, Globals.segment_height + Globals.segment_margin)
            #if the food array is empty or the current x and y coordinates are not already in the food array then the loop is broken
            #else the loop continues until a valid x and y coordinate is found
            if self.Food == [] or all(i.rect.x != x and i.rect.y != y for i in self.Food):
                #if the food is not ontop of an obstical object or within 2 segment of a wall.
                #This means that the food will always be possible to get
                #it needs to be 2 segments as the AI pathing is still not that great, and it is possible for the snake to get stuck
                if any(i[0][0] - 2 * (Globals.segment_width + Globals.segment_margin) <= x <= i[0][1] + 2 * (Globals.segment_width + Globals.segment_margin)
                       and i[1][0] - 2 * (Globals.segment_height + Globals.segment_margin) <= y <= i[1][1] + 2 * (Globals.segment_height + Globals.segment_margin)for i in Obsticals.Matrix):
                    continue
                else:
                    break
        #creating a new food object
        food_item = Food_item(x, y)
        #adding the food item to the food array and sprites
        self.Food.append(food_item)
        self.spriteslist.add(food_item)
        #recursion
        self.replenish(Obsticals)

class Food_item(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()
        # Set height, width
        self.image = pygame.Surface([Globals.segment_width, Globals.segment_height])
        self.image.fill(Globals.GREEN)

        # Set top-left corner of the bounding rectangle to be the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

