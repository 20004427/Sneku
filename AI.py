import pygame
import random
import Globals
import Pathfinding

class AI():
    def __init__(self, Obsticals):
        self.segments = []
        self.spriteslist = pygame.sprite.Group()
        #var for interation
        z = 0
        #loops until their are 15 segments for the AI
        #due to how i have generated the terrain, this method should be fine,
        #but if the terrain genertion is improved, then this method of creting the AI snake will have to be improved.
        while True:
            for i in range(15):
                x = (Globals.segment_width + Globals.segment_margin) * (15 + z) - (Globals.segment_width + Globals.segment_margin) * i
                y = (Globals.segment_height + Globals.segment_margin) * (10 + z)
                #If the x and y values are inside an object, then the object isn't added to the segments
                if any(i[0][0] <= x <= i[0][1] and i[1][0] <= y <= i[1][1] for i in Obsticals):
                    pass
                #if the x and y values are not inside the terrain, then adding the segment to the segments list
                else:
                    segment = Segment(x, y)
                    self.segments.append(segment)
                    self.spriteslist.add(segment)
            #if their are 15 segments, then the loop breaks
            if len(self.segments) >= 15:
                break
            #else, resetting the segments and sprite list
            for i in self.segments:
                self.spriteslist.remove(i)
            self.segments = []
            #adding one to the interation
            z += 1
        #initializing the path finding class
        self.Pathfinder = Pathfinding.Pathfinder(Obsticals)
        #setting up an array to hold the current path
        self.currentPath = []

    #function to move the snake along the path
    def move(self, end, Matrix):
        #if their isn't a current path
        if self.currentPath == []:
            #getting a path
            self.currentPath = self.Pathfinder.astar((self.segments[0].rect.x, self.segments[0].rect.y), end, self.segments)
        #setting the x and y coords to be the first x, y of the path
        x = self.currentPath[0][0]
        y = self.currentPath[0][1]
        #removing the first step of the path
        self.currentPath = self.currentPath[1:]

        # Insert new segment into the list
        segment = Segment(x, y)
        self.segments.insert(0, segment)
        self.spriteslist.add(segment)
        # Get rid of last segment of the snake
        # .pop() command removes last item in list
        old_segment = self.segments.pop()
        self.spriteslist.remove(old_segment)

    # used to add segments to the end of the snake
    def AddSegment(self):
        # getting the difference in x and y between the last 2 segments to determine where the new segment should be placed
        difx = self.segments[-1].rect.x - self.segments[-2].rect.x
        dify = self.segments[-1].rect.y - self.segments[-2].rect.y
        # if the diff x is greater than zero then the last segment is to the right of the second to last segment
        # Theirfore the new segment should be to the right of the last segment (the last segment is moving to the left)
        if difx > 0:
            x = self.segments[-1].rect.x + (Globals.segment_width + Globals.segment_margin)
            y = self.segments[-1].rect.y
        # if the diff x is smaller than zero then the second to last segment is to the right of the last segment
        # Theirfore the new segment should be to the left of the last segment as the last segment is moving to the right
        elif difx < 0:
            x = self.segments[-1].rect.x - (Globals.segment_width + Globals.segment_margin)
            y = self.segments[-1].rect.y
        # if the diff y is greater than zero then the last segment is below the second to last segment.
        # Theirfore the new segment will be below the last segment as the last segment is moving upwards
        elif dify > 0:
            x = self.segments[-1].rect.x
            y = self.segments[-1].rect.y + (Globals.segment_width + Globals.segment_margin)
        # if the diff y is less than zero then the last segment is above the second to last segment.
        # Theirfore the new segment will be above the last segment as the last segment is moving downwards
        else:
            x = self.segments[-1].rect.x
            y = self.segments[-1].rect.y - (Globals.segment_width + Globals.segment_margin)
        # creating a new segment from the x and y values
        segment = Segment(x, y)
        # adding the segment to the segments array and sprite list
        self.segments.append(segment)
        self.spriteslist.add(segment)

class Segment(pygame.sprite.Sprite):
    """ Class to represent one segment of a snake. """

    # Constructor
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([Globals.segment_width, Globals.segment_height])
        self.image.fill(Globals.WHITE)

        # Set top-left corner of the bounding rectangle to be the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y