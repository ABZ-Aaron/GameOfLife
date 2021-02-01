#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 21:24:47 2020

@author: aaronwright

Purpose: This is the game of life. It is a cellular automation, whereby 
        cells on a grid live or die depending on rules that have been set.
"""
############ Libraries and Global Variables ##############

# Import required libraries.
import numpy as np

import random

import time

# Set this to true to unleash a zombie cells which will work its way around 
# the board attacking other cells.
ZOMBIE_ATTACK = True

# These variables determine the number each cell type is represented by, 
# and array size.
ZOMBIE = 2
LIVE = 1
DEAD = 0
ARRAY_WIDTH = 20
ARRAY_HEIGHT = 20

##################### Functions #####################

# Generate blanks array (zeroes) of specified width and height.
def dead_state(width, height):
    array = np.zeros((width, height), dtype=np.int)
    return array

# Randomly populate array with 1s or 0s
def random_state(width, height):
    # Generate array of zeros. For each element in array, set to 0 or 1.
    state = dead_state(width, height)
    for x in range(0, width):
        for y in range(0, height):
            num = random.uniform(0,1) 
            state[x][y] = DEAD if num >= .5 else LIVE
        
    # If zombie is activated, add zombie to random cell
    if ZOMBIE_ATTACK:
        random_x = int(random.uniform(0, width))
        random_y = int(random.uniform(0, height)) 
        state[random_x][random_y] = ZOMBIE

    return state
     
# Format the board and print.
def render(state):
    # Create new array to store formatted board.
    formatted = np.zeros((state.shape[0], state.shape[1]), dtype=np.str)
    # Assign character based on number.
    for x in range(len(state)):
        for y in range(len(state[x])):        
            current_cell = state[x][y]        
            if current_cell == 1:
                formatted[x][y] = "."
            elif current_cell == 0:
                formatted[x][y] = " "
            elif current_cell == 2:
                formatted[x][y] = "@"            
    # Formate new array and print.
    for row in formatted:
        print(" ".join(map(str, row)))
        
# Determine what the next board state is based on rules
def next_board_state(state):
    # Return width and height of current state passed to function
    width = len(state)
    height = len(state[0])
    # Create new array to save new state
    new_state = dead_state(width, height)
    # Create list to save possible steps for zombie to take
    zombie_steps = []
    # Loop through width and height of array
    for x in range(0, width):
        for y in range(0, height):          
            # Initialise current cell and sum.
            # Sum will be used to dermine how many live cells there
            # are surrounding current cell.
            current_cell = state[x][y]
            liveSum = 0
            
            # For width of array, loop through range of cells before and after
            # current cell
            for i in range(x-1, x+2):         
                # If cell in range is off the board, move on to next one.
                if (i < 0) or (i >= width):
                    continue              
                # For height of array, loop through range of cells below and
                # above current cell
                for j in range(y-1, y+2):                  
                    # If cell in range is off the board, move on to next one.
                    if (j < 0) or (j >= height):
                        continue                  
                    # If cell in range is the current cell, move on to next one.
                    if (i == x) and (j == y):
                        continue                  
                    # For current cell in range, if it's live, add 1 to sum
                    if state[i][j] == LIVE:
                        liveSum += 1                     
                    # Save index to list to track possible steps zombie can take.
                    if current_cell == ZOMBIE:
                        zombie_steps.append((i,j))

            # If current cell is alive
            if current_cell == LIVE:
                # If live cells surrounding current cell is 0 or 1 or greater 
                # than 3, current cell is now dead. Else cell stays alive.
                if liveSum <= 1:
                    new_state[x][y] = DEAD
                elif liveSum <= 3:
                    new_state[x][y] = LIVE
                else:
                    new_state[x][y] = DEAD
                    
            # If current cell is dead.
            elif current_cell == DEAD:

                # If live cells surrounding dead cell is 3, cell is now 
                # alive. Else cell remains dead.
                new_state[x][y] = LIVE if liveSum ==3 else DEAD
                        
    return new_state, zombie_steps
            
            
################# Start Script ##################  
    
# Generate initial state.
state = random_state(ARRAY_WIDTH, ARRAY_HEIGHT)
new_state = state

# Pass initial state to render to convert 1s to #s and 0s to blank spaces.
# Then generate next board state based on rules, and continue
# indefinitely.
while True:
    render(new_state)
    new_state, zombie_steps = next_board_state(new_state)
    
    # Unleash a zombie to attach the humans
    if ZOMBIE_ATTACK:
        zombie_step = random.choice(zombie_steps)
        new_state[zombie_step[0]][zombie_step[1]] = ZOMBIE
        
    # Stop script if all cells are destoryed.
    alive= 0
    for x in range(len(new_state)):
        for y in range(len(new_state[x])):
            if new_state[x][y] == 1:
                alive +=1
                
    if alive == 0:
        render(new_state)
        print("All Cells Destroyed!!")
        break
    
    time.sleep(0.03)


    

