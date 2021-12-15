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


def main():
    players_list = clue.repl.ClueRepl.prompt_players_list()
    player = clue.repl.ClueRepl.select_player(players_list)
    # add which player I'm to fill up all 0's after initial set command
    print(f"You are player {player}")
    data = Scoresheet(players_list)
    for card in clue.ALL_CARDS:
        data.set_ownership(player, card, clue.DOESNT_HAVE_CARD)

    repl = clue.repl.ClueRepl(data)
    """ 
    "quit" >> exits the repl hence all the entries are gone! DO NOT type that b4 the end of the game! 
        # TODO? add 'are you sure?' message
    "set" >> data.set_ownership('Dave', clue.PLUM, HAS_CARD) 
    "sheet" >> data.print_scoresheet()
    """
    repl.do_input()


if __name__ == "__main__":
    main()

    # TODO:  prevent the line parser from allowing you to put the same player in `asker` and `responses`
    # TODO make sure asker is not in the responses of a log entry (and have a 'reset' command that resets the current entry)
    # TODO add an "undo" function
    # todo while playig save it into a file, and reload from .json
    # todo propose whose turn it is? unless someone won't make it into a room
    # todo start adding intelligence to figure out the cards players have >> WIP
    # todo set up a 'test' case with preset players and scoresheet partially filled up

    # todo when I type analyze it should to all of them it should keep running analyze until there is no new info
    # todo select which game we're using: with wich set of weapons/suspects/rooms
