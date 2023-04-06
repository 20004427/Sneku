"""
 Snake Game template, using classes.
 
 Derived from:
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
"""

# Imports
import pygame
import string
import AI
import Food
import Globals
import Obsticals
import ReadScores
import Snake
import UIObjects


###This script is the heart of the program###
#It is used to switch between scenes and instantiate clases from other scripts.
#All modules in this program link back to this script#
#This is quite a long script, but I didn't want to create a new file for each scene.

#Main Menu Scene
class MainMenu():
    #Initializing the scene
    def __init__(self):
        #UI objects
        self.Font = pygame.font.SysFont('comicsans', 50)
        self.TitleTxt = UIObjects.Text(self.Font, Globals.GREEN, [Globals.Screen_Width/2 , 60], screen, 'Snake')
        self.ButtonPlay = UIObjects.Button(Globals.BLACK, Globals.Screen_Width/2 - 80, 160, 150, 65, 'Play')
        self.ButtonScores = UIObjects.Button(Globals.BLACK, Globals.Screen_Width/2 - 80, 240, 150, 65, 'HighScores', font = pygame.font.SysFont('comicsans', 35))
        self.ButtonQuit = UIObjects.Button(Globals.BLACK, Globals.Screen_Width/2 - 80, 320, 150, 65, 'Quit')

    #Drawing the UI to screen
    def draw(self):
        self.TitleTxt.Display()
        self.ButtonPlay.draw(screen, outline = Globals.GREEN)
        self.ButtonScores.draw(screen, outline = Globals.GREEN)
        self.ButtonQuit.draw(screen, outline = Globals.GREEN)

    #checking the input from the user
    def CheckInput(self):
        #getting the mouse x and y coords
        Mouse_x, Mouse_y = pygame.mouse.get_pos()
        #if the user has pressed something
        for event in pygame.event.get():
            #if the user closes the window
            if event.type == pygame.QUIT:
                Globals.done = True
                break
            #if the user presses a key
            if event.type == pygame.KEYDOWN:
                # if the key is escape then the game quits
                if event.key == pygame.K_ESCAPE:
                    Globals.done = True
                    Globals.Scenes['MainMenu'] = False
                    break
            #if the mouse is over the quit button and the user presses the mouse button
            if self.ButtonQuit.isOver((Mouse_x, Mouse_y)) and event.type == pygame.MOUSEBUTTONUP:
                #quiting the game by changing the main loop and Main menu bool statements to be false
                Globals.done = True
                Globals.Scenes['MainMenu'] = False
                Globals.Scenes['GameOver'] = False
            #if the mouse is over the play button and the user presses the mouse button
            if self.ButtonPlay.isOver((Mouse_x, Mouse_y)) and event.type == pygame.MOUSEBUTTONUP:
                #setting the mainmenu scene to be false and game to be true
                Globals.Scenes['MainMenu'] = False
                Globals.Scenes['Game'] = True
            #If the mouse is over the scores button and the user presses the mouse button
            if self.ButtonScores.isOver((Mouse_x, Mouse_y)) and event.type == pygame.MOUSEBUTTONUP:
                screen.fill(Globals.BLACK)
                Globals.Scenes['HighScores'] = True
                Globals.Scenes['MainMenu'] = False

