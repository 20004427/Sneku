# --- Globals --- #

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Screen size
#height and width of the game area
height = 600
width = 600
#height and width of the actual screen
Screen_Height = 650
Screen_Width = 600


# Margin between each segment
segment_margin = 3

# Set the width and height of each snake segment
segment_width = int(min(height, width) / 40 - segment_margin)
segment_height = int(min(height, width) / 40 - segment_margin)

# Set initial speed player
x_change = segment_width + segment_margin
y_change = 0

###AI###
#set initial speed AI
x_change = segment_width + segment_margin
y_change = 0
AIScore = 0

#Learning
#This isn't needed as I didn't impliment a learning AI.
#But it might be fun to try and create an enviroment for Q-learning based on this program
#over the summer break, so i kept the variables for q-learning in for the moment.
Food_Bonus = 5
Collision_Player = -5
Collision_Wall = -5
Collision_Screen = -5
IdleReward = 0.1


# Scenes
#used to controll scenes
Scenes = {'MainMenu': True, 'Game': False, 'GameOver': False, 'HighScores': False, 'ScoreEntry':False}

#MainLoop controll
done = False

#Food
InitialFoodNo = 5

#ScorePlayer
CurrentScore = 0

#ScoreAI
AICurrentScore = 0

#MaxObsticals
MaxObjects = 20

#MaxScores allowed to be saved
MaxScores = 100