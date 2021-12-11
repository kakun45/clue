import clue
from clue import HAS_CARD, DOESNT_HAVE_CARD
from clue.scoresheet import Scoresheet
import clue.repl

def printing_test():
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


if __name__ == "__main__":

    players_list = clue.repl.ClueRepl.prompt_players_list()
    # data = Scoresheet(["Dave", "Olivia", "Xeniya"])
    data = Scoresheet(players_list)
    repl = clue.repl.ClueRepl(data)
    """ 
    "quit" >> exits the repl hence all the entries are gone! DO NOT type that b4 the end of the game! 
        # TODO? add 'are you sure?' message
    "set" >> data.set_ownership('Dave', clue.PLUM, HAS_CARD) 
    "sheet" >> data.print_scoresheet()
    """
    repl.do_input()
    # TODO add an "undo" function


