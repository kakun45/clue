from typing import List

import clue


class Fact:
    def __init__(self, player: str, card: str, has_card: bool):
        """
        player Has or Doesn't have a card
        """
        self.player = player
        self.card = card
        self.has_card = has_card

    def card_state(self) -> int:
        if self.has_card:
            return clue.HAS_CARD
        else:
            return clue.DOESNT_HAVE_CARD

    def __str__(self):
        return f"Fact({self.player}, {self.card}, {self.has_card})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, Fact) and self.player == other.player and self.card == other.card and self.has_card == other.has_card


def rule_1(sheet, turn_history) -> List[Fact]:
    """
    Only one player can have a card
    :return:
    """
    results = []
    for card in sheet.all_cards():
        owner = sheet.get_owner(card)
        if owner:
            other_players = list(sheet.players_names)
            other_players.remove(owner)
            for other_player in other_players:
                if sheet.get_ownership(other_player, card) == clue.BLANK:
                    results.append(Fact(other_player, card, False))  # Player, clue.GREEN, DOESNT_HAVE_CARD
                elif sheet.get_ownership(other_player, card) == clue.HAS_CARD:
                    raise Exception("more than one player has a card")
                else:
                    # they are already marked with "doesnt have card"
                    pass
    return results


def rule_2(sheet, turn_history) -> List[Fact]:
    """
    During the turn we just found out that one of the players doesn't have all 3 asking cards
    :return: results -> List[Fact]
    """
    results = []
    for turn in turn_history:  # [obj1, obj2]
        for player_key in turn.responses:  # {player:True, player:False}
            if not turn.responses[player_key]:  # player:False
                results.append(Fact(player_key, turn.suspect, False))
                results.append(Fact(player_key, turn.weapon, False))
                results.append(Fact(player_key, turn.room, False))

    return results


def rule_3(sheet, turn_history) -> List[Fact]:
    """
    Check every turn!
    A guesses (Plum, Knife, Gazebo) and B=Yes,C=No.   If scoresheet says B does not have plum or gazebo (B does not have plum and B does not have gazebo),
    then B must have the knife.

    :param sheet:
    :param turn_history:
    :return:  List[Fact]
    """
    results = []
    for turn in turn_history:  # [obj1, obj2]
        for player_key in turn.responses:  # {player:True, player:False}
            if turn.responses[player_key]:  # "YES"
                cards = [turn.suspect, turn.weapon, turn.room]
                actual_states = sheet.get_ownership_cards(player_key, cards)
                looking_for = [clue.BLANK, clue.DOESNT_HAVE_CARD, clue.DOESNT_HAVE_CARD]  # looking for 2 doesn't_have-s
                if sorted(actual_states) == sorted(looking_for):

                    the_card = None
                    for i in range(3):
                        if actual_states[i] == clue.BLANK:
                            if the_card:
                                raise Exception()
                            the_card = cards[i]
                    if the_card is None:
                        raise Exception()
                    results.append(Fact(player_key, the_card, True))
    return results


def rule_4(sheet, turn_history) -> List[Fact]:
    """
    Every weapon except one is own by a player, that One is an Answer
    :param sheet:
    :param turn_history:
    :return:
    """
    def r4(sheet, cards: List[str]) -> List[Fact]:
        potential_answers = []
        for card in cards:
            if not sheet.is_excluded(card):  # situation when BLANK or DOESNT_HAVE_CARD for every player in a row
                potential_answers.append(card)
        if len(potential_answers) == 1:
            # if card is the answer
            results = []
            for player in sheet.players_names:
                results.append(Fact(player, potential_answers[0], False))
            return results
        else:
            return []

    return r4(sheet, sheet.game.suspects) + r4(sheet, sheet.game.weapons) + r4(sheet, sheet.game.rooms)


def rule_5(sheet, turn_history) -> List[Fact]:
    """ 4 player game: the asker asks with one of his cards, and 2 ppl have them, we don;t need to know who has it, we mark they
    aren't the answer
    """
    # skip if less than 4 players
    if len(sheet.players_names) < 4:
        return []
    results = []
    for turn in turn_history:
        cards = [turn.suspect, turn.weapon, turn.room]
        # exactly 2 people must have responded yes, and neither can be the current player:
        ppl_responded_yes = [player_key for player_key in turn.responses if turn.responses[player_key]]
        if len(ppl_responded_yes) == 2 and sheet.current_player not in ppl_responded_yes and sheet.current_player != turn.asker:
            # sanity check:  current player shouldn't have any of these cards: [2,2,2]
            if [sheet.get_ownership(sheet.current_player, card) for card in cards] == [clue.DOESNT_HAVE_CARD, clue.DOESNT_HAVE_CARD, clue.DOESNT_HAVE_CARD]:
                # look for one card not owned by ppl_responded_yes, and two cards where we have blanks for both players
                neither_has_it = []
                both_are_blank = []
                player_b, player_c = ppl_responded_yes
                for card in cards:
                    if sheet.get_ownership(player_b, card) == clue.DOESNT_HAVE_CARD and sheet.get_ownership(player_c, card) == clue.DOESNT_HAVE_CARD:
                        neither_has_it.append(card)
                    elif sheet.get_ownership(player_b, card) == clue.BLANK and sheet.get_ownership(player_c, card) == clue.BLANK:
                        both_are_blank.append(card)
                if len(neither_has_it) == 1 and len(both_are_blank) == 2:
                    results.append(Fact(None, both_are_blank[0], True))
                    results.append(Fact(None, both_are_blank[1], True))

    return results


def rule_6(sheet, turn_history) -> List[Fact]:
    pass


def run_all(sheet, turn_history) -> List[Fact]:
    rules = [rule_1, rule_2, rule_3, rule_4, rule_5]  #rule_5, rule_6, rule_7]
    results = []
    for f in rules:
        results += f(sheet, turn_history)

    # only return NEW facts
    return [fact for fact in results if not sheet.has_fact(fact)]
