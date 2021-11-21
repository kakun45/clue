import clue
from clue.scoresheet import Scoresheet


if __name__ == "__main__":
    data = Scoresheet(["Dave", "Olivia", "Xeniya"])
    #data = Scoresheet([1, 2, 3])
    print(data.is_valid())