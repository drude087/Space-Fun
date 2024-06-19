# Space-Fun
Project Title: Space Fun
Overview:

"Space Fun" is a 2D space shooter game developed using Pygame, a popular Python library for creating video games. The game features a player-controlled spaceship that navigates through space, shooting enemies and dodging obstacles. The objective is to survive as long as possible while achieving a high score. As the game progresses, the difficulty increases with more frequent enemy and obstacle spawns.

Key Features:

Player Movement:

The player controls a spaceship that can move left, right, up, and down within the screen boundaries using the arrow keys.

A teleport/dash feature allows the player to make quick horizontal movements by pressing 'A' for left and 'D' for right. 

This feature is available at regular intervals (every 5 seconds).

Enemies and Obstacles:

Enemies: Appear at the top of the screen and move downward. They can shoot bullets toward the player.

Rocks: Act as obstacles that fall from the top of the screen and need to be avoided or destroyed.

Hearts: Represent the player's lives and are displayed on the screen. The player starts with three hearts.

Shooting Mechanics:

The player can shoot bullets by pressing the space bar.

Bullets move upwards and can destroy enemies and rocks on collision.

Enemies also shoot bullets downward toward the player.

Score System:

The player's score increases by one point every second.

The score is displayed on the screen and is updated in real-time.

Collision Detection:

Bullets collide with enemies and rocks, destroying both upon impact.

The player collides with enemies, rocks, and enemy bullets, losing a heart upon collision.

If the player loses all hearts, the game ends.

Difficulty Progression:

The game increases in difficulty as the player's score increases. This is achieved by decreasing the spawn intervals of enemies, rocks, and enemy bullets.


