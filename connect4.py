#importing libraries
import time #required for piece falling animation
import os   #required for clearing console

def start(empty): #prints game ui at start
    print("\nC O N N E C T     4") 
    print("-------------------") 
    instructions() 
    print("-------------------") 
    users = get_users(empty) 
    players = users[0] 
    tokens = users[1] 
    print("-------------------")   
    print("-------------------") 
    return players, tokens

def get_users(empty): #gets and returns the names and tokens of players

    valid = 0 
    while not valid: 
        try:
            print("Player names or pieces may not be identical, empty, or equal to:", empty)
            print("Player names are limited to 16 characters and cannot contain colons (:) or commas (,)")
            print("Player pieces are limited to 1 character")
            print("-------------------") 
            player_1 = input("Player 1, enter your name:    ").strip()[:16]
            token_1 = input(f"{player_1}, enter your piece:    ").strip()[0] 
            print("-------------------") 
            player_2 = input("Player 2, enter your name:    ").strip()[:16]
            token_2 = input(f"{player_2}, enter your piece:    ").strip()[0]
            if player_1 == player_2 or token_1 == token_2 or not player_1 or not player_2 or not token_1 or not token_2 or empty == token_1 or empty == token_2 or ':' in player_1 or ',' in player_1 or ':' in player_2 or ',' in player_2: 
                print("-------------------") 
                print(f"Names and Pieces can not be identical or empty\nPlayer pieces can not be {empty}\nPlayer names cannot contain colons or commas\nTry again")
            
            else:
                print(f"\n{player_1}'s piece: {token_1}\n{player_2}'s piece: {token_2}") 
                valid = 1
        except IndexError:
            print('Player names and pieces can not be empty') 
            
    

    return [[player_1, player_2], [token_1, token_2]]

def instructions(): #prints the instructions at the start of the game
    print("Each turn the player will enter the column number in which to place their piece") 
    print("Turns alternate between player 1 and 2") 
    print("Under the board the column numbers are displayed") 
    print("When 4 pieces of the same player are connected in a row, the game ends and that player wins") 

def printboard(the_board): #prints the game board
    os.system('cls' if os.name == 'nt' else 'clear') #clears previously printed board before reprinting the board
    print("\n\nC O N N E C T     4") 
    print("-------------------") 

    for row in the_board: 
        for column in row: 
            print(column, end='  ') 
        print("")

    print("-------------------")
    print("1  2  3  4  5  6  7") 
    print("-------------------")

def check_full(the_board, empty): #checks if the game board is full
    full = 1 
    for row in the_board: 
        for piece in row: 
            if piece == empty: 
                full = 0 
    return full

def check_input(): #checks and ensures that the input provided by the user is valid
    check = 0 
    while not check: 
        print("")
        value = input("Enter Column Number:    ").strip() 
        if value.isdigit(): 
            if 1 <= int(value) <= 7: 
                check = 1 
        if not check: 
            print("Column must be a number between 1 and 7 inclusive") 
    print("") 
    return int(value)

def insert_piece(board, target_column, tokens, turn, empty): #inserts the piece into the column selected by the user
    found = 0
    inserted = 0 
    target_column -= 1 
    for current_row in range(5, -1, -1): 
        if board[current_row][target_column] == empty: #finds first empty slot from the bottom
            target_row = current_row
            found = 1 
            break #exits the loop once position found

    #falling piece animation
    if found:
        for this_row in range(target_row+1):

            board[this_row][target_column] = tokens[turn]

            if this_row != target_row:

                printboard(board)
                print("Please wait....")

                time.sleep(0.15)

                board[this_row][target_column] = empty
        inserted = 1

    else:
        print("Column is full")

    return inserted, board

def taketurn(board, players, turn, tokens, won, turn_counter, empty_character): #checks if the game can continue and lets the next player take turn

    current_player = players[turn]  
    if not check_full(board, empty_character):
        print("Current player:", current_player) 

        added = 0 
        while not added: 
            insert_column = check_input() 
            if insert_piece(board, insert_column, tokens, turn, empty_character)[0]: 
                added = 1 
        won = check_win(board, players, tokens, turn, turn_counter) 

        if turn == 0: # turn alternates between 0 and 1 for player 1 and 2 respectively
            turn = 1
        else:
            turn = 0
        turn_counter += 1 #increment turn counter for scoring

    else:
        #if board is full
        print("B O A R D    F U L L")
        print("G A M E    D R A W N")
        print("S K I L L  I S S U E")
        won = 1

    return turn, won, turn_counter

