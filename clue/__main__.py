import clue
from clue import HAS_CARD, DOESNT_HAVE_CARD
from clue.scoresheet import Scoresheet


if __name__ == "__main__":
    data = Scoresheet(["Dave", "Olivia", "Xeniya"])
    #data = Scoresheet([1, 2, 3])
    print(data)

    data.set_ownership("Dave", clue.MUSTARD, HAS_CARD)
    data.set_ownership("Dave", clue.GREEN, HAS_CARD)
    data.set_ownership("Dave", clue.SCARLET, HAS_CARD)
    data.set_ownership("Dave", clue.PLUM, HAS_CARD)
    data.set_ownership("Dave", clue.GRAY, HAS_CARD)
    data.set_ownership("Dave", clue.PEACH, HAS_CARD)
    data.set_ownership("Xeniya", clue.MUSTARD, DOESNT_HAVE_CARD)
    data.set_ownership("Xeniya", clue.GREEN, DOESNT_HAVE_CARD)
    data.set_ownership("Xeniya", clue.SCARLET, DOESNT_HAVE_CARD)
    data.set_ownership("Xeniya", clue.PLUM, DOESNT_HAVE_CARD)
    data.set_ownership("Xeniya", clue.GRAY, DOESNT_HAVE_CARD)
    data.set_ownership("Xeniya", clue.PEACH, DOESNT_HAVE_CARD)
    data.set_ownership("Olivia", clue.PEACOCK, DOESNT_HAVE_CARD)

    for s in ["Dave", "Xeniya", "Olivia"]:
        data.set_ownership(s, clue.KNIFE, DOESNT_HAVE_CARD)

    data.print_scoresheet()
    # r = clue.pad_right("hello", 8)
    # print(f"|{r}|")
