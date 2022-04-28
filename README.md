## The Game
This is a terminal implementation of the classic brick breaking game.  
To start the game, run 

```bash
python main.py
```

The game keeps track of the time game has been played, the user score and the lives remaining.
## The controls
a : Move Left  
b : Move Right  
' ': Launch Ball (Whitespace)  
x : Exit Game
n : Next Level 

## Blocks
Three types of blocks are available:

* **Unbreakable**: Cannot be broken except when using a through ball power up  
* **Breakable**:
Has a power state and is broken when power is zero. Power Max to Min &rarr; Green, Blue and Red   
* **Exploding**:
When this is broken it also breaks the bricks neighboring to it  
* **Rainbow**:
Changes color and power until hit for the first time


## Scoring
Whenever an breakable block is broken, the player gains point equal to the initial power of the brick  
Whenever an unbreakable block is broken, the player gains 5 points  
Whenever an exploding block is broken, the player gets 1 point 


## Power ups
Whenever a breakable brick is broken, it has a 10% chance of dropping one of the following powerups

| Name            | Symbol | Description                                            |
| --------------- | ------ | ------------------------------------------------------ |
| Expand Paddle   | E      | Expands the paddle                                     |
| Shrink Paddle   | S      | Shrinks the paddle                                     |
| Fast Ball       | F      | Increases the speed of the ball                        |
| Through Ball    | T      | Allows the ball to break through any brick in its path |
| Paddle Grab     | G      | Allows paddle to grab the ball when in contact         |
| Shooting Paddle | B      | The paddle shoots bullets for a fixed time             |

All the powerups are temporary and are deactivated after a small duration of time
