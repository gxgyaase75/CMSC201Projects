"""
File: frogger.py
    Author: Gabriel Gyaase
    Date: 11/14/2024
    Section: 10
    E-mail: ggyaase1@umbc.edu
    Description: This file simulates a game 
                 of Frogger, where the user
                 has to get the frog on the
                 other side of the road using
                 the commands 'w', 'a', 's', 'd' 
                 (for up, left, down and right 
                 respectively) and 'j' for the
                 frog to jump to a diagonally
                 adjacent spot.
    Note: Meant to be used with game1.frog, game2.frog and game3.frog.
    Given Score: 80/105
"""
import os
root, directories, files = next(os.walk('.'))

FROGGER = '\U0001318F'
EMPTY_SPACE = '_'
BLANK_SPACE = ' '
CLOSED_SPACE = 'X'

def display_files(): # Displays files and asks user which one they want to play
    """
    :return: The selected file the user picks.
    """
    file_num = 1
    file_list = []
    for file in files:
        if '.frog' in file:
            file_list.append(file)
            print(f'[{file_num}]', file)
            file_num += 1
    file_selected = False
    select_file = int(input("Enter an option or filename: "))
    while file_selected == False:
        if select_file != 0 and select_file <= file_num:
            file_selected = True
        else:
            print("Invalid option.")
            select_file = int(input("Enter an option or filename: "))
    file = file_list[select_file - 1]
    return file

def list_breakdown(list): # Converts the .frog files into lists
    """
    :param: The list of strings containing the game's info
    :return: A new list of the integers containing the game's info
    """
    for i in range(len(list)):
        if '\n' in list[i]:
            list[i] = int(list[i][:-2]) # Uses string slicing to remove \n
        else:
            list[i] = int(list[i])
    return list

def create_outer_rows(length, list): # Removes first and last lines to grid
    """
    :param: The length of each row in the grid
    :param: The rows of the grid used in the game
    :return: A new list containing all of the rows needed for the game
    """
    new_list = []
    start_line = ''
    end_line = ''
    for i in range(length):
        start_line += ' '
        end_line += ' '
    start_line += '\n'
    end_line += '\n'
    new_list.append(start_line)
    for i in range(len(list)):
        new_list.append(list[i])
    new_list.append(end_line)
    return new_list

def make_grid(list): # Turns the file into a 2D list
    """
    :param: The list of each row in the file selected
    :return: N/A; creates a new grid
    """
    grid = []
    for i in range(len(list)):
        row = []
        for char in list[i]:
            if char != '\n':
                row.append(char)
        grid.append(row)
    return grid

def print_grid(grid, frog_pos): # Prints the grid as text each turn
    """
    :param: the grid the game takes place on
    :param: the current position of the frog
    :return: N/A; outputs the grid with the frog
    """
    for i in range(len(grid)):
        line = ''
        for j in range(len(grid[i])):
            if i == frog_pos[0] and j == frog_pos[1]:
                line += FROGGER
            else:
                line += grid[i][j]
        print(line)

def make_move(action, frog_pos, grid): # Allows the frog to move any direction
    """
    :param: a string of which direction the user wants to use
    :param: the position of the frog on the grid
    :param: the grid where the game takes place
    :return: True/False if the action has been successfully made
    """
    row_length = len(grid)
    col_length = len(grid[0])
    pos_x = frog_pos[0]
    pos_y = frog_pos[1]
    if action == 'W': # Up
        if pos_x == 0: # Stops the frog from going too far up
            print("Frogger is already at the top!")
            return False
        else:
            if pos_x == 0:
                grid[pos_x][pos_y] = BLANK_SPACE
            else:
                grid[pos_x][pos_y] = EMPTY_SPACE
            pos_x -= 1
    elif action == 'A': # Left
        if pos_y == 0: # Stops the frog from going too far left
            print("Frogger can't go anymore left!")
            return False
        else:
            if pos_x == 0:
                grid[pos_x][pos_y] = BLANK_SPACE
            else:
                grid[pos_x][pos_y] = EMPTY_SPACE
            pos_y -= 1
    elif action == 'S': # Down (no need to prevent it from going anymore down)
        if pos_x == 0: 
            grid[pos_x][pos_y] = BLANK_SPACE
        else:
            grid[pos_x][pos_y] = EMPTY_SPACE
        pos_x += 1
    elif action == 'D': # Right
        if pos_y == (col_length - 1): # Stops the frog from going too far right
            print("Frogger can't go anymore right!")
            return False
        else:
            if pos_x == 0:
                grid[pos_x][pos_y] = BLANK_SPACE
            else:
                grid[pos_x][pos_y] = EMPTY_SPACE
            pos_y += 1
    return [pos_x, pos_y]
    
def jump_space(frog_pos, coordinates, jump_count, grid):
    """
    :param: frog_pos: a list of the frog's current coordinates
    :param: coordinates: the list of coordinates of where the 
            user wants to jump to
    :param: jump_count: the number of jumps the frog has
    :param: grid: the grid where the game takes place
    :return: the new coordinates of the frog's position
    """
    col_length = len(grid[0])
    print(coordinates)
    if jump_count == 0: # Returns false if there are no jumps left.
        print("You have no jumps.")
        return False
    elif len(coordinates) != 2: # Returns false if there aren't two coordinates
        print("Invalid coordinates.")
        return False
    for i in range(len(coordinates)):
        coordinates[i] = int(coordinates[i])
    frog_x = frog_pos[0]
    frog_y = frog_pos[1]
    jump_x = coordinates[0]
    jump_y = coordinates[1]
    if (((frog_x - jump_x) > 1) or ((frog_x - jump_x) < -1)) or \
        ((jump_y < 0) or (jump_y > col_length - 1)):
        print("Jump is too far.") 
        return False # Returns false if jump is too far/out of bounds
    else:
        frog_x = jump_x
        frog_y = jump_y
        return [frog_x, frog_y]
    
