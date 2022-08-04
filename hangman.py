import random
from words import wordList,hangman

#to choose a random word from the given wordlist
def startgame():
    word = random.choice(wordList).lower()
    return word

def check(nextChar,gWord,guessedLetters,wrongGuess):
    if nextChar == "":
        return ("noinput","Enter any letter")
    elif wrongGuess == 7:
        return ("gameover","Game over")
    nextChar = nextChar.lower()
    if nextChar in guessedLetters:
        return ("invalid","Cannot guess the same letter again, change your guess")
    elif nextChar in gWord:
        word = ""
        for i in range(len(gWord)):
            if gWord[i] in guessedLetters:
                word += gWord[i] + ' '
            elif gWord[i]==nextChar:
                word += nextChar + ' '
            else:
                word += '_ '
        return ("correct",word)
    else:
        return ("wrong","Wrong Guess")
