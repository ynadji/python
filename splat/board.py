import os
import random

class Board:
     num_dots = 0
     grid = []
     
     #Constructor for the Board class.
     #num_players - the number of players in the game
     #x_size - the number of columns the board will have
     #y_size - the number of rows the board will have
     #rounds - the number of rounds the game will have
     #num_end_square - the number of squares that must be left to end the game.
     def __init__(self, num_players, x_size, y_size, rounds, num_end_square): 
        global num_dots
        global grid
        
        self.num_players = num_players
        self.x_size = x_size
        self.y_size = y_size
        self.rounds = rounds
        self.num_end_square = num_end_square

        self.init_grid()
        


     #Determines if the grid has enough dots to end the game.
     #True when there are enough dots, false otherwise.
     def at_max_dots(self):
          global num_dots
          
          board_size = self.x_size * self.y_size
          if ( (board_size - self.num_dots) <= self.num_end_square ):
               return True
          else:
               return False

     #Randomly places a dot on the grid.
     #Does not add a dot if there is already a dot at that location
     #or the max number of dots has been reached.
     def add_dot(self):
          global grid

          if not self.at_max_dots():
               x = random.randrange(0, self.x_size)
               y = random.randrange(0, self.y_size)
               
               loc = [x,y]
 
               while self.is_dot_at(loc):
                    x = random.randrange(0, self.x_size)
                    y = random.randrange(0, self.y_size)
                    loc = [x,y]
                   
 

               self.grid.append([None, x, y])
               self.num_dots += 1
               
     #Initializes the grid to start with the numebr of players + 1 dots.
     def init_grid(self):
          global num_dots

          index = 0
          while index < self.num_players + 1:
               self.add_dot()
               index += 1

     #Determines if there is a dot at location.
     def is_dot_at(self, location):
          global grid

          for each in self.grid:
               if (each[1] == location[0]) and (each[2] == location[1]):
                    return True
      
          return False
                 
     #Prints the list of dots.
     def print_grid(self):
          global grid
          self.grid.sort()
          for i in range(len(self.grid)):
               print self.grid[i]

     
     #Allows the player to claim a dot as their own.
     #Only works when there is an unclaimed dot at location.
     def claim_dot(self, player, location):
          global grid

          for each in self.grid:
               if (each[0] == None and each[1] == location[0]) and (each[2] == location[1]):
                  each[0] = player

     #Moves a dot to another unclaimed spot.
     #Only works when dot as specified actually exists.
     def move_dot(self, dot):
          global grid

          if self.grid.count(dot) > 0:
               player = dot[0]
               self.grid.remove(dot)
          
               x = random.randrange(0, self.x_size)
               y = random.randrange(0, self.y_size)
               
               loc = [x,y]
 
               while self.is_dot_at(loc):
                    x = random.randrange(0, self.x_size)
                    y = random.randrange(0, self.y_size)
                    loc = [x,y]
                   
               self.grid.append([player, x, y])

     #Determines if a location is in a list of dots.
     def is_in_list(self, loc, list):
          for each in list:
               if (each[1] == loc[0]) and (each[2] == loc[1]):
                    return True
          return False

     #Determines if two locations are adjacaent
     def neighbors(self, loc1, loc2):
          if ((loc1[0] == loc2[0] - 1) or (loc1[0] == loc2[0]) or (loc1[0] == loc2[0] + 1)) and ((loc1[1] == loc2[1] - 1) or (loc1[1] == loc2[1]) or (loc1[1] == loc2[1] + 1)):
                  return True
          return False     

     #Returns all the locations adjacent to the dot.
     def find_all_adjacent(self, dot):
          global grid
          list = []
          
          for each in self.grid:
               if each[0] == dot[0]:
                    if self.neighbors((dot[1], dot[2]), (each[1], each[2])):
                         list.append(each)
                    
          return list

     #Finds the longest string of dots for player (player is the players name)
     def longest_string(self, player):
          global grid

          count = 0
          for each in self.grid:
               if each[0] == player:
                    found = self.find_all_adjacent(each)

                    for item in found:
                         temp_list = self.find_all_adjacent(item)
                         for item2 in temp_list:
                              if not self.is_in_list((item2[1], item2[2]), found):
                                   found.append(item2)
                                   
                    if(len(found) > count):
                         count = len(found)
          return count

     #Goes through all the players and sees who has the longest string of dots.
     def find_winner(self):
          global grid
          longest = (None, 0)
  
          for each in self.grid:
               cur_longest = self.longest_string(each[0])
               if(cur_longest > longest[1]):
                    longest = (each[0], cur_longest)
          return longest

     #Returns the list of players
     def player_name_list(self):
          global grid
          
          list = []
          for each in self.grid:
               if not self.is_in_list2(each[0], list):
                    list.append(each[0])
               
     #Determines if a string is already in a list of strings.
     def is_in_list2(self, name, list):
          for each in list:
               if (name == each):
                    return True
          return False

     
                    
     
