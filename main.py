import json
import os
import sys
import random
import time


def game() -> None:
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    print("You have a lot of chances to guess the correct number.\n")
    while True:
        answer = random.randint(1, 100)
        print("Please select the difficulty level:")
        print("1. Easy (10 chances)")
        print("2. Medium (5 chances)")
        print("3. Hard (3 chances)\n")
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Please enter a number.")
            sys.exit(0)

        if choice == 1:
            max_chance = 10
            print("Great! You have selected the Easy difficulty level.")
        elif choice == 2:
            max_chance = 5
            print("Great! You have selected the Medium difficulty level.")
        elif choice == 3:
            max_chance = 3
            print("Great! You have selected the Hard difficulty level.")
        else:
            print("Please enter a number between 1 and 3.")
            continue
        print("Let's start the game!\n")

        current_chance = max_chance
        start_time = time.time()

        while True:
            try:
                guess = int(input("Enter your guess: "))
            except ValueError:
                print("Please enter a number.")
                continue

            if guess < answer:
                print(f"The number is greater than {guess}.")
            elif guess > answer:
                print(f"The number is less than {guess}.")
            elif guess == answer:
                print(f"Congratulations! You guessed the correct number in {max_chance-current_chance} attempts.")
                print(f"Your time is {time.time() - start_time} seconds.")
                record, new_record = new_result(max_chance-current_chance, str(choice))
                if new_record:
                    print(f"You have a new record! Now record on current difficult is {record}.")
                else:
                    print(f"Current record is {record}.")
                break
            current_chance -= 1
            if current_chance <= 0:
                print(f"You have no chances to guess the correct number. The correct number was {answer}.")
                print(f"You have lose.")
                break

        want_play = input("Do you want to play again? (y/n)\n")
        if want_play.lower() == "y" or want_play.lower() == "yes":
            continue
        else:
            print("Thank you for playing!")
            break



def new_result(new_result: int, difficult: str) -> (int, bool):
    record = False
    try:
        with open("data.json", "r") as f:
            result = json.load(f)
        if not result["best_result"][difficult] or new_result < result["best_result"][difficult]:
            result["best_result"][difficult] = new_result
            record = True
            with open("data.json", "w") as f:
                json.dump(result, f)
        return result["best_result"][difficult], record
    except Exception as e:
        print("Unexpected error:", sys.exc_info()[0])

def create_json() -> None:
    try:
        with open("data.json", 'w') as f:
            data = {
                "best_result": {
                    1: None,
                    2: None,
                    3: None,
                }
            }
            json.dump(data, f)
    except Exception as e:
        print("Unexpected error:", sys.exc_info()[0])


if __name__ == '__main__':
    if not os.path.isfile("data.json"):
        create_json()

    args = sys.argv[1:]

    if len(args) == 0 or args[0] == "help":
        print("Usage: python main.py [start|delete|help]")
        print("\tstart: starts the game")
        print("\tdelete: deletes the score data")
        print("\thelp: prints this help message")
    elif args[0] == "start":
        game()
    elif args[0] == "delete":
        create_json()
    else:
        print("Invalid command. Write 'help' to see available commands.")