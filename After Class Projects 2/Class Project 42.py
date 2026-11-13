import numpy as np


def main() -> None:
    numbers = np.array([10, 20, 30, 40, 50])
    other_numbers = np.array([1, 2, 3, 4, 5])

    print("Original array:", numbers)
    print("Add 5 to every element:", numbers + 5)
    print("Multiply every element by 2:", numbers * 2)
    print("Add the arrays element by element:", numbers + other_numbers)
    print("First element:", numbers[0])
    print("First three elements:", numbers[:3])
    print("Sum:", np.sum(numbers))
    print("Average:", np.mean(numbers))
    print("Elements greater than 25:", numbers[numbers > 25])


if __name__ == "__main__":
    main()