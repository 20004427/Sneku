#AI pathfinding using the A* algoithm
import Globals
import numpy as np
import heapq
import warnings


#I followed the tutorial from:
#and https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
#To make this module
#All credit for the A* algorithm goes to Ryan Colling Wood
#The origional algorithm can be found at: https://gist.github.com/ryancollingwood/32446307e976a11a1185a5394d6657bc

##I also watched the video explaining the algorithm by The Coding Train: https://www.youtube.com/watch?v=aKYlikFAV4k&t=610s
#Luckly i have done some programming in js before so i was able to mostly understand what he was coding.
class Pathfinder():
    def __init__(self, Obsticals):
        #creating a blank array to store the matrix map of obsticals (1 being an obstical, 0 being anything else)
        self.Matrix = []
        #all possible movements from a given point. You can pressume that the AI will never move off screen, as the food will never be spawned off screen.
        self.neighbors = [(0,Globals.segment_width+Globals.segment_margin),(0,-(Globals.segment_width+Globals.segment_margin)),
                          (Globals.segment_height+Globals.segment_margin,0),(-(Globals.segment_height+Globals.segment_margin),0)]
        #I origionally used a full matrix for this, instead of passing the objects x and y values into this, but I had issues with getting the correct values
        #for the matrix map (this is a map of 1's and 0's where one's are walls and 0's are walkable terrain) due to how i did the rect of the objects.
        self.Obsticals = Obsticals

    #function to generate a matrix for the pathfinding, lower values represent good paths whilst higher values represent bad paths
    #Thus, the path is generated by finding the lowest sum of each possible path from point a to point b
    #This only needs to be called on the game scene initialization, as the map will not change whilst the game is running

    #This isn't actually needed as I ended up directly comparing x and y values instead of using a matrix.
    #I ran out of time to fix it. I think i know how to fix it though.
    #I've kept it just incase i try to fix it at somepoint, as it would be a much more practical and versatile method of using the A* algorithm
    def CreateMatrix(self, Obsticals):
        #setting a blank matrix varaible
        Matrix = []
        #creating the matrix
        #looping through all the y values
        for y in range(0, Globals.height + 1, Globals.segment_height + Globals.segment_margin):
            #setting a current row matrix
            CurrRow = []
            #looping through all the x values
            for x in range(0, Globals.width + 1, Globals.segment_width + Globals.segment_margin):
                #if the x and y values match an object
                if any(i[0][0] <= x <= i[0][1] and i[1][0] <= y <= i[1][1] for i in Obsticals.Matrix):
                    #adding a 1 to the row
                    CurrRow.append(1)
                else:
                    #else adding a 0
                    CurrRow.append(0)
            #adding the current row to the matrix
            Matrix.append(CurrRow)
        self.Matrix = Matrix
        #returning the matrix. For testing purposes
        return Matrix

    #Astar algorithm
    #Created by Ryan Colling Wood
    #adapted by me
    def astar(self, start, end, AIObjects, Matrix = None):
        # Create start and end node
        #setting their valeus to 0
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Heapify the open_list and Add the start node
        heapq.heapify(open_list)
        heapq.heappush(open_list, start_node)

        #adding a stop condition
        outer_iterations = 0
        max_iterations = 300

        # loop until you find the end
        while len(open_list) > 0:
            #adding 1 to the iterations
            outer_iterations += 1

            #creating a limit just incase a path can't be found
            #prevents endless looping and crashing
            if outer_iterations > max_iterations:
                #if we hit this point return the path such as it is
                #it will not contain the destination
                warnings.warn('end point not found, too many iterations')
                return return_path(current_node)

            # get the current node
            current_node = heapq.heappop(open_list)
            closed_list.append(current_node)

            #Found the goal
            if current_node == end_node:
                return return_path(current_node)

            #Generate children
            children = []
            for new_position in self.neighbors:
                # get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
                #if node is off the game window
                if node_position[0] > Globals.width or node_position[0] < 0 or node_position[1] > Globals.height or node_position[1] < 0:
                    continue

                #initially i used a matrix like they did in the tutorial, but i had issues with initializing it due to the obsticals being created by changing their rect
                #rather than creating multiple smaller obsticals to make one big obstical
                #so i used this method instead. I am comparing the current node position to the position and size of each obstical.
                #It isn't the cleanest way of doing this, and will limit future development of the program, but it works.
                #I.E. If i wanted the AI to chase the player and also collect food, I would have used a cost based matrix, where obsticals are 3,
                #food is 2, player is 1 and walkable terrain is 0 (or something like that). The algorithm looks for the path of lowest cost.
                if any(i[0][0] <= node_position[0] <= i[0][1] and i[1][0] <= node_position[1] <= i[1][1] for i in self.Obsticals):
                    continue

                #if the node x and y values are equal to one of the AI segments x and y values
                if any(i.rect.x == node_position[0] and i.rect.y == node_position[1] for i in AIObjects[1:]):
                    continue

                #create new node:
                new_node = Node(current_node, node_position)

                #append the new node to the children array
                children.append(new_node)

            for child in children:
                #child is in the closed list
                if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                    continue

                #create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                #child is already in the open list
                if len([open_node for open_node in open_list if child.position == open_node.position and child.g > open_node.g]) > 0:
                    continue
                #if child isn't in the open list, then add it.
                heapq.heappush(open_list, child)
        warnings.warn("couldn't get a path to destination")
        return None

#this isn't used, but was used for another tutorial I looked at. And it is a usefull function to have, so i kept it
def heuristic(a, b):
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

#node class
class Node():
    def __init__(self, parent=None, position=None):
        #setting variables
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    #Honestly, I don't know what these do.
    def __eq__(self, other):
        return self.position == other.position

    def __repr__(self):
        return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f


#function to return the path
def return_path(current_node):
    #creating an empty path
    path = []
    current = current_node
    #looping through the nodes until the start point is reached (paths backwards)
    while current is not None:
        #adding the current node position to the path
        path.append(current.position)
        current = current.parent
    #returning the reversed path
    return path[::-1]