#Game Scene
class GameScene():
    #Initializing the scene
    def __init__(self):
        #Creating an initial snake
        self.snake = Snake.Snake()
        #Creating the AI
        self.AI = None
        #Initializing the food (this doesn't create the food)
        self.Food = Food.Food()
        #Creating font
        self.Font = pygame.font.SysFont('comicsans', 40)
        # Creating the map based on the location of the snake and food
        self.Map = Obsticals.Obsticals()
        # whilst the map has less objects than the max number of objects
        while len(self.Map.Objects) <= int(Globals.MaxObjects / 2):
            # creating the map
            self.Map.CreateMap(self.snake)
        # Initializing the Game AI
        self.AI = AI.AI(self.Map.Matrix)
        # Creating the Matrix for the AI pathfinder
        self.AI.Pathfinder.CreateMatrix(self.Map)
        # Creating initial food for the map creation
        self.replenishFood()

    #drawing the scene to the display
    def draw(self):
        # -- Draw everything
        # Clear screen
        screen.fill(Globals.BLACK)
        #drawing the snake to screen
        self.snake.spriteslist.draw(screen)
        #drawing the food to screen
        self.Food.spriteslist.draw(screen)
        #drawing the obsticals to screen
        self.Map.spriteslist.draw(screen)
        #drawing the AI to screen
        self.AI.spriteslist.draw(screen)
        #updating the scores
        Score = 'Score: {}'.format(Globals.CurrentScore)
        ScoreAI = 'AI Score: {}'.format(Globals.AIScore)
        ScoreTxt = UIObjects.Text(self.Font, Globals.WHITE, [Globals.width - len(Score) * 10, Globals.height + 25], screen, Score)
        ScoreTxtAI = UIObjects.Text(self.Font, Globals.WHITE, [len(Score) * 10, Globals.height + 25], screen, ScoreAI)
        #displaying the score to the screen
        ScoreTxt.Display()
        ScoreTxtAI.Display()
        # creating a divider between the game window and the bottom section for the score and other ui objects
        pygame.draw.line(screen, Globals.RED, (0, Globals.height), (Globals.width, Globals.height))
        # Flip screen
        pygame.display.flip()

    #cheking the input from the user
    def CheckInput(self):
        #if the user pressed something
        for event in pygame.event.get():
            #if the user closes the window
            if event.type == pygame.QUIT:
                Globals.done = True
                Globals.Scenes['Game'] = False
                break

            # Set the direction based on the key pressed
            # We want the speed to be enough that we move a full
            # segment, plus the margin.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Globals.x_change = (Globals.segment_width + Globals.segment_margin) * -1
                    Globals.y_change = 0
                if event.key == pygame.K_RIGHT:
                    Globals.x_change = (Globals.segment_width + Globals.segment_margin)
                    Globals.y_change = 0
                if event.key == pygame.K_UP:
                    Globals.x_change = 0
                    Globals.y_change = (Globals.segment_height + Globals.segment_margin) * -1
                if event.key == pygame.K_DOWN:
                    Globals.x_change = 0
                    Globals.y_change = (Globals.segment_height + Globals.segment_margin)
                #if the escape key is pressed
                if event.key == pygame.K_ESCAPE:
                    #settng the Game loop to be False and the main menu loop to be true
                    Globals.Scenes['MainMenu'] = True
                    Globals.Scenes['Game'] = False
                    #resetting the game to default values
                    screen.fill(Globals.BLACK)
                    Globals.x_change = Globals.segment_width + Globals.segment_margin
                    Globals.y_change = 0
        # move snake one step
        self.snake.move()
        #move the AI one step
        #The AI movement function requires a end point (the position of a food object), and the pathfinding matrix.
        self.AI.move((self.Food.Food[-1].rect.x, self.Food.Food[-1].rect.y), self.AI.Pathfinder.Matrix)
        #checking snake collisions
        self.snake.checkCollision()
        #if the snake has only two segments, then the game ends.
        if len(self.snake.segments) <= 2 or self.Map.Collisions(self.snake):
            Globals.x_change = Globals.segment_width + Globals.segment_margin
            Globals.y_change = 0
            Globals.Scenes['GameOver'] = True
            Globals.Scenes['Game'] = False

    #detecting collisions
    def CollisionDetection(self):
        #checking for collision between the head of the snake and a food sprite
        CollisionPlayer = pygame.sprite.spritecollide(self.snake.segments[0], self.Food.spriteslist, True)
        #checking for collision between the head of the AI and a food sprite
        CollisionAI = pygame.sprite.spritecollide(self.AI.segments[0], self.Food.spriteslist, True)
        #Checking for collision between the AI and the Player snake
        CollisionAIPlayer = pygame.sprite.spritecollide(self.AI.segments[0], self.snake.spriteslist, False)
        #Checking for a collision between the Player and AI
        CollisionPlayerAI = pygame.sprite.spritecollide(self.snake.segments[0], self.AI.spriteslist, False)
        #if the Collisions array is not empty
        if CollisionPlayer:
            #removing the collided food from the food array
            self.Food.Food.remove(CollisionPlayer[0])
            #adding one to the score
            Globals.CurrentScore += 1
            #adding a segment to the snake
            self.snake.AddSegment()
            #if all the food has been eaten
            if len(self.Food.Food) == 0:
                #replenishing the food
                self.replenishFood()

        #if the collisions rray is not empty
        if CollisionAI:
            # removing the collided food from the food array
            self.Food.Food.remove(CollisionAI[0])
            # adding one to the Ai score
            Globals.AIScore += 1
            # adding a segment to the AIsnake
            self.AI.AddSegment()
            # if all the food has been eaten
            if len(self.Food.Food) == 0:
                # replenishing the food
                self.replenishFood()

        #if the collision array is not empty
        if CollisionAIPlayer:
            # getting the position of the segment that the head of the snake collided with in the array of snake segments
            Index = self.snake.segments.index([i for i in self.snake.segments if i.rect.x == self.AI.segments[0].rect.x and i.rect.y == self.AI.segments[0].rect.y][0])
            # If the index isn't that of the head of the snake (their will only every be one collision between the head and a segment at any given time)
            if Index != 0:
                #taking one off of the player score
                #origionally this was going to be the number of segments removed, but that seemed to be a bit too harsh
                #I know i was meant to end the game, but once again this seemed to be a bit harsh.
                #The A* algorithm is good enough that keeping up with the AI's score whilst avoiding it is hard enough as it is.
                #This seemed to be a good balance between the different options above.
                Globals.CurrentScore -= 1
                Globals.AIScore += 1
                # removing the sprites
                # slicing the array based on the collision
                for i in self.snake.segments[Index:]:
                    self.snake.spriteslist.remove(i)
                    self.snake.segments.remove(i)

        #if the collision array is not empty
        if CollisionPlayerAI:
            #resseting directions of the player and switching to the game over scene
            Globals.x_change = Globals.segment_width + Globals.segment_margin
            Globals.y_change = 0
            Globals.Scenes['GameOver'] = True
            Globals.Scenes['Game'] = False

    #function to replenish
    def replenishFood(self):
        #looping endlessly until a condition is met and loop is broken.
        #I am assuming that their will always be space for food to spawn
        while True:
            # replenishing the food
            self.Food.replenish(self.Map)
            # checking for collisions between the snake and food
            #this prevents food from spawning in the snake
            Collisions = [pygame.sprite.spritecollide(i, self.Food.spriteslist, False) for i in self.snake.segments]
            #If the AI has been initialized
            if self.AI != None:
                # checking for collisions between the AI and food
                # this prevents fodo from spawning in the AI
                CollisionsAI = [pygame.sprite.spritecollide(i, self.Food.spriteslist, False) for i in self.AI.segments]
                #if their are no collisions between the AI and food, and between the player and food
                if CollisionsAI.count([]) == len(self.AI.segments) and Collisions.count([]) == len(self.snake.segments):
                    #setting up a tempary array
                    TempPaths = []
                    #cycling through the food
                    for i in self.Food.Food:
                        #trying to get a path from the ai to the food
                        Path = self.AI.Pathfinder.astar((self.AI.segments[0].rect.x, self.AI.segments[0].rect.y), (i.rect.x, i.rect.y), self.AI.segments)
                        #if the path is none, or the path is incomplete
                        if Path == None or Path[-1] != (i.rect.x, i.rect.y):
                            #continuing without adding the path to the temp paths
                            continue
                        else:
                            #if the pathfinding was successfull then the path is added to the array
                            TempPaths.append(Path)
                    #if the number of path is equal to the number of required food
                    if len(TempPaths) == Globals.InitialFoodNo:
                        break
            # if their are no collisions between the snake and food
            elif Collisions.count([]) == len(self.snake.segments):
                break
            # if their are collisions, then resetting the food array and sprites and replenishing the food again.
            for i in self.Food.Food:
                self.Food.spriteslist.remove(i)
            self.Food.Food = []

