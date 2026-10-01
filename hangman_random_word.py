import argparse
import random
import getpass
import sys

parser = argparse.ArgumentParser()
parser.add_argument("filename", nargs="?")
parser.add_argument("--penalties", type=int, default=12)
parser.add_argument("--two-player", action="store_true")

args = parser.parse_args()

if args.two_player:
    word = getpass.getpass("Player 1, enter a secret word: ").lower()
else:
    if args.filename is None:
        print("Error: missing argument", file=sys.stderr)
        exit(1)

    words = []

    try:
        with open(args.filename, "r") as file:
            for line in file:
                word = line.strip()   

                if not word or " " in word:
                    print("Error: invalid file format", file=sys.stderr)
                    sys.exit(1)
                    # exit(0): 程式正常結束(成功完成)
                    # exit(1): 程式發生錯誤結束
                words.append(word)

    except FileNotFoundError:
        print("Error: file not found", file=sys.stderr)
        sys.exit(1)

    if len(words) == 0:
        print("Error: empty file", file=sys.stderr)   # stderr: standard error
        sys.exit(1)

    word = random.choice(words)

hidden_word = ["-"] * len(word)

penalty = 0
guessed_letters = []

while penalty < args.penalties:
    print(" ".join(hidden_word), "/", penalty, "penalties")
    print("guessed letters:", " ".join(guessed_letters))
    guess = input("$> ").lower()

    if guess == "hint":
        hidden_letters = []     # 還沒被猜出的

        for i in range(len(word)):
            if hidden_word[i] == "-":
                hidden_letters.append(word[i])

        hint_letter = random.choice(hidden_letters)

        for i in range(len(word)):
            if word[i] == hint_letter:
                hidden_word[i] = hint_letter

        penalty += 2
        print("hint:", hint_letter)

    elif len(guess) == 1:
        guessed_letters.append(guess)

        if guess in word:
            found = 0
            for i in range(len(word)):
                if word[i] == guess:
                    hidden_word[i] = guess
                    found += 1
            print("found:", guess)

        else:
            print("no", guess)
            penalty += 1

    else:
        if guess == word:
            print("you win!")
            break
        else:
            print(guess, "incorrect")
            penalty += 5

    if "-" not in hidden_word:
        print("you win!")
        break

    if penalty >= args.penalties:
        print("you lose!")
        print("the correct answer is", word)
