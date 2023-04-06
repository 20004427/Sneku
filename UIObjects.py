import pygame
import Globals

#initializing the pygame font module !REQUIRED FOR FONT TO WORK!

pygame.font.init()

#Universal class for creating buttons
class Button():
    #Initiallizing the button
    def __init__(self, color, x, y, width, height, text='', textColour = Globals.WHITE, font = pygame.font.SysFont('comicsans', 60)):
        self.font = font
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.textColour = textColour

    #drawing the button to a screen, I reused this from a few mini python challenges i did over the summer break and am currently working on
    #which is why their are some unused variables and classes.
    def draw(self, win, background=None, outline=None):
        # Call this method to draw the button on the screen
        #if the outline is defined
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        #if the background is not defined
        if background == None:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        #if the backgound is defined (Note backgound should be an image)
        else:
            #Scaling the image
            image = pygame.transform.scale(background, (self.width, self.height))
            #turning the image into a rect
            rect = image.get_rect()
            #centering the image
            rect.center = (self.x+self.width/2, self.y+self.height/2)
            #displaying the image
            win.blit(image, rect)

        #if text has been defined
        if self.text != '':
            #setting up the font
            font = self.font
            #creating the text
            text = font.render(self.text, 1, self.textColour)
            #displaying the text to screen
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    #if a given x and y coord is over the button. This was intended for a mouse, but could also be used as an event trigger box in gain.
    #i.e. if a player moves inside a button
    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

#Universal Class For Text
class Text():
    def __init__(self, font, color, pos, surface, text):
        self.Font_Font = font
        self.Font_Color = color
        self.Font_Pos = pos
        self.Surface = surface
        self.Text = text

    #Draws text to display
    def Display(self):
        text = self.Font_Font.render(self.Text, 1, self.Font_Color)
        text_rect = text.get_rect(center = (self.Font_Pos))
        self.Surface.blit(text, text_rect)

class CheckBox():
    def __init__(self, pos, surface, scale, text, font, font_color):
        self.Pos = pos
        self.Scale = scale
        self.Surface = surface
        self.Sprite_Triggered = pygame.image.load("Assetts/UIObjects/Checkbox(Both).png")
        self.Sprite_Not_Triggered = pygame.image.load("Assetts/UIObjects/Checkbox(Background).png")
        self.Triggered = False
        self.Text = text
        self.Text_Font = font
        self.Text_Font_Color = font_color

    def Display(self):
        if self.Triggered:
            image = pygame.transform.scale(self.Sprite_Triggered, self.Scale)
            rect = image.get_rect()
            rect.center = (self.Pos[0] + self.Scale[0] / 2, self.Pos[1] + self.Scale[1] / 2)
            self.Surface.blit(image, rect)
        else:
            image = pygame.transform.scale(self.Sprite_Not_Triggered, self.Scale)
            rect = image.get_rect()
            rect.center = (self.Pos[0] + self.Scale[0] / 2, self.Pos[1] + self.Scale[1] / 2)
            self.Surface.blit(image, rect)
        if self.Text != '':
            text = self.Text_Font.render(self.Text, 1, self.Text_Font_Color)
            self.Surface.blit(text, (self.Pos[0] + (self.Scale[0] / 2 - text.get_width() / 2) - 200, self.Pos[1] + (self.Scale[1] / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        if pos[0] > self.Pos[0] and pos[0] < self.Pos[0] + self.Scale[0]:
            if pos[1] > self.Pos[1] and pos[1] < self.Pos[1] + self.Scale[1]:
                return True
        return False