#Scene for UI objects for the game over event
class GameOverScene():
    def __init__(self):
        #Main header font
        self.FontH1 = pygame.font.SysFont('comicsans', 30)
        #sub header font
        self.FontH2 = pygame.font.SysFont('comicsans', 20)
        #text
        self.TxtGameOver = UIObjects.Text(self.FontH1, Globals.RED, (Globals.Screen_Width/2, Globals.height + 15), screen, 'Game Over')
        self.TxtPress = UIObjects.Text(self.FontH2, Globals.WHITE, (Globals.Screen_Width/2, Globals.height + 35), screen, 'Press any key to continue')

    #function to check for input
    def CheckInput(self):
        #if the user has pressed something
        for event in pygame.event.get():
            #if the user has pressed any key
            if event.type == pygame.KEYDOWN:
                screen.fill(Globals.BLACK)
                #changing to the mainmenu scene
                Globals.Scenes['GameOver'] = False
                Globals.Scenes['ScoreEntry'] = True

    #drawing the scene to the screen
    def draw(self):
        self.TxtGameOver.Display()
        self.TxtPress.Display()

class HighScores():
    def __init__(self):
        #Setting up the UI
        self.ButtonClose = UIObjects.Button(Globals.BLACK, Globals.Screen_Width / 2 - 80, 520, 150, 65, 'Close')
        self.FontH1 = pygame.font.SysFont('comicsans', 60)
        self.FontH2 = pygame.font.SysFont('comicsans', 40)
        self.FontScores = pygame.font.SysFont('comicsans', 25)
        self.Header = UIObjects.Text(self.FontH1, Globals.GREEN, [Globals.Screen_Width / 2, 60], screen, 'HighScores')
        #using string formatting methods to make a grid.
        #:<15 aligns to the left, :>15 aligns to the right
        TableHeaderTxt = '{:<15}{:>15}'.format('Name','Score')
        self.TableHeader = UIObjects.Text(self.FontH2, Globals.GREEN, [Globals.Screen_Width/2, 120], screen, TableHeaderTxt)
        self.HighScores = ReadScores.HighScores()

    def draw(self):
        #drawing the UI to the screen
        self.Header.Display()
        self.ButtonClose.draw(screen, outline = Globals.GREEN)
        self.TableHeader.Display()
        #looping through the Highscores
        #the highscores is an array of the top 10 scores
        for i in range(len(self.HighScores)):
            #setting the name and score as seperate variables
            name = self.HighScores[i][0]
            score = self.HighScores[i][1]
            #creating a text variable :: :<20 aligns to left, :>20 aligns to the right
            #creating a gap in between the two collums using (20 - len(name))
            TxtName = '{:<30}'.format(name)
            TxtScore = '{:<20}'.format(score)
            #creating tempoary text
            TempTextName = UIObjects.Text(self.FontScores, Globals.GREEN, [Globals.Screen_Width / 2 - 80, 180 + i * 30], screen, TxtName)
            TempTextScore = UIObjects.Text(self.FontScores, Globals.GREEN, [Globals.Screen_Width / 2 + 180, 180 + i * 30], screen, TxtScore)
            #displaying the text
            TempTextName.Display()
            TempTextScore.Display()


    def CheckInput(self):
        #getting the x and y positions of the mouse
        Mouse_x, Mouse_y = pygame.mouse.get_pos()
        # if the user has pressed something
        for event in pygame.event.get():
            # if the user closes the window
            if event.type == pygame.QUIT:
                Globals.done = True
                break
            # if the user presses a key
            if event.type == pygame.KEYDOWN:
                # if the key is escape then the game quits
                if event.key == pygame.K_ESCAPE:
                    screen.fill(Globals.BLACK)
                    Globals.Scenes['MainMenu'] = True
                    Globals.Scenes['HighScores'] = False
            #if the user is over the close button and presses the mouse button
            if self.ButtonClose.isOver((Mouse_x, Mouse_y)) and event.type == pygame.MOUSEBUTTONUP:
                screen.fill(Globals.BLACK)
                Globals.Scenes['MainMenu'] = True
                Globals.Scenes['HighScores'] = False

