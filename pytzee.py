"""
    File: pytzee.py
    Author: Gabriel Gyaase
    Date: 10/16/2024
    Section: 10
    E-mail: ggyaase1@umbc.edu
    Description: This file simulates a game
                 of the board game Yahtzee
                 redubbed "Pytzee", that allows
                 the user to gain points based on
                 the rolls in a specified amount of
                 turns. The possible ways to gain
                 points include counting any number
                 from 1 to 6, a three of a kind, 
                 a four of a kind, a full house, 
                 a small straight, a large straight,
                 a pytzee, and chance. With the
                 expection of pytzee, each type of
                 count can be used once, but the
                 user can skip turns if they can't
                 use anything on the current roll.
                 Once the rounds are over, the final
                 score is added up, and bonus points
                 are given if it is 63 or more.
    # Given Score: 56/90
"""

import random

TOTAL_DICE = 5
DICE_FACES = 6
SKIP_PHRASE = 'skip'

def roll_dice():
    """
    :return: a list containing five integers representing dice rolls 
    between 1 and 6.
    """
    roll_list = []
    for i in range(TOTAL_DICE):
        roll_list.append(random.randint(1, 6))
    return roll_list

def show_scorecard(count_list, special_count_list):
    """
    :return: a line of strings that shows the user's current score for each
    type of score.
    """
    types_list = ["Three of a Kind", "Four of a Kind", "Full House", \
                  "Small Straight", "Large Straight", "Pytzee", "Chance"]
    # Row 1: 1's 2's 3's 4's ...
    print("1's\t2's\t3's\t4's\t5's\t6's")
    # Row 2: Points for each number
    for i in range(len(count_list)):
        count_list[i] = str(count_list[i])
    print('\t'.join(count_list))
    # Row 3: Three of a Kind, Four of a Kind, etc.
    print('  '.join(types_list))
    # Row 4: Points for each special roll (The spaces are intentional)
    print(f"             {special_count_list[0]}     \
          {special_count_list[1]}           {special_count_list[2]}     \
          {special_count_list[3]}       \
        {special_count_list[4]}\
        {special_count_list[5]}      {special_count_list[6]}")
    # Turns lists back into ints
    for i in range(len(count_list)):
        count_list[i] = int(count_list[i])
    for i in range(len(special_count_list)):
        special_count_list[i] = int(special_count_list[i])

