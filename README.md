# RollDice Demo
Target: Create a program, which given a valid sequence of dice rolls will produce the total score for the game.

Programming Language
Python

Installation
Mac OS X: A version of Python is already installed.
Windows: You will need to install one of the 3.x versions available at python.org.

Dependency
No dependency required

General usage information
Download the ZIP package and unzip it.
In Terminal(MacOS) or Window Console, the script will run by simply typing python followed by the file name of the script: 
python rolldice_demo.py.

Tested On
 1. macOS 12.4 with the Python version 3.10.0 and Visual Studio Code
 2. Windows 11 Pro with the Python version 3.10.0 and Visual Studio Code
 
Unit Test
This script has implemented unitTest.
Input sample data in the use cases will be a sequence of dice rolls, which would look like:
[[1, 1, 3], [4, 2, 1], [6, 6, 2],[2, 1, 6], [5, 4, 1], [3, 3, 3], [3, 4, 5],[4, 5, 2], [2, 2, 2], [4, 4, 4], [6, 3, 5],[4, 1, 3]]


Limitation
A few use cases have been implemented. However, the application running failure may be possible.
Some situations have not been handled right now:
1. Incorrect number of rounds
2. Incorrect number of rolls
3. Incorrect number of roll values
