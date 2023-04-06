import Globals
#was going to use plotly to create a table of the names and scores, then export it as an image to display is pygame
#but had trouble getting the orca package to work.
#it seems to be a common issue.

#function to save scores
def SaveScore(Name):
    #trying to open the file as r+ (will only work if the file exists)
    try:
        f = open('Scores.txt', 'r+')
        Scores = [i for i in f.readlines()]
        f.close()
    #if the file doesn't exist
    except:
        #creating a new txt file
        f = open('Scores.txt', 'w+')
        scores = []

    #setting a dictionary variable
    DictScores = {}
    #looping through scores
    for i in Scores:
        #unpacking the file lines
        key, value = i.split()
        DictScores[key] = int(value)
    #setting the current users name to their current score
    DictScores[Name] = Globals.CurrentScore
    #sorting the dictionary using pythons inbuilt sort function, by default this sorts from lowest to highest, so reverse must be True
    DictScores = [(key, value) for key, value in sorted(DictScores.items(), key=lambda x: x[1], reverse=True)]

    #saving the scores to the file
    f = open('Scores.txt', 'w+')
    #if the length of the DictScores is less than the maximum allowed scores
    #then all scores in DictScores are saved
    if len(DictScores) <= Globals.MaxScores:
        for key, value in DictScores:
            f.write(key + ' ' + str(value) + '\n')
    #else only the first n scores are saved, where n is Globals.maxscores
    else:
        for key, value in DictScores[:Globals.MaxScores]:
            f.write(key + ' ' + str(value) + '\n')
    f.close()

def HighScores(HighScores = True):
    #if the scores.txt file exists, then opening it as r+ (read)
    try:
        f = open('Scores.txt', 'r+')
        Scores = [i for i in f.readlines()]
        f.close()
    #if it doesn't exist, then opening it as w+, (write), which creates a new file
    except:
        f = open('Scores.txt', 'w+')
        Scores = []

    #setting a dictionary var
    DictScores = {}
    #looping and unpacking
    for i in Scores:
        key, value = i.split()
        DictScores[key] = int(value)
    #sorting
    DictScores = [(key, value) for key, value in sorted(DictScores.items(), key=lambda x: x[1], reverse=True)]
    #returning the top 10 scores
    if HighScores:
        return(DictScores[:11])
    else:
        return DictScores