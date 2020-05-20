<h1>The Sprouts Game<h1>
<h2> Introduction <h2>
 
Invented in 1967, Sprouts is a two player game that starts with any number of dots randomly placed. Taking turns, players will connect two dots with a line (this includes starting and ending a line at the same dot) and adding a new dot somewhere along this line after which their turn ends. The game ends when no more connections can be made and the player to draw the last valid line is the winner. They are constrained by the following rules:

<h2> The Rules <h2>

1. The line may take on any shape, but not get too close to itself, or cross existing lines.
2. The new dot may not be placed on an existing dot. The new dot will split an existing line into two shorter lines.
3. No dot can have more than three lines attached to it, so new dots placed are considered to have two lines attached to it already.

The idea is to make it impossible for the other player to win.

Rules obtained : https://nrich.maths.org/2413

<h2> Implementation <h2>

Choose to implement in Python using pygame as I'd not worked with the library before to pose more of a challenge. 
Further utilised:
- sys: Exit feature
- math: Distance calculation
- random: Start sequence randomly generated
- time: access to Clock