def ask_count(score, dice_roll): # Asks the user what kind of count the user wants
    """
    :param: The total score and the dice roll list
    :return: The score, with whatever applied count the user selects, if
    possible
    """
    question = input("How do you want to count it? ").strip().lower()
    accepted_count = False
    while accepted_count != True:
        if 'count' in question:
            if '1' in question and 1 in dice_roll: # Count 1's
                if count_list[0] == 0:
                        print("Accepted the 1.")
                        apply_count('count', 1, score, dice_roll)
                        accepted_count = True
                else:
                    print("You have already used your count for 1. Try again.")
                    question = \
                        input("How do you want to count it? ").strip().lower()
            elif '2' in question and 2 in dice_roll: # Count 2's
                if count_list[1] == 0:
                    print("Accepted the 2.")
                    apply_count('count', 2, score, dice_roll)
                    accepted_count = True
                else:
                    print("You have already used your count for 2. Try again.")
                    question = \
                    input("How do you want to count it? ").strip().lower()
            elif '3' in question and 3 in dice_roll: # Count 3's
                if count_list[2] == 0:
                    print("Accepted the 3.")
                    apply_count('count', 3, score, dice_roll)
                    accepted_count = True
                else:
                    print("You have already used your count for 3. Try again.")
                    question = \
                        input("How do you want to count it? ").strip().lower()
            elif '4' in question and 4 in dice_roll: # Count 4's
                if count_list[3] == 0:
                    print("Accepted the 4.")
                    apply_count('count', 4, score, dice_roll)
                    accepted_count = True
                else:
                    print("You have already used your count for 4. Try again.")
                    question = \
                        input("How do you want to count it? ").strip().lower()
            elif '5' in question and 5 in dice_roll: # Count 5's
                if count_list[4] == 0:
                    print("Accepted the 5.")
                    apply_count('count', 5, score, dice_roll)
                    accepted_count = True
                else:
                    print("You have already used your count for 5. Try again.")
                    question = \
                        input("How do you want to count it? ").strip().lower()
            elif '6' in question and 6 in dice_roll: # Count 6's
                if count_list[5] == 0:
                    print("Accepted the 6.")
                    apply_count('count', 6, score, dice_roll)
                    accepted_count = True
                else:
                    print("You have already used your count for 6. Try again.")
                    question = \
                        input("How do you want to count it? ").strip().lower()
        elif 'of a kind' in question:
            if ('3' in question or 'three' in question): # Three of a Kind
                if (check_of_a_kind(dice_roll, 3) == True) and \
                    special_count_list[0] == 0:
                    print('Three of a Kind!')
                    apply_count('kind', 3, score, dice_roll)
                    accepted_count = True
                else:
                    print("Three of a Kind is not possible. Try again.")
                    question = \
                        input("How do you want to count it? ").strip().lower()
            elif ('4' in question or 'four' in question): # Four of a Kind
                if check_of_a_kind(dice_roll, 4) == True and \
                    special_count_list[1] == 0:
                    print('Four of a Kind!')
                    apply_count('kind', 4, score, dice_roll)
                    accepted_count = True
                else:
                    print('Four of a Kind is not possible. Try again.')
                    question = \
                        input("How do you want to count it? ").strip().lower()
        elif 'full house' in question: # Full House (NOT WORKING)
            num_count = [0, 0, 0, 0, 0, 0]
            rolls = [1, 2, 3, 4, 5, 6]
            for i in range(len(dice_roll)):
                for j in range(len(rolls)):
                    if int(dice_roll[i]) == int(rolls[j]):
                        num_count[j] += 1
            if special_count_list[2] == 0 and (3 in num_count) and \
                (2 in num_count):
                print("Full House! +25 points!")
                score += 25
                special_count_list[2] += 25
                accepted_count = True
            else:
                print('A full house is not possible. Try again.')
                question = \
                    input("How do you want to count it? ").strip().lower()
        elif 'small straight' in question: 
            # Small Straight
            if special_count_list[3] == 0:
                if (1 in dice_roll and 2 in dice_roll and 3 in dice_roll and \
                    4 in dice_roll) or (2 in dice_roll and 3 in dice_roll and \
                    4 in dice_roll and 5 in dice_roll) or (3 in dice_roll and \
                    4 in dice_roll and 5 in dice_roll and 6 in dice_roll):
                    print("Small Straight! +30 points!")
                    score += 30
                    special_count_list[3] += 30
                    accepted_count = True
            else:
                print("A small straight is not possible. Try again.")
                question = \
                    input("How do you want to count it? ").strip().lower()
        elif 'large straight' in question: 
            # Large Straight
            if special_count_list[4] == 0:
                if (1 in dice_roll and 2 in dice_roll and 3 in dice_roll and \
                    4 in dice_roll and 5 in dice_roll) or (2 in dice_roll and \
                    3 in dice_roll and 4 in dice_roll and 5 in dice_roll and \
                    6 in dice_roll):
                    print("Large Straight! +40 points!")
                    score += 40
                    special_count_list[4] += 40
                    accepted_count = True
                else:
                    print('A large straight is not possible. Try again.')
                    question = \
                        input("How do you want to count it? ").strip().lower()
            else:
                print("A large straight is not possible. Try again.")
                question = \
                    input("How do you want to count it? ").strip().lower()
        elif 'pytzee' in question: # Yahtzee/Pytzee
            possible = False
            for i in range(len(dice_roll)): # Checks if any number is equal to 
                # every die
                if (i + 1) == dice_roll[0] and (i + 1) == dice_roll[1] and \
                (i + 1) == dice_roll[2] and (i + 1) == dice_roll[3] and \
                (i + 1) == dice_roll[4]:
                    possible = True
            if possible == True:
                if special_count_list[5] == 0:
                    print("Pytzee! +50 points!")
                    score += 50
                    special_count_list[5] += 50
                    accepted_count = True
                else:
                    print("Pytzee! (Multiple Pytzee Bonus) +100 points!")
                    score += 100
                    special_count_list[5] += 100
                    accepted_count = True
            else:
                print("A Phyztee is not possible. Try again.")
                question = \
                    input("How do you want to count it? ").strip().lower()
        elif 'chance' in question:
            if special_count_list[6] == 0:
                for i in range(len(dice_roll)):
                    score += dice_roll[i]
                    special_count_list[6] += dice_roll[i]
                accepted_count = True
            else:
                print('Chance is not possible. Try again.')
                question = \
                    input("How do you want to count it? ").strip().lower()
        elif SKIP_PHRASE in question:
            print("Roll skipped.")
            accepted_count = True
        else:
            print("That count is not possible. Please try again.")
            question = \
                    input("How do you want to count it? ").strip().lower()