class ScoreEntry():
    def __init__(self):
        #setting up the IO
        self.FontH1 = pygame.font.SysFont('comicsans', 50)
        self.FontH2 = pygame.font.SysFont('comicsans', 40)
        self.FontScores = pygame.font.SysFont('comicsans', 25)
        self.TxtYouScored = UIObjects.Text(self.FontH1, Globals.GREEN, [Globals.Screen_Width / 2, 60], screen, 'You Scored:')
        self.TxtQ1 = UIObjects.Text(self.FontH1, Globals.GREEN, [Globals.Screen_Width / 2, 180], screen, 'Would you like to save your score?')
        self.ButtonYes = UIObjects.Button(Globals.BLACK, Globals.Screen_Width / 2 - 175, 260, 150, 65, 'Yes')
        self.ButtonNo = UIObjects.Button(Globals.BLACK, Globals.Screen_Width / 2 + 25, 260, 150, 65, 'No')
        #This bool determines if the user wants to enter their score
        self.EnterScore = False
        #This bool is activated if the user tries to save their score without entering anything
        self.Warning = False
        self.Warningtxt = UIObjects.Text(self.FontH2, Globals.RED, [Globals.Screen_Width / 2, 380], screen, 'You must enter at least one character')
        self.Input = ''
        self.TxtEntername = UIObjects.Text(self.FontH1, Globals.GREEN, [Globals.Screen_Width / 2, 60], screen, 'Enter you name:')
        self.ButtonOk = UIObjects.Button(Globals.BLACK, Globals.Screen_Width / 2 - 80, 260, 150, 65, 'Ok')
        self.TxtPress = UIObjects.Text(self.FontH2, Globals.RED, (Globals.Screen_Width/2, 380), screen, 'Press any key to continue')
        #This bool determines if the player meets the reuirements to add their score to the highscores
    def draw(self):
        PossibleEntry = (len(ReadScores.HighScores(False)) < Globals.MaxScores or Globals.CurrentScore > min(int(i[1]) for i in ReadScores.HighScores(False)))
        #if the user would like to save their score
        if self.EnterScore:
            #clearing the display
            screen.fill(Globals.BLACK)
            #drawing the button
            self.ButtonOk.draw(screen, outline = Globals.GREEN)
            self.TxtEntername.Display()
            #if the user input is empty
            if self.Input == '':
                #drawing the default value
                Input = UIObjects.Text(self.FontH1, Globals.GREEN, [Globals.Screen_Width / 2, 120], screen, 'YourName')
            #if the user input is less than/ = to 8
            #then just displaying the input
            elif len(self.Input) <= 8:
                Input = UIObjects.Text(self.FontH1, Globals.GREEN, [Globals.Screen_Width / 2, 120], screen, self.Input)
            #else, then displaying the last 9 characters of their input using string slicing
            else:
                Input = UIObjects.Text(self.FontH1, Globals.GREEN, [Globals.Screen_Width / 2, 120], screen, self.Input[len(self.Input)-8:])
            #if the users input is greater or equal to 20 characters.
            if len(self.Input) >= 20:
                #telling them that they have reached the maximum input length.
                Txt = UIObjects.Text(self.FontScores, Globals.RED, [Globals.Screen_Width / 2, 200], screen, 'You have reached the maximum input length')
                Txt.Display()
            if self.Warning:
                self.Warningtxt.Display()
            Input.Display()
        else:
            #displaying their score
            TxtScore = UIObjects.Text(self.FontH2, Globals.GREEN, [Globals.Screen_Width / 2, 100], screen,'{}'.format(Globals.CurrentScore))
            self.TxtYouScored.Display()
            TxtScore.Display()
            if PossibleEntry:
                #asking them if they want to save their score
                self.TxtQ1.Display()
                #drawing the buttons
                self.ButtonYes.draw(screen, outline = Globals.GREEN)
                self.ButtonNo.draw(screen, outline = Globals.GREEN)
            else:
                self.TxtPress.Display()

    def CheckInput(self):
        PossibleEntry = (len(ReadScores.HighScores(False)) < Globals.MaxScores or Globals.CurrentScore > min(int(i[1]) for i in ReadScores.HighScores(False)))
        #getting the current position of the mouse
        Mouse_x, Mouse_y = pygame.mouse.get_pos()
        # if the user has pressed something
        for event in pygame.event.get():
            # if the user closes the window
            if event.type == pygame.QUIT:
                Globals.done = True
                break
            # if the user presses a key
            if event.type == pygame.KEYDOWN and self.EnterScore:
                #getting the current pressed keys
                key = pygame.key.name(event.key)
                print(key)
                #using the string module to determine if the input is valid.
                #I found this easier than comparing the asciii values
                if (key in string.ascii_letters or key in string.digits) and len(self.Input) < 20:
                    #if it is a valid input, then adding it to the current input
                    self.Input += key
                    #removing the warning
                    self.Warning = False
                #if they press backspace
                if event.key == pygame.K_BACKSPACE:
                    #removing the last letter of the string using string slicing.
                    self.Input = self.Input[:-1]
            if not PossibleEntry and event.type == pygame.KEYDOWN:
                # clearing the screen and switching back to the main menu
                screen.fill(Globals.BLACK)
                Globals.Scenes['MainMenu'] = True
                Globals.Scenes['ScoreEntry'] = False


            if PossibleEntry:
                #if the user is over the no button, they press the mouse button, and they are still on the first part of this scene
                if self.ButtonNo.isOver((Mouse_x, Mouse_y)) and event.type == pygame.MOUSEBUTTONUP and not self.EnterScore:
                    #clearing the screen and switching back to the main menu
                    screen.fill(Globals.BLACK)
                    Globals.Scenes['MainMenu'] = True
                    Globals.Scenes['ScoreEntry'] = False

                #if the user is over the yes button, they press the mouse button, and they are still on the first part of this scene
                elif self.ButtonYes.isOver((Mouse_x, Mouse_y)) and event.type == pygame.MOUSEBUTTONUP and not self.EnterScore:
                    #clearing the screen and moving to the second part of this scene (user name input section)
                    screen.fill(Globals.BLACK)
                    self.EnterScore = True
            #if the user is over the ok button, they press the mouse button, and they are on the second part of this scene, and the input of their name is not blank
            if self.ButtonOk.isOver((Mouse_x, Mouse_y)) and event.type == pygame.MOUSEBUTTONUP and self.EnterScore:
                if self.Input != '':
                    ReadScores.SaveScore(self.Input)
                    Highscores.HighScores = ReadScores.HighScores()
                    self.Input = ''
                    Globals.Scenes['MainMenu'] = True
                    Globals.Scenes['ScoreEntry'] = False
                #if the input is blank, setting the warning bool to be true
                else:
                    self.Warning = True
            #adding a delay, makes getting input a bit more accurate.
            #however, you still get 'double key presses'. where the user presses a key once and it is read as two presses
            #im not sure how to fix this
            pygame.time.delay(50)

