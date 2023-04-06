import Globals
import pygame

pygame.init()

class Snake():
    """ Class to represent one snake. """

    # Constructor
    def __init__(self):
        self.segments = []
        self.spriteslist = pygame.sprite.Group()
        #creating the initial snake
        for i in range(15):
            x = (Globals.segment_width + Globals.segment_margin) * 30 - (Globals.segment_width + Globals.segment_margin) * i
            y = (Globals.segment_height + Globals.segment_margin) * 2
            segment = Segment(x, y)
            self.segments.append(segment)
            self.spriteslist.add(segment)

    #moving the snake
    def move(self):
        # Figure out where new segment will be
        x = self.segments[0].rect.x + Globals.x_change
        y = self.segments[0].rect.y + Globals.y_change

        # Don't move off the screen
        # At the moment a potential move off the screen means nothing happens, but it should end the game
        if 0 <= x <= Globals.width - Globals.segment_width and 0 <= y <= Globals.height - Globals.segment_height:
            # Insert new segment into the list
            segment = Segment(x, y)
            self.segments.insert(0, segment)
            self.spriteslist.add(segment)
            # Get rid of last segment of the snake
            # .pop() command removes last item in list
            old_segment = self.segments.pop()
            self.spriteslist.remove(old_segment)
        #if the snake is going off screen
        else:
            #reseting the x and y change
            Globals.x_change = Globals.segment_width + Globals.segment_margin
            Globals.y_change = 0
            #changing scenes
            Globals.Scenes['GameOver'] = True
            Globals.Scenes['Game'] = False

    #used to add segments to the end of the snake
    def AddSegment(self):
        #getting the difference in x and y between the last 2 segments to determine where the new segment should be placed
        difx = self.segments[-1].rect.x - self.segments[-2].rect.x
        dify = self.segments[-1].rect.y - self.segments[-2].rect.y
        #if the diff x is greater than zero then the last segment is to the right of the second to last segment
        #Theirfore the new segment should be to the right of the last segment (the last segment is moving to the left)
        if difx > 0:
            x = self.segments[-1].rect.x + (Globals.segment_width + Globals.segment_margin)
            y = self.segments[-1].rect.y
        # if the diff x is smaller than zero then the second to last segment is to the right of the last segment
        # Theirfore the new segment should be to the left of the last segment as the last segment is moving to the right
        elif difx < 0:
            x = self.segments[-1].rect.x - (Globals.segment_width + Globals.segment_margin)
            y = self.segments[-1].rect.y
        #if the diff y is greater than zero then the last segment is below the second to last segment.
        #Theirfore the new segment will be below the last segment as the last segment is moving upwards
        elif dify > 0:
            x = self.segments[-1].rect.x
            y = self.segments[-1].rect.y + (Globals.segment_width + Globals.segment_margin)
        # if the diff y is less than zero then the last segment is above the second to last segment.
        # Theirfore the new segment will be above the last segment as the last segment is moving downwards
        else:
            x = self.segments[-1].rect.x
            y = self.segments[-1].rect.y - (Globals.segment_width + Globals.segment_margin)
        #creating a new segment from the x and y values
        segment = Segment(x, y)
        #adding the segment to the segments array and sprite list
        self.segments.append(segment)
        self.spriteslist.add(segment)

    #used to check collisions between the head of the snake and other sprites
    def checkCollision(self):
        #checking the collision between the snake head and the snake body without removing any objects
        CollisionSelf = pygame.sprite.spritecollide(self.segments[0], self.spriteslist, False)
        #If their is a Collision
        if CollisionSelf:
            #getting the position of the segment that the head of the snake collided with in the array of snake segments
            Index = self.segments.index(CollisionSelf[0])
            #If the index isn't that of the first 2 segments or the head (their will only every be one collision between the head and a segment at any given time)
            if Index > 2:
                #slicing the array based on the collision
                Globals.CurrentScore -= len(self.segments[Index:])
                #removing the sprites
                for i in self.segments[Index:]:
                    self.spriteslist.remove(i)
                    self.segments.remove(i)
            elif Index != 0:
                # resseting directions of the player and switching to the game over scene
                Globals.x_change = Globals.segment_width + Globals.segment_margin
                Globals.y_change = 0
                Globals.Scenes['GameOver'] = True
                Globals.Scenes['Game'] = False


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