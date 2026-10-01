import sys
import random

if len(sys.argv) < 2:
    print("Error: missing argument", file=sys.stderr)
    sys.exit(1)

filename = sys.argv[1]
words = []

try:
    with open(filename, "r") as file:
        for line in file:
            word = line.strip()    # remove "\n"

            if not word or " " in word:
                print("Error: invalid file format")
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

secret_word = random.choice(words)

print(secret_word)