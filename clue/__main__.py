import clue
from clue import HAS_CARD, DOESNT_HAVE_CARD
from clue.scoresheet import Scoresheet
import clue.repl


def printing_test(data):
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


def main():
    print("Which game?")
    print("1. Master Detective")
    print("2. (newer version of Clue with green board)")
    choice = int(input("Enter version of game to play>"))
    game = [clue.MASTER_DETECTIVE, clue.GREEN_BOARD][choice - 1]
    # game = clue.MASTER_DETECTIVE
    # game = clue.GREEN_BOARD
    players_list = clue.repl.ClueRepl.prompt_players_list()
    player = clue.repl.ClueRepl.select_player(players_list)
    # add which player I'm to fill up all 0's after initial set command
    print(f"You are player {player}")
    data = Scoresheet(players_list, player, game)
    for card in game.all_cards:
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