def check_of_a_kind(dice_roll, num):
    """
    :param: the dice roll and the number in a row (three or four)
    :return: A true/false that confirms there is or is not that number of the
    same number in a row.
    """
    if num == 3:
        # Checks all possible combinations for three of one side of die
        for i in range(len(dice_roll)):
            for j in range(len(dice_roll)):
                for k in range(len(dice_roll)):
                    if (dice_roll[i] == dice_roll[j] and i != j) and \
                        (dice_roll[i] == dice_roll[k] and i != k) and (j != k):
                        return True
        return False
    elif num == 4: 
        # Checks all possible combinations if there is four of one type of die
        for i in range(len(dice_roll)):
            for j in range(len(dice_roll)):
                for k in range(len(dice_roll)):
                    for l in range(len(dice_roll)):
                        if (dice_roll[i] == dice_roll[j] and i != j) and \
                            (dice_roll[i] == dice_roll[k] and i != k) and \
                                (dice_roll[i] == dice_roll[l] and i != l) and \
                                    (j != k) and (j != l) and (k != l):
                            return True
        return False

def apply_count(type, num, score, dice_roll):
    """
    :param: The type of count the user wants, the corresponing number,
    the current score and the dice roll list
    :return: Adds the score to the corresponding points.
    """
    if type == 'kind': # Scores three of a kind and four of a kind (adds all)
        for i in range(len(dice_roll)):
            score += dice_roll[i]
            special_count_list[num - 3] += dice_roll[i]
    elif type == 'count': # Takes all counts of a number and adds it.
        multiplier = 0
        for i in range(len(dice_roll)):
            if dice_roll[i] == num:
                multiplier += 1
        score += (multiplier * num)
        count_list[num - 1] += (multiplier) * num

def play_game(num_rounds): # Starts the Game of Yahtzee based on turn amount.
    """
    :param: The number of rounds in the game the user wants to play.
    :return: The final score for the game.
    """
    score = 0
    for i in range(num_rounds):
        print(f'***** Beginning Round {i + 1} *****')
        if i > 0:
            print(f'Your score is {score}.')
        dice_roll = roll_dice()
        print(dice_roll)
        ask_count(score, dice_roll)
        show_scorecard(count_list, special_count_list)
        score = sum(count_list) + sum(special_count_list)
    if score >= 63:
        print("High Score Bonus! +35 points!")
        score += 35
    return score

if __name__ == '__main__':
    count_list = [0, 0, 0, 0, 0, 0]
    special_count_list = [0, 0, 0, 0, 0, 0, 0]
    num_rounds = \
        int(input('What is the number of rounds that you want to play? '))
    seed = int(input('Enter the seed or 0 to use a random seed: '))
    if seed:
        random.seed(seed)
    end_score = play_game(num_rounds)
    print(f"Your final score is {end_score}.")
