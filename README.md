# Clue Worksheet Project

Digital Player's Assistant for the game Clue. 
  
Features:
- generates a digital score sheet with facts about a game, color codes its guesses
- watches over all the rules and automatically adds new info in player's scoresheet
- supports different sets of cards in a game
<img width="944" alt="Screen Shot 2023-01-22 at 11 23 28 PM" src="https://user-images.githubusercontent.com/53381916/213966592-b0659209-9f8e-4574-803a-49528565400f.png">


## How to play
```
python -m clue
```

```set <card> player=``` - initial set(assign) a card(-s) to a certain player(owner). 
Most truthy will work after = 'true/t/yes/y/yep/does/do...' Ex.: ```set plum dave=yes``` 
yes,no, or ? for blank ... or even ```set plum dave=``` for blank
<img width="948" alt="Screen Shot 2023-01-22 at 11 35 04 PM" src="https://user-images.githubusercontent.com/53381916/213966583-37b4efce-b27c-43ea-b14f-bdcdb6f420c3.png">

```d``` - supports partial card name typing, but this will return ["Dining", "Drawing"] if input just "d"

```dave knif plum di olivia=no``` - ex. of a turn input: dave(player-asker), 
knif(=knife weapon), 
plum(suspect), 
di(=dining room location), 
olivia(player-responder),
=no (responder's answer).
<img width="948" alt="Screen Shot 2023-01-22 at 11 39 39 PM" src="https://user-images.githubusercontent.com/53381916/213966953-292c7a6f-842b-4c80-9c29-e808bbd65ee3.png">

```clear```- clears out wrong current entry
<img width="950" alt="Screen Shot 2023-01-22 at 11 41 10 PM" src="https://user-images.githubusercontent.com/53381916/213967060-84efa1d0-60e7-4147-94d3-3038b130df5d.png">

```sheet``` - prints a scoresheet to a screen at any time

```analyze``` - run/re-run analytics on new information learned
<img width="949" alt="Screen Shot 2023-01-22 at 11 43 19 PM" src="https://user-images.githubusercontent.com/53381916/213967245-3275ddb6-6736-4f94-b5b5-8de300897015.png">

```next```- proceed to a next turn (includes ```analyze```)
<img width="949" alt="Screen Shot 2023-01-22 at 11 45 07 PM" src="https://user-images.githubusercontent.com/53381916/213967404-ae70a539-addf-4b66-9362-39e50a530448.png">

You may get lucky and guess one of 3 answers on your first turn, which will be highlighted in red for you
<img width="947" alt="Screen Shot 2023-01-22 at 11 45 58 PM" src="https://user-images.githubusercontent.com/53381916/213967648-1d71010b-c559-4cdd-9020-f0162a9a806b.png">

```history```  - prints out the turn history
<img width="947" alt="Screen Shot 2023-01-22 at 11 50 33 PM" src="https://user-images.githubusercontent.com/53381916/213967916-1d6881f6-ad52-4c33-a868-00825431749d.png">

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
 
