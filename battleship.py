# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 14:22:21 2022
version 1.0 on Nov 23 2022

@author: Filip Niklas
"""
import random
import csv
import pandas as pandasForSortingCSV
from datetime import date
import time

while True: #The whole program is nested in a while loop such that we can replay if the user wants.
    
    #Board begins as an empty list
    board = []
    
    #Board is made iterating x a number of times and then appending string "O" 
    #fives time to each iteration which then makes the board
    for x in range(10):
      board.append(["O"] * 10)
    
    #Board print as function, which includes a .join function for better visuals
    def print_board(board):
      for row in board:
        print(" ".join(row))
    
    #Initial flavour text
    print("""
                                     |__
                                     |\/
                                     ---
                                     / | [
                              !      | |||
                            _/|     _/|-++'
                        +  +--|    |--|--|_ |-
                     { /|__|  |/\__|  |--- |||__/
                    +---------------___[}-_===_.'____              /
                ____`-' ||___-{]_| _[}-  |     |_[___\==--         \/    _
 __..._____--==/___]_|__|_____________________________[___\==--___,-----' .7
|                                                                         /
 \_______________________________________________________________________|
                                                       Art by Matthew Bace
          """)
    print("""\nWelcome to Filip's Battleship game, Captain! Your goal is to sink all enemy vessels
    by guessing the right positions. Intelligence reports that the enemy has five ships of 
    various sizes hidden on the map: a carrier (5), a battleship (4), a cruiser (3), 
    a submarine (3) and a destroyer (2). Quartermaster informs us we have 30 shots available 
    to fire upon the enemy. May it be enough. Godspeed, Captain, and may your aim be true!\n""")
    
    #Calls the function of the board, which prints it. 
    print("This is the map:")
    print_board(board)
    
    enemy_ships = [] #This is the full list of all enemy ships. Appended to by ship_extension func.
    
    def ship_pos_generator(board): #Generates the initial position of the ship based on the dimensions of the board.
        
        def pos_generator(board): #Actual position generator. 
            ship_pos = [] #Position begins as empty list.
            row = random.randint(0, len(board) - 1) #Row coordinate: a random number based on the size of the board.
            column = random.randint(0, len(board[0]) - 1) #Column coordinate, same as above except targets the board index.
            ship_pos.append(row)
            ship_pos.append(column)
            return ship_pos
            
        checking_pos = pos_generator(board)
        
        #After creation, the position is checked against existing positions in the checker function.
        #While a collision obtains (True), the position is overwritten by a new generation and checked again
        #When no collision obtains (False), the position is returned
        
        while ship_collision_checker(checking_pos) == True:
            checking_pos = pos_generator(board)
        return checking_pos
    
    def ship_collision_checker(ship_pos): #Checks ship position against existing ones. Accepts either list or dict. 
    
        #If collision obtains, returns True. If no collision obtains, returns False. 
        
        if len(enemy_ships) == False: #If there are no existing positions, False is returned by default.
            return False 
        
        else: #Checks whethether the argument is list or dict, as different loops must apply to get to the values of each.
    
            if isinstance(ship_pos, dict):
                for ship in enemy_ships:
                    for position in ship.values():
                        for position2 in ship_pos.values():
                            if position == position2:
                                return True
                return False
                                
            if isinstance(ship_pos, list):
                for ship in enemy_ships:
                    for position in ship.values():
                        if position == ship_pos:
                            return True
                return False
        
    def ship_ext_dir(location, size): #Gives directions for ship extender. Accepts list as location and int as size.
    
        #This function checks the ship size against the size of the board, and is meant
        #to prevent the extender from building ships that cross the boad edge.
        #The directions are dynamically based on the board and ship size.
        #The ships coordinates are checked by accessing the locations's index. 
        #Returns one of four coordinate directions: up, down, left or right.
        #Given the board and ship size are dynamic, there may be unforeseen bugs if either
        #exceeds possible parameters, in that case, option else paths execute with bug prints.
        
        row_or_column = random.choice(["row", "column"]) #Row or column direction is randomly chosen.
        
        if row_or_column == "row": #Row direction means either going up or down the rows of the board.
            
            
            if location[0] < size - 1: #If coordinate is on the upper side, expansion must go down.
                return "go_down"
            elif location[0] > len(board) - size - 1: #If coordinate is on the lower side, expansion must go up.
                return "go_up"
            elif location[0] > size - 2 and location[0] < len(board) - size + 1: #If between, expansion can go either way.
                
                up_or_down = random.choice(["up", "down"]) #Another random choice to decide up or down.
                if up_or_down == "up":
                    return "go_up"
                elif up_or_down == "down":
                    return "go_down"
                
            else: #If the parameters don't work, given the board and size are dynamic, here is a bug reporter.
                print("Bug at ship_ext_dir :: inner else row")
                return "Bug at ship_ext_dir :: inner else row"
            
            
        elif row_or_column == "column": #Column direction means eiher going right or left on the columns of the board.
            
            
            if location[1] < size - 1: #If coordinate is on the left side, expansion must go right.
                return "go_right"
            elif location[1] > len(board[0]) - size - 1: #If coordinate is on the right side, expansion must go left.
                return "go_left"
            elif location[1] > size - 2 and location[1] < len(board[0]) - size + 1: #If between, expansion can go either way.
                
                right_or_left = random.choice(["right", "left"]) #Another random choice to decide left or right.
                if right_or_left == "right":
                    return "go_right"
                elif right_or_left == "left":
                    return "go_left"
                
            else:
                print("Bug at ship_ext_dir :: inner else col")
                return "Bug at ship_ext_dir :: inner else col"
            
            
        else:
            print("Bug at ship_ext_dir :: outer else")
            return "Bug at ship_ext_dir :: outer else"
    
    def ship_extension(location, size): #Extends the ship size based on initial location(list) and intended size(int). 
    
        ship_pos = {} #The multi-position ship begins as empty dictionary.
        ship_pos["ship_pos_0"] = location #The initial location is added to the dictionary. Necessary for the checker function. 
        direction = ship_ext_dir(location, size) #Receives from ship_ext_dir about which direction to extend towards.
        
        if ship_collision_checker(ship_pos) == False: #First the ship location is checked for collisions. False means no collisions.
            
            for extension in range(size): #This loop runs based on the inteded size of the ship.
                extension + 1
                
                #Extensions are new positions dictated by the direction and the size.
                #For every loop, extension increases by one, which is used in the 
                #generation of the adjacent position(list), which is then added to
                #as an entry to the ship dictionary.
                
                if direction == "go_up":
                    new_pos_row = location[0] - extension
                    new_pos_col = location[1]
                    new_list = []
                    new_list.append(new_pos_row)
                    new_list.append(new_pos_col)
                    ship_pos["ship_pos_" + str(extension)] = new_list
                elif direction == "go_down":
                    new_pos_row = location[0] + extension
                    new_pos_col = location[1]
                    new_list = []
                    new_list.append(new_pos_row)
                    new_list.append(new_pos_col)
                    ship_pos["ship_pos_" + str(extension)] = new_list
                elif direction == "go_left":
                    new_pos_row = location[0]
                    new_pos_col = location[1] - extension
                    new_list = []
                    new_list.append(new_pos_row)
                    new_list.append(new_pos_col)
                    ship_pos["ship_pos_" + str(extension)] = new_list
                elif direction == "go_right":
                    new_pos_row = location[0]
                    new_pos_col = location[1] + extension
                    new_list = []
                    new_list.append(new_pos_row)
                    new_list.append(new_pos_col)
                    ship_pos["ship_pos_" + str(extension)] = new_list
                    
            if ship_collision_checker(ship_pos) == False: #After loop exhaustion, the multi-position ship is checked again for collisions.
            
                #Provided no collisions, the ship dictionary gets appended to the total list of enemy ships and returned.
                enemy_ships.append(ship_pos)
                return ship_pos  
            
            else: #If collision is True, the extender function returns False to the builder, in order to restart the process.
                return False
            
        else: #If collision is True, the extender function returns False to the builder, in order to restart the process.
            return False
    
    def ship_builder(size): #Control function that builds a ship based on its size(int).
        
        ship_as_dict = False #Sets variable which is to become a dictionary made up of positions(list) initally as False.
        while ship_as_dict == False:
        
            ship_as_list = ship_pos_generator(board) #Generates the first ship position at a free location on the board.
            
            ship_as_dict = ship_extension(ship_as_list, size) #Extends a multi-position ship based on size and board availability.
        
            #When ship extension is successful, it overwrites ship_as_dict as a non-empty dictionary,
            #which breaks the while loop and proceeds to return the completed ship.
            #Else, ship extension returns False, which does not overwrite the while loop and restarts
            #the process again, until successful. 
            
        return ship_as_dict
    
    
    carrier = ship_builder(5)
    #print(carrier)
    battleship = ship_builder(4)
    #print(battleship)
    cruiser = ship_builder(3)
    #print(cruiser)
    submarine = ship_builder(3)
    #print(submarine)
    destroyer = ship_builder(2)
    #print(destroyer)
    
    #print("List of enemy ships:\n", enemy_ships)
    
    def identity_checker(my_list): #Accepts list made up of dictionaries. Used for testing.
        
        pos_list = [] #Empty list to hold unique elements from the list.
        duplicate_pos_list = [] #Empty list to hold the duplicate elements from the list.
        
        for ship in my_list:
            for position in ship.values():
                if position not in pos_list:
                    pos_list.append(position)
                else:
                    duplicate_pos_list.append(position)
                
        print("List of duplicates >>\n", duplicate_pos_list)
        print("Unique Item List >>\n", pos_list)
    
    #identity_checker(enemy_ships)
    
    def remove_empty_dict(enemy_ship_list): #Removes empty dictionary (shipwrecks) from the enemy ships list
        enemy_ship_list = list(filter(None, enemy_ships))
        return enemy_ship_list
    
    def check_user_input(input): #Checks user input for integers, returns incorrect when no integers given.
        try:
            integer = int(input)
            return integer
        except ValueError:
            print("Sir, we need a number for the coordinate!")
            return "incorrect"
        
    def game(rounds): #This is the function for the main game. Takes no. of rounds as argument. Returns user score.
        
        user_score = 0 #Tracks the points the user achieves through the game.
        hit = 5
        miss = 3
        sink = 10
        win = 25
        
        for turn in range(rounds): #Game is turn based, determined by the int in rounds per the func. argument. 
            
            flag = False #Flag variable used to steer the function. Will be overwritten as true if user strikes an enemy ship. 
            print("\nTurn", turn + 1) #Adds +1 to turn. When it matches the number of rounds, the game ends.
            
            new_shot_text = random.choice(["a", "b", "c", "d", "e"]) #Since there will be many rounds, there are addition options for flavor text.
            if new_shot_text == "a":
                print("Captain, gun control needs new coordinates! Where shall we shoot?")
            if new_shot_text == "b":
                print("Captain! Where shall we shoot? In your infinite wisdom, give us the coordinates.")
            if new_shot_text == "c":
                print("The next shot has hit written all over it, Captain. We just need the coordinates to send it home.")
            if new_shot_text == "d":
                print("Captain, we ask you kindly for the coordinates. The gun crew are working overtime to turn the turrets, but they need coordinates!")
            if new_shot_text == "e":
                print("By Jove, we shall strike an enemy vessel, if not sink it outright. Give us but an aim, Captain!")
            
            target_pos = [] #The position of the user begins as empty list. 
            guess_row = "incorrect" #Because the user can input a non-int, a while loop is set in place that breaks when the user inputs an int correctly.
            while guess_row == "incorrect":
                guess_row_raw = input("Insert row coordinate of 0 to {}: ".format(len(board) - 1))
                guess_row = check_user_input(guess_row_raw)
            guess_col = "incorrect" #Same as above, but for column this time.
            while guess_col == "incorrect":
                guess_col_raw = input("Insert column coordinate of 0 to {}: ".format(len(board[0]) - 1))
                guess_col = check_user_input(guess_col_raw)
            target_pos.append(guess_row) #When the user has correctly input an int for row and column,
            target_pos.append(guess_col) #each are appended to the target position list. 
            
            for ship in enemy_ships: #Now we iterate through the ships (dict) in the ship list.
                ship_copy = ship.copy() #Because dictionaries cannot be modified while iterated, a copy is made of the present ship (dict) and the copy gets iterated.
                for key, pos in ship_copy.items(): #We iterate through the key and value (position) in the ship copy (dict)
                    if target_pos == pos: #When the user's target position (list) matches an existing ship value (list), the following incurs:
                        del ship[key] #The key with the associated ship value is deleted in the original dictionary.
                        flag = True #Flag is set to true, which prevents the outcome below.
                        board[guess_row][guess_col] = "X" #The board is visibly modified by marking a strike with an X.
                        print_board(board) #The modified board is re-printed.
                        print("A hit, Captain! We have struck an enemy ship at row {r}, col {c}".format(r=guess_row, c=guess_col))
                        user_score += hit #Add hit score to the users total score.
                        if ship == {}: #In the case that the ship has all its parts destroyed (deleted), it becomes an empty dictionary.
                            print("Captain, we have sunk an enemy vessel!")
                            user_score += sink #User is additionally rewraded for sinkinga whole ship.
                        enemy_ships_checked = remove_empty_dict(enemy_ships) #The ship list is purged of empty dictionaries. Because we cannot alter a variable outside the func. we create a new list here.
                        if len(enemy_ships_checked) == False: #When the purged enemy ship list is empty, the game is won.
                            user_score += win
                            print("Congratulations, you have sunk all the enemy vessels! Glory be to you, Captain!")
                            return user_score #Func. ends since there are no more enemy ships to strke or sink!
                        
        
            if flag == False: #When the user fails to strike any enemy vessels, flag remains false and the following ensues:
                
                if (guess_row < 0 or guess_row > len(board) - 1) or (guess_col < 0 or guess_col > len(board[0]) - 1): #In the case that user inputs an int beyond the board scope.
                    
                    if turn == rounds:
                         print ("Game Over")
                    else:
                        user_score -= miss
                        print ("Oops, that's not even in the ocean.")
                          
                elif(board[guess_row][guess_col] == "X") or (board[guess_row][guess_col] == "Ø"): #In the case thta the user inputs an int that matches an existing strike or miss.
                    
                    if turn == rounds:
                        print ("Game Over")
                    else:
                        print ("You guessed that one already.")
                      
                else:
                    
                    if turn == rounds:
                        print ("Game Over")
                    else: #Most likely, the user simply misses within the board.
                        user_score -= miss
                        print ("You missed hitting any enemy ships!")
                        board[guess_row][guess_col] = "Ø" #Board is modified to display a miss.
                        print_board(board)
                        
                        
        return user_score #When the user runs through all the rounds without sinking all enemy ships, the func. returns the accumulated score. 
                        
    score = game(30) #Calls the game func., argument is the no. of rounds for the game and returns a user score.
    
    #score = 10 #For testing purposes, you can skip the game func. and just give the user a fixed score.
    
    print("Your score this game was: {} points!".format(score))
    
    name = input("Type in your name: ") #User may record their score, which gets stored in a dictionary along with the date the game was played.
    user_score = {}
    user_score['name'] = name
    user_score['score'] = score
    today = date.today()
    user_score["time"] = today.strftime("%B %d, %Y")
    
    
    with open("battleship_stats.csv", "a") as stats_csv: #Opens and appends the user's name, score and date of playing the game to a separate .csv file. 
        fields = ["name", "score", "time"]
        stats_writer = csv.DictWriter(stats_csv, fieldnames=fields)
        #stats_writer.writeheader()
        stats_writer.writerow(user_score)
        
    with open("battleship_stats.csv", "r") as stats_csv: #Opens and reads the same .csv file as above and displays the top then players (by score).
        csvData = pandasForSortingCSV.read_csv(stats_csv)
        
        csvData.sort_values(["score"], axis=0, ascending=[False], inplace=True)
        csvData = csvData.set_index("time")
        csvData = csvData.head(10)
        
        print("\n")
        print(f'|{"Battleship Statistics":^40}|')
        print(f'|{"- TOP TEN CAPTAINS -":^40}|')
        print(csvData)
        print("\n")
    
    while True: #Lastly, a rematch prompt is asked. 
       rematch = str(input("Would you like to play again? (y/n) "))
       if rematch in ("y", "n", "Y", "N"): #When the user inputs the correct strings, the inner loop is broken. 
           break
       print("Invalid input!") #When the user inputs the incorrect input, the inner loop repeats with printing an error message. 
    if rematch == "y" or rematch == "Y": #In the case of a rematch, the outer while loop continues and the whole program effectively begins agian.
        continue
    else: #In the case of the user not wanting to play again, the outer while loop is broken, ending the program. 
        print("\nThank you for playing Filip's Battleship game! We hope to see you back, Captain!")
        print("\n\nProgram will terminate in 10 seconds . . .")
        time.sleep(10)
        break
    

#Ideas for further development: allow the user to put down their own ships, 
#this would require a new board, a control scheme to put down the ships in a 
#convenient way, and an AI that attempts to guess the players ships and sink them.
#Alter the coordinate system to be 1-10 rather than 0-9 for user friendliness.
#Add more flavour text to spicy things up between the rounds with jokes and silly dialogue. 
#Make the game a two-player game. 