# Call this function so the Pygame library can initialize itself
pygame.init()

#setting up the screen
screen = pygame.display.set_mode([Globals.Screen_Width, Globals.Screen_Height])

# Set the title of the window
pygame.display.set_caption('Snake Game')

#initializing the pygame clock
clock = pygame.time.Clock()

#initializing the scenes
Menu = MainMenu()
Game = GameScene()
GameOver = GameOverScene()
Highscores = HighScores()
scoreentry = ScoreEntry()

#main loop
while not Globals.done:
    #loop for the mainmenu scene
    while Globals.Scenes['MainMenu']:
        #drawing the main menu scene to the display and checking the input
        Menu.draw()
        pygame.display.flip()
        Menu.CheckInput()

    #loop for the game scene
    while Globals.Scenes['Game']:
        #drawing the game scene to the display and checking the input
        Game.draw()
        pygame.display.flip()
        Game.CheckInput()
        Game.CollisionDetection()
        # Pause
        clock.tick(5)

    #loop for the game over scene
    while Globals.Scenes['GameOver'] and not Globals.Scenes['MainMenu']:
        GameOver.draw()
        pygame.display.flip()
        GameOver.CheckInput()

    #loop for the Highscores scene
    while Globals.Scenes['HighScores']:
        Highscores.draw()
        Highscores.CheckInput()
        pygame.display.flip()

    #loop for the score entry
    while Globals.Scenes['ScoreEntry']:
        scoreentry.draw()
        scoreentry.CheckInput()
        pygame.display.flip()

    #resetting
    Globals.Scenes['GameOver'] = False
    Globals.CurrentScore = 0
    Globals.AIScore = 0
    screen.fill(Globals.BLACK)
    #resetting the game
    Game = GameScene()
pygame.quit()

