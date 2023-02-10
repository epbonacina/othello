A Alpha-beta pruning based AI capable of playing Othello.


# How to play
We recommend the [World Othello Federation](https://www.worldothello.org/about/about-othello/othello-rules/official-rules/english) website for more information about game rules.

In order to test our AI, you could run `python server.py advsearch.fanatico advsearch.humanplayer`.  
This command should start a match between you, the human player, and our AI, `fanatico`.

The current board will always be displayed on screen and, during your turn, you will be asked to type the column and line on which you want to place a disk. You should type something like `7 0`, where `7` and `0` are the chosen column and line, respectively.

![image](https://user-images.githubusercontent.com/63553534/217971348-55f33832-0724-4995-8967-67112aaf4f47.png)

The asterisks that surround some disks in the previous image represent the disks that have flipped from `W` (white) to `B` (black) during the previous player move. 

# Available players
There are a few available players for you to test.

- `advsearch.fanatico`, which is our current best player;
- `advsearch.que_loucura`, which is our previous champion;
- `advsearch.randomplayer`, which has no brain;
- `advsearch.humanplayer`, which is you.

You can choose which players you want to test in the previous section.


# Required Python packages
There are no external Python packages needed.


# Implementation details
## Evaluation:
Our champion evaluates the current board analysing its `actual_mobility`, `potencial_mobility` and its corners.
- `actual_mobility`: analyses the number of moves each player can make;
- `potencial_mobility`: analyses the number of empty slots around each player's disks;
- `corners_indirect`: analyses if its possible to capture a corner during the next turn;
- `corners_direct`: analyses the number of corners captured by the player.

## Terminating condition
We use a simple depth terminating condition. When our AI explores more than a certain number of levels of the tree, it returns the its evaluation of the current board. If the computer on which the AI is beeing executed is powerful enough, the depth will be automatically increased.

## Enhancements
- We've optimized our weights by minimizing the Mean Squared Error (MSE) of our evaluation function. Because of its demanding nature, the process of minimizing the MSE was only possible after pre-computing the evaluation function components. It boosted our optimization process in at least 10000x and gave us a very small MSE (<0,001).

- We've implemented a Transposition Table that is responsible for detecting if the current game state has already been seen before. If that is the case, then we already have the computed value for that state.

# Developers
- Enzo Pedro Bonacina [Turma B] 00313316;
- Hiram Artnak Martins [Turma B] 00276484;
- Thales Junqueira Albergaria Moraes Perez [Turma B] 00303035.

# References
- Artificial Intelligence: A Modern Approach. Disponível em: <http://aima.cs.berkeley.edu/>;
- SANNIDHANAM, V.; ANNAMALAI, M. An Analysis of Heuristics in Othello. [s.l: s.n.]. Disponível em: <https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf>.



