# Game 2048: Artificial intelligence

# Instructions:
#   Move up, down, left, or right to merge the tiles. The objective is to
#   get a tile with the number 2048 (or higher)
#
# Control:
#    arrows  : Merge up, down, left, or right
#    r       : Restart game
#    q / ESC : Quit

from Game2048 import Game2048
import numpy as np
import pygame

# env = Game2048()
# env.reset()
# actions = ['left', 'right', 'up', 'down']
# exit_program = False
# action_taken = False

saved_scores = []
number_of_simulations = 1
number_of_tests = 2

for i in range(number_of_tests):
    env = Game2048()
    env.reset()
    actions = ['left', 'right', 'up', 'down']
    exit_program = False
    action_taken = False
    while not exit_program:
        env.render()

        # Process game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_program = True
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                    exit_program = True
                if event.key == pygame.K_UP:
                    action, action_taken = 'up', True
                if event.key == pygame.K_DOWN:
                    action, action_taken  = 'down', True
                if event.key == pygame.K_RIGHT:
                    action, action_taken  = 'right', True
                if event.key == pygame.K_LEFT:
                    action, action_taken  = 'left', True
                if event.key == pygame.K_r:
                    env.reset()


        # INSERT YOUR CODE HERE

        # Dictionairy to contain scores for each first step
        scores = {'left': 0, 'right': 0, 'up': 0, 'down': 0}

        # Loops thorugh possible actions
        for first_action in actions:
            # Loops through a desired amount of games for each initial move
            for n in range(number_of_simulations):
                # A Game2048 object is created with the current state of the game
                # With this object we will "search" for the best solution for our next move by going randomly through the steps
                simulation = Game2048((env.board, env.score))

                # Takes the first step
                (board, score), reward, done = simulation.step(first_action)

                # Loops until the simulation hits game over. Done takes the value of game_over in the Game2048 object
                while not done:
                    # Picks a random action from the actions list
                    action = actions[np.random.randint(4)]
                    # The step is performed
                    (board, score), reward, done = simulation.step(action)

                    if done:
                        # Adds the score to the scores dictionairy
                        scores[first_action] += score

                    action_taken = True

        # Scores are printed
        print(scores)
        # Get the key of action in the scores dict with the highest value. This is the action to choose
        next_action = max(scores, key = lambda k: scores[k])
        print(next_action)

        # END OF YOUR CODE

        if action_taken:
            (board, score), reward, done = env.step(next_action)
            if done:
                saved_scores.append(score)
                print(saved_scores)
                exit_program = True
            action_taken = False

env.close()

# Write data to a csv file
with open("montecarlo"+ str(number_of_simulations) + "sims" + ".csv", "a") as file:
    # Loop through the saved scores and write them to the file seperated by ","
    for score in saved_scores:
        file.write("%s, " % score)
    file.close()
