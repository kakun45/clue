# Clue Worksheet Project

Digital Player's Assistant for the game Clue. 
  
Features:
- generates a digital score sheet with facts about a game, color codes its guesses
- watches over all the rules and automatically adds new info in player's scoresheet
- supports different sets of cards in a game

## How to play

```set <card> player=``` - sets(assigns) a card(-s) to a certain player(owner). 
Most truthy will work: 'true/t/yes/y/yep/does/do...' Ex.: ```set plum dave=yes``` 
yes,no, or ? for blank ... or even ```set plum dave=``` for blank

```d``` - supports partial card name typing, but this will return ["Dining", "Drawing"] if input just "d"

```dave knif plum di olivia=no``` - ex. of a turn input: dave(player-asker), 
knif(=knife weapon), 
plum(suspect), 
di(=dining room location), 
olivia(player-responder),
=no (responder's answer).

```clear```- clears out wrong current entry

```sheet``` - prints a scoresheet to a screen at any time

```analyze``` - run/rerun analytics on new information learned

```next```- proceed to a next turn (includes ```analyze```)

```history```  - prints out the turn history

```quit``` - quit the program

## How to test

```
python -m pytest tests/
```

## How to format

note: black's default is 88 char per line

```
black FILENAME
```

## How to lint
```
pylint clue
```

## todo:
- mark `set card=player` and `player=y` during the same turn

(VS typing 2ce player has the card "Dave=y" and "set card Dave=y" let it figure out only one entry of either)
- add an "undo" function
- while playing save it into a file, and add reload from .json
- propose whose turn it is? unless someone won't make it into a room
 