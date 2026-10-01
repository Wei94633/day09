import argparse
import random
import getpass
import sys
from datetime import date
from game_ui import PygameUI

parser = argparse.ArgumentParser()
parser.add_argument("filename", nargs="?")
parser.add_argument("--penalties", type=int, default=12)
parser.add_argument("--two-player", action="store_true")
args = parser.parse_args()


def play_round(args, ui):
    ui.reset()
    print = ui.print
    if args.two_player:
        word = getpass.getpass("Player 1, enter a secret word: ").lower()
    else:
        if args.filename is None:
            print("Error: missing argument", file=sys.stderr)
            sys.exit(1)

        words = []

        try:
            with open(args.filename, "r") as file:
                for line in file:
                    word = line.strip()

                    if not word or " " in word:
                        print("Error: invalid file format", file=sys.stderr)
                        sys.exit(1)


                    words.append(word)

        except FileNotFoundError:
            print("Error: file not found", file=sys.stderr)
            sys.exit(1)

        if len(words) == 0:
            print("Error: empty file", file=sys.stderr)
            sys.exit(1)

        word = random.choice(words)

    hidden_word = ["-"] * len(word)

    penalty = 0
    attempts = 0
    guessed_letters = []

    best_attempts = None
    best_date = None

    try:
        with open("highscore.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")

                record_date = parts[0]
                record_attempts = int(parts[1])

                if best_attempts is None or record_attempts < best_attempts:
                    best_attempts = record_attempts
                    best_date = record_date

    except FileNotFoundError:
        pass

    while penalty < args.penalties:
        print(" ".join(hidden_word), "/", penalty, "penalties")
        print("guessed letters:", " ".join(guessed_letters))
        guess = ui.input("$> ", locals()).lower()
        attempts += 1

        if guess == "hint":
            hidden_letters = []

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
                today = date.today()
                if best_attempts is None or attempts < best_attempts:
                    with open("highscore.txt", "a") as file:
                        file.write(f"{today},{attempts}\n")

                    print(f"Best ever! You guessed '{word}' in {attempts} attempts.")

                else:
                    print(
                        f"You guessed '{word}' in {attempts} attempts, "
                        f"but the record from {best_date} is {best_attempts} attempts."
                )

                break
            else:
                print(guess, "incorrect")
                penalty += 5

        if "-" not in hidden_word:
            today = date.today()
            if best_attempts is None or attempts < best_attempts:
                with open("highscore.txt", "a") as file:
                    file.write(f"{today},{attempts}\n")

                print(f"Best ever! You guessed '{word}' in {attempts} attempts.")

            else:
                print(
                    f"You guessed '{word}' in {attempts} attempts, "
                    f"but the record from {best_date} is {best_attempts} attempts."
            )

            break

        if penalty >= args.penalties:
            print("you lose!")
            print("the correct answer is", word)

    return ui.finish(locals())


if __name__ == '__main__':
    ui = PygameUI()
    while play_round(args, ui):
        pass
