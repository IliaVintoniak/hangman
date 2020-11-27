# Problem Set 2, hangman.py
# Name: Illia Vintoniak KM-03
# Collaborators: none
# Time spent: 3 days

# Hangman Game

import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

wordlist = load_words()

def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    wordg_1 = set(secret_word)
    wordg_2 = set(letters_guessed)
    if (wordg_1 & wordg_2) == wordg_1:
        return True
    else:
        return False


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    q = ''
    for i in range(len(secret_word)):
        try:
            letters_guessed.index(secret_word[i])
        except ValueError:
            q += '_ '
        else:
            q += secret_word[i]
            continue
    return q


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    a = ''
    for i in range(len(string.ascii_lowercase)):
        try:
            letters_guessed.index(string.ascii_lowercase[i])
        except ValueError:
            a += string.ascii_lowercase[i]
        else:
            continue
    return a


def hangman(secret_word):
    """
    secret_word: string, the secret word to guess.
    Starts up an interactive game of Hangman.
    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.
    * The user should start with 6 guesses
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.
    * After each guess, you should display to the user the
      partially guessed word so far.
    Follows the other limitations detailed in the problem write-up.
    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    warnings_num = 3
    guesses_num = 6
    letters_guessed = []
    inputed_letter = set()

    print(f'Welcome to the Hangman!\nI am thinking of a word that is {len(secret_word)} letters long.')
    print(f'You have {warnings_num} warnings left.')

    while guesses_num > 0 and not is_word_guessed(secret_word, letters_guessed):
        print('- * 100')
        print(f'you have {guesses_num} guesses left.\n'
              f'available letters: {get_available_letters(letters_guessed)}')
        letter = input('please guess a letter: ').lower()

        if letter not in list(string.ascii_lowercase):
            if warnings_num > 0:
                warnings_num -= 1
            else:
                guesses_num -= 1
            print(f"Oops! That's not a valid letter. You have {warnings_num} "
                  f'warnings left: {get_guessed_word(secret_word, letters_guessed)}')
        else:
            if letter in inputed_letter:
                if warnings_num > 0:
                    warnings_num -= 1
                else:
                    guesses_num -= 1
                print(f"Oops! You've already guessed that letter. You have {warnings_num} warnings left: "
                      f"{get_guessed_word(secret_word, letters_guessed)}")
            elif letter in secret_word:
                letters_guessed.append(letter)
                print(f'Good guess: {get_guessed_word(secret_word, letters_guessed)}')
            else:
                guesses_num -= 2 if letter in 'aeiou' else 1
                print(f'Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}')
            inputed_letter.add(letter)

    print('-' * 100)
    if is_word_guessed(secret_word, letters_guessed):
        game_score = guesses_num * len(set(list(secret_word)))
        print(f'congrats, you won!\nYour total score for this game is:{game_score}')
    else:
        print(f'sorry, you ran out of guesses. The word was {secret_word}')

def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    my_word = "".join(my_word.split(" "))
    if len(my_word)!=len(other_word):
        return False
    else:
        for i in range(len(other_word)):
            if my_word[i] == other_word[i] or my_word[i] == "_":
                continue
            else:
                return False
        return True

def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.
    '''
    matches = [word for word in wordlist if match_with_gaps(my_word, word) == True]
    if not matches:
        print("No matches found.\n")
    else:
        print("Possible word matches: " + ", ".join(matches), end="." + "\n")
    return

def hangman_with_hints(secret_word):
    """
    secret_word: string, the secret word to guess.
    Starts up an interactive game of Hangman.
    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.
    * The user should start with 6 guesses
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.
    * After each guess, you should display to the user the
      partially guessed word so far.
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.
    Follows the other limitations detailed in the problem write-up.
    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    warnings_num = 3
    guesses_num = 6
    letters_guessed = []
    inputed_letter = set()

    print(f'welcome to the Hangman!\nI am thinking of a word that is {len(secret_word)} letters long.')
    print(f'you have {warnings_num} warnings and {guesses_num} guesses left')

    while guesses_num > 0 and not is_word_guessed(secret_word, letters_guessed):
        print('-' * 100)
        print(f'you have {guesses_num} guesses left.\n'f'Available letters: {get_available_letters(letters_guessed)}')
        letter = input('Please guess a letter: ').lower()

        if letter == '*':
            p_words = show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            print(p_words)

        elif letter not in list(string.ascii_lowercase):
            if warnings_num > 0:
                warnings_num -= 1
            else:
                guesses_num -= 1
            print(f'oops! That is not a valid letter. You have {warnings_num} ')
            print(f'warnings left: {get_guessed_word(secret_word, letters_guessed)}')
        else:
            if letter in inputed_letter:
                if warnings_num > 0:
                    warnings_num -= 1
                else:
                    warnings_num -= 1
                print(f"oops! You've already guessed that letter. You have {warnings_num} warnings left: "
                      f"{get_guessed_word(secret_word, letters_guessed)}")
            elif letter in secret_word:
                letters_guessed.append(letter)
                print(f'good guess: {get_guessed_word(secret_word, letters_guessed)}')
            else:
                print(f'oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}')
                guesses_num -= 2 if letter in 'aeiou' else 1
            inputed_letter.add(letter)

    print('-' * 120)
    if is_word_guessed(secret_word, letters_guessed):
        game_score = guesses_num * len(set(list(secret_word)))
        print(f'congrats, you won!\nYour total score for this game is:{game_score}')
    else:
        print(f'sorry, you ran out of guesses. The word was:{secret_word}')

if __name__ == "__main__":


    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    secret_word = choose_word(wordlist)
    hangman(secret_word)

###############

    # To test part 3 re-comment out the above lines and
    # uncomment the following two lines.
    #secret_word = choose_word(wordlist)
    #hangman_with_hints(secret_word)
