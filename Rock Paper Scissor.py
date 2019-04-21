'''
Code by: Olivia J.Y Chan [2019-04-21]

This programs simulates a game of Rock Paper Scissor.
It consists of the following sections: Move enum, MatchResult enum, Player class, GameHistory class, Game Main body

Permission given to refer to the code, modify the code and copy the code for personal usage.
No permissions given for commercial purposes, not that I would expect anyone to do so. The code is fairly generic after all.
'''
from enum import Enum # To define an enum for the possible moves
import random # For the random move selection function

# Possible move set
class Move(Enum):
    Invalid = 0
    Rock = 1
    Paper = 2
    Scissor = 3

# Possible match results
class MatchResult(Enum):
    NoResult =0
    Tie=1
    Win =2
    Loss =3

# Player class: Each player has an unique number (could be UUID), a score, and move (memoryless)
class Player:
    def __init__(self,number):
        self.number = number 
        self.score = 0
        self.move = Move.Invalid

    # Adds to the player's existing score
    def addScore(self):
        self.score+=1

    # Reset the player's score
    def resetScore(self):
        self.score = 0

    # Defines the player's move
    def makesMove(self,move):
        self.move = move

    # Randomly assigns a move for the player
    def makeRandomMove(self):
        randomNumber = random.randint(1,3)
        self.move = Move(randomNumber)

    # Displays last move 
    # This is a Markov process: the player has no memory of the previous moves.
    def lastMove(self):
        print("Player %d played %s"%(self.number, self.move))

    def __str__(self):
     return ("Player %s with score of %s "%(self.number ,self.score))

# Class to keep track of total of matches played
# Can be edited to have a list/history log of wins (e.g. Match1, Player 1 Win)
# Assumes that a Tie gives no points to either players
class GameHistory:  
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.totalTie = 0
        self.totalGames = 0

    def addGameCount(self):
        self.totalGames +=1

    def addTieCount(self):
        self.totalTie +=1
        self.totalGames +=1

    def getTotalGames (self):
        return self.totalGames

    def resetHistory(self):
        self.player1.resetScore()
        self.player2.resetScore()
        self.totalTie =0
        self.totalGames = 0
    
    def __str__(self):
        return ("Total of %d games have been played."%(self.getTotalGames()))

# Returns whether player1 ties, loses or wins versus player2
def Match(player1, player2):
    result = MatchResult.NoResult
    #Check that both of the players did performed a valid move
    if player1.move == Move.Invalid or player2.move == Move.Invalid:
        raise Exception('One of the players performed an invalid move.') 
    
    # Check determine the result of the match
    # If this were Java, C++, C# or even the Wolfram Language, I would use a switch case
    # Another option was to use a dictionary, but given the numbers of conditions to check, it might not be readable.
    # If player1 plays Rock
    if player1.move == Move.Rock:
        if player2.move == Move.Rock: 
            return MatchResult.Tie
        elif player2.move == Move.Paper:
            return MatchResult.Loss
        elif player2.move == Move.Scissor:
            return MatchResult.Win 
    # If player1 plays Paper
    elif player1.move == Move.Paper:
        if player2.move == Move.Paper:
            return MatchResult.Tie
        elif player2.move == Move.Scissor:
            return MatchResult.Loss
        elif player2.move == Move.Rock:
            return MatchResult.Win
    # If player1 plays Scissor
    elif player1.move == Move.Scissor:
        if player2.move == Move.Scissor:
            return MatchResult.Tie
        elif player2.move == Move.Rock:
            return MatchResult.Loss
        elif player2.move == Move.Paper:
            return MatchResult.Win

    return result
            

'''
Game Starts
'''
def main():
    # Declare and initialize the players
    player1 = Player(1)
    player2 = Player(2)

    #Declare and initialize the Game History
    history = GameHistory(player1, player2)

    #Declare and initialize a boolean to tell the program whether to quit the game
    quit = False

    print("Welcome to Olivia Chan's simple Rock Paper Scissor Simulator")
    while not quit:
        try:
            print("Starting Match #%d : "%(history.totalGames+1))
            moveInput = input("Player 1, please pick a move from : \n1. Rock \n2. Paper \n3. Scissor \n")

            # Assumes the user is always Player1 and always perfect
            # Randomly make a move for Player2 (the computer!)
            player1.move = Move(int(moveInput))
            player2.makeRandomMove()

            match = Match(player1,player2)
        
            # Update history and scores
            if match == MatchResult.Tie:
                history.addTieCount()
            elif match == MatchResult.Loss:
                history.addGameCount()
                player2.addScore()
            elif match == MatchResult.Win:
                history.addGameCount()
                player1.addScore()
            
            # Print an empty line, for formating (this is a poor formatting decision:: to be improved)
            print()
            player1.lastMove() # Print player last moves
            player2.lastMove()
            print(player1) # Print player status
            print(player2)
            print("Numbers of Tie: %d"%(history.totalTie)) # Print total ties
            print(history) #Print current game status

            continueGame = input("Do you want to continue playing? (Y/N) ")
            print() #Printing another empty line for formatting! Help me! (TT^TT)

            if continueGame.capitalize() =='N':
                print("Thank you for playing! ")
                quit = True
            elif continueGame.capitalize() != 'Y':
                print("You gave an invalid response. Program will terminate. Thank you for playing.")
                quit = True              

        except Exception:
            print("An error occured. Exiting Program.")
            quit = True
    
if __name__ == '__main__':
    main()