def shuffle_rows(frog_pos, grid, row_speed):
    """
    :param: The current position of the frog
    :param: The grid the game takes place on
    :param: A list of the respective speed of each list
    :return: N/A; creates the reshuffled grid
    """
    old_frog_x = frog_pos[0] # Shifts rows by their respective speeds
    old_frog_y = frog_pos[1] # Records frog's position
    if old_frog_x != 0: # Removes frog and replaces proper space
        grid[old_frog_x][old_frog_y] = EMPTY_SPACE
    else:
        grid[old_frog_x][old_frog_y] = BLANK_SPACE
    for i in range(1, len(grid) - 1):
        turn = int(row_speed[i - 1]) * -1
        grid[i] = grid[i][turn:] + grid[i][:turn] # Shifts rows
    if old_frog_x == frog_pos[0] and old_frog_y == frog_pos[1]:
        grid[old_frog_x][old_frog_y] = FROGGER

def check_collision(frog_x, current_grid, grid_template):
    """
    :param: the current row the frog is on
    :param: the grid the game takes place
    :param: a copy of the grid from the beginning of the game
    """
    # Checks every blocked space, and confirms if a frog has "taken" one block.
    if frog_x != 0 and frog_x != (len(current_grid) - 1):
        block_count = 0
        current_block_count = 0
        for i in range(len(current_grid)):
            for j in range(len(current_grid[i])):
                if current_grid[i][j] != EMPTY_SPACE and \
                current_grid[i][j] != BLANK_SPACE and \
                current_grid[i][j] != FROGGER:
                    current_block_count += 1
                if grid_template[i][j] != EMPTY_SPACE and \
                current_grid[i][j] != BLANK_SPACE and \
                grid_template[i][j] != FROGGER:
                    block_count += 1
        if current_block_count != block_count:
            return False
        else:
            return True
    else:
        return True

def win_condition(frog_pos, grid):
    """
    :param: the current position of the frog in a list
    :param: The grid the game takes place
    :return: True/False if the frog is at the last row
    """
    # Confirms that the frog has made it to the other side
    row_length = len(grid)
    frog_x = frog_pos[0]
    if frog_x == (row_length - 1):
        return True
    else:
        return False

def frogger_game(file):
    """
    :param: The game file the user wants to play.
    :return: If the frog has won the game, or got run over on the way there
    """
    road_crossed = False
    frog_lose = False
    main_file = open(file, 'r')
    rows = main_file.readlines()
    main_file.close()
    grid_info = list_breakdown(rows[0].split(" "))
    move_speed = list_breakdown(rows[1].split(" "))
    row_length = int(grid_info[0])
    col_length = int(grid_info[1])
    jumps = int(grid_info[2])
    rows = create_outer_rows(col_length, rows[2:])
    grid = make_grid(rows)
    grid_copy = make_grid(rows)
    turn_num = 1
    frogger_pos = [0, col_length//2]
    while road_crossed == False and frog_lose == False:
        print(turn_num) # While loop to simulate turns
        print_grid(grid, frogger_pos)
        next_move = input("WASDJ >> ").upper().strip()
        move_confirmed = False
        while move_confirmed == False: # Potential Moves
            if next_move == 'W' or next_move == 'A' or \
                next_move == 'S' or next_move == 'D':
                the_move = make_move(next_move, frogger_pos, grid)
                if the_move == False:
                    print("You cannot make this move. Try again.")
                    next_move = input("WASDJ >> ").upper().strip()
                else:
                    frogger_pos = the_move
                    move_confirmed = True
            elif 'J' in next_move:
                next_move = next_move.split(" ")[1:]
                the_jump = jump_space(frogger_pos, next_move, jumps, grid)
                if the_jump == False:
                    print("You cannot make this jump. Try again.")
                    next_move = input("WASDJ >> ").upper().strip()
                else:
                    frogger_pos = the_jump
                    jumps -= 1 # Uses a jump for limit
                    move_confirmed = True
            else:
                move_confirmed = True # Nothing happens
        shuffle_rows(frogger_pos, grid, move_speed)
        if check_collision(frogger_pos[0], grid, grid_copy) == False:
            frog_lose = True
        if win_condition(frogger_pos, grid) == True:
            road_crossed = True
        turn_num += 1
    if frog_lose == True:
        turn_num += 1
        print(turn_num) # Prints out the grid if the frog is run over
        for i in range(len(grid)):
            line = ''
            for j in range(len(grid[i])):
                line += grid[i][j]
            print(line)
        print("You lost. Sorry, Frogger.")
    elif road_crossed == True:
        turn_num += 1
        print(turn_num) # Prints out the grid if the frog made it to the end
        for i in range(len(grid)):
            line = ''
            for j in range(len(grid[i])):
                line += grid[i][j]
            print(line)
        print("You Win! Frogger gets to cross another day.")
if __name__ == '__main__':
    game_file = display_files()
    frogger_game(game_file)