def check_win(board, players, tokens, turn, turn_counter): #conducts checks on the board to see if any winning criteria has been met, and assigns score to the winning player
    won, winner = horizontal_check(board, players, tokens, turn) 
    if not won: 
        won, winner = vertical_check(board, players, tokens, turn) 
    if not won: 
        won, winner = diagonalLR_check(board, players, tokens, turn) 
    if not won: 
        won, winner = diagonalRL_check(board, players, tokens, turn) 

    #score calculation    
    if won: 
        printboard(board) 
        print(f'{winner} IS THE WINNER!!!!\n')
        score = 1120 - (turn_counter//2)*40 #maximim score is 1000; score reduced by 40 points for each turn taken
        print("Score:")
        print(f'{winner} : {score}')
        update_scores(winner, score)

    return won

def horizontal_check(board, players, tokens, turn): #checks horizontally for any winning case
    for row in board: 
        for col in range(0, 4): 
            if row[col] == tokens[turn] and row[col] == row[col +1] == row[col +2] == row[col +3]: 
                return True, players[turn]
    return False, None

def vertical_check(board, players, tokens, turn): #checks vertically for any winning case
    for column in range(0, 7): 
        for row in range(0, 3):
            if board[row][column] == tokens[turn] and board[row][column] == board[row +1][column] == board[row +2][column] == board[row +3][column]: 
                return True, players[turn]
    return False, None


def diagonalLR_check(board, players, tokens, turn): #checks diagonally from left bottom to right top for any winning case
    for row in range(3, 6): 
        for col in range(0, 4): 
            if board[row][col] == tokens[turn] and board[row][col] == board[row -1][col +1] == board[row -2][col +2] == board[row -3][col +3]: 
                return True, players[turn]
    return False, None

def diagonalRL_check(board, players, tokens, turn): #checks diagonally from left top to right bottom for any winning case
    for row in range(0, 3): 
        for column in range(0, 4): 
            if board[row][column] == tokens[turn] and board[row][column] == board[row +1][column +1] == board[row +2][column +2] == board[row +3][column +3]: 
                return True, players[turn]
    return False, None

def update_scores(winner, score): #updates scores to the scores file

    #scores are saved like this {Ayan:1000},
    try:
        scores_file = open('High_Scores.txt', 'r+') #opens file for read and write (pointer at start)
        content = scores_file.read().strip()
        player_scores = [i.split(':') for i in content.split(',')] if content else []

        player_scores.append([winner, score])
        player_scores.sort(key=lambda x: int(x[1]), reverse=True)

        scores_file.truncate(0) #shortening the file to 0 bytes (emptying it)
        scores_file.seek(0) #moving pointer to start

        entries = [] #list to store scores
        for entry in player_scores:
            entries.append(f"{entry[0]}:{entry[1]}")
        #join to avoid leading or trailing commas
        scores_file.write(','.join(entries)) #all scores are joined by commas then written to the file
        scores_file.close()

    except FileNotFoundError: #if file does not exist
        with open("High_Scores.txt", 'w') as player_scores_file: #create text file
            player_scores_file.write(f"{winner}:{score}")

def print_scores(): #retrieves and prints the high scores of players
    try:
        scores_file = open('High_Scores.txt', 'r')  
        content = scores_file.read().strip()
        scores_file.close()        
        
        if not content:
            print("\nHigh Scores: No scores recorded yet.")
            return

        high_scores = [i.split(':') for i in content.split(',')] #create a 2d list with each item of the list being [player, score]
        print("\nHigh Scores:")
        print('')
        print(f'{"Player":16}{"Score":5}')
        print('-'*21)
        for i in high_scores:
            print(f'{i[0]:16}{i[1]:>4}')
            
    except FileNotFoundError:
        print("\nHigh Scores: No scores recorded yet.")     

def continue_play(): #asks the players if they want to keep playing when a game ends
    keep_playing = 0
    while keep_playing != 'Y' and keep_playing != 'N':
        try:
            keep_playing = (input("Replay ?\nEnter yes (Y) or no (N)   ").upper())[0] #take first character of input
        except IndexError: #taking first character of an empty string causes indexerror
            print('Please provide an input!!!')
            
    return keep_playing

if __name__ == '__main__': #main loop of the game 
    keep_playing = 1
    while keep_playing != 'N':
        #initializing variables
        empty_character = '|'
        board = [[empty_character] * 7 for i in range(6)] 
        players, tokens = start(empty_character) 
        turn = 0 
        turn_counter = 0
        won = False 

        while not won: 
            printboard(board) 
            turn, won, turn_counter = taketurn(board, players, turn, tokens, won, turn_counter, empty_character)
        #when game over    
        keep_playing = continue_play()

    print_scores()
    print("\nG O O D B Y E !")
