import random
difficulty = input("Choose a difficulty level (easy, medium, hard): ").lower()
highest_number = 0
if difficulty == "easy":
    highest_number = 10
    random_number = random.randint(0, highest_number)
    lives = 3
elif difficulty == "medium":
    highest_number = 25
    random_number = random.randint(0, highest_number)
    lives = 5
else:
    highest_number = 50
    random_number = random.randint(0, highest_number)
    lives = 7

guess = input("Guess a number between 0 and " + str(highest_number) + ": ")
while lives > 0:
    if guess.isdigit():
        guess = int(guess)
        print("You guessed:", guess, "and the random number is:", random_number)
        if guess == random_number:
            print("Congratulations! You guessed correctly.")
            break
        else:
            print("Sorry, that's not the correct number.")
            lives -= 1
    else:
        print("Please enter a valid number.")
        break
else:
        print("Sorry, that's not the correct number.")