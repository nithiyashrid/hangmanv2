import random
from words import wordList,hangman

#to choose a random word from the given wordlist
def startgame():
    word = random.choice(wordList).lower()
    return word

def check(nextChar,gWord,guessedLetters):
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

def play(word,notGuessed):
    guessedOverall = []
    guessedCorrect = []
    guessedWrong = []
    guessed = False
    print(hangman[0])
    incrementHangman = 1
    #until the hangman is built completely-guessing is allowed
    while incrementHangman<8:
        nextChar = input("Enter the guessed letter\t:\t")
        nextChar = nextChar.lower()

        while nextChar in guessedOverall:
            print("Cannot guess the same letter again, change your guess")
            nextChar = input("\nEnter the guessed letter\t:\t")
        guessedOverall.append(nextChar)

        if nextChar in word:
            print(hangman[incrementHangman])
            for i in range(len(word)):
                if word[i]==nextChar:
                    notGuessed[i] = nextChar
            print("Guessed word :-",notGuessed)
            guessedCorrect.append(nextChar)

        else:
            print(hangman[incrementHangman])
            print("\nWRONG Guess, Attempts left\t=\t",7-incrementHangman)
            incrementHangman += 1
            guessedWrong.append(nextChar)
        if notGuessed.count('_')==0:
            guessed = True
            break

    if guessed == True:
        return "You Win!"
    else:
        return "You loose :("
