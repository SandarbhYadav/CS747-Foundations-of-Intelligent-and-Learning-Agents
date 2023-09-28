from importlib.resources import path
from gym_driving.assets.car import *
from gym_driving.envs.environment import *
from gym_driving.envs.driving_env import *
from gym_driving.assets.terrain import *

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import time
import pygame, sys
from pygame.locals import *
import random
import math
import argparse

# Do NOT change these values
TIMESTEPS = 1000
FPS = 30
NUM_EPISODES = 10

class Task1():

    def __init__(self):
        """
        Can modify to include variables as required
        """

        super().__init__()

    def next_action(self, state, theta):
        """
        Input: The current state
        Output: Action to be taken
        TO BE FILLED
        """

        # Replace with your implementation to determine actions to be taken

        # Current angle of the car
        phi = state[3]
        phi = phi % 360

        # Car is aligned with centre of the road
        if abs(theta - phi) < 2:
            # Straight
            action_steer = 1
            action_acc = 4

        # Car is not aligned with centre of the road
        else:
            # Rotate
            if theta < 180:
                if theta < phi <= 180 + theta:
                    # Anticlockwise
                    action_steer = 0
                    action_acc = 2
                else:
                    # Clockwise
                    action_steer = 2
                    action_acc = 2
            else:
                if theta - 180 <= phi < theta:
                    # Clockwise
                    action_steer = 2
                    action_acc = 2
                else:
                    # Anticlockwise
                    action_steer = 0
                    action_acc = 2

        action = np.array([action_steer, action_acc])  

        return action

    def controller_task1(self, config_filepath=None, render_mode=False):
        """
        This is the main controller function. You can modify it as required except for the parts specifically not to be modified.
        Additionally, you can define helper functions within the class if needed for your logic.
        """
    
        ######### Do NOT modify these lines ##########
        pygame.init()
        fpsClock = pygame.time.Clock()

        if config_filepath is None:
            config_filepath = '../configs/config.json'

        simulator = DrivingEnv('T1', render_mode=render_mode, config_filepath=config_filepath)

        time.sleep(3)
        ##############################################

        # e is the number of the current episode, running it for 10 episodes
        for e in range(NUM_EPISODES):
        
            ######### Do NOT modify these lines ##########
            
            # To keep track of the number of timesteps per epoch
            cur_time = 0

            # To reset the simulator at the beginning of each episode
            state = simulator._reset()

            # Added by me
            x_init = state[0]
            y_init = state[1]
            theta_rad = math.atan2((0 - y_init), (350 - x_init))
            theta_deg = np.rad2deg(theta_rad)
            theta = theta_deg % 360
            
            # Variable representing if you have reached the road
            road_status = False
            ##############################################

            # The following code is a basic example of the usage of the simulator
            for t in range(TIMESTEPS):
        
                # Checks for quit
                if render_mode:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()

                action = self.next_action(state, theta)
                state, reward, terminate, reached_road, info_dict = simulator._step(action)
                fpsClock.tick(FPS)

                cur_time += 1

                if terminate:
                    road_status = reached_road
                    break

            # Writing the output at each episode to STDOUT
            print(str(road_status) + ' ' + str(cur_time))

class Task2():

    def __init__(self):
        """
        Can modify to include variables as required
        """

        super().__init__()

    def next_action(self, state, ran_cen_list):
        """
        Input: The current state
        Output: Action to be taken
        TO BE FILLED

        You can modify the function to take in extra arguments and return extra quantities apart from the ones specified if required
        """

        # Replace with your implementation to determine actions to be taken

        # Extracting state features
        x = state[0]
        y = state[1]
        v = state[2]
        a = state[3]
        a = a % 360
        ang_tol = 4

        # Declaration
        action_steer = 1
        action_acc = 4

        # Region 1
        if max(ran_cen_list[1][1] + 80, ran_cen_list[3][1] + 80, -50) < y < min(ran_cen_list[0][1] - 80, ran_cen_list[2][1] - 80, 50):
            if (a < ang_tol) or (360 - ang_tol < a < 360):
                # Straight
                action_steer = 1
                action_acc = 4
            else:
                # Rotate
                if a <= 180:
                    # Rotate anticlockwise
                    action_steer = 0
                    action_acc = 2
                else:
                    # Rotate clockwise
                    action_steer = 2
                    action_acc = 2

        # Region 2
        elif ((ran_cen_list[0][0] - 80 < x < ran_cen_list[0][0] + 80) and (y > ran_cen_list[0][1] + 80)) \
                or ((ran_cen_list[1][0] - 80 < x < ran_cen_list[1][0] + 80) and (y < ran_cen_list[1][1] - 80)) \
                or ((ran_cen_list[2][0] - 80 < x < ran_cen_list[2][0] + 80) and (y > ran_cen_list[2][1] + 80)) \
                or ((ran_cen_list[3][0] - 80 < x < ran_cen_list[3][0] + 80) and (y < ran_cen_list[3][1] - 80)):

            if (a < ang_tol) or (360 - ang_tol < a < 360):
                # Straight
                action_steer = 1
                action_acc = 4
            else:
                # Rotate
                if a <= 180:
                    # Rotate anticlockwise
                    action_steer = 0
                    action_acc = 2
                else:
                    # Rotate clockwise
                    action_steer = 2
                    action_acc = 2

        # Region 3
        else:
            if y > 0:
                if abs(a - 270) < ang_tol:
                    # Straight
                    action_steer = 1
                    action_acc = 4
                else:
                    # Rotate
                    if 90 < a < 270:
                        # Clockwise
                        action_steer = 2
                        action_acc = 2
                    else:
                        # Anticlockwise
                        action_steer = 0
                        action_acc = 2
            else:
                if abs(a - 90) < ang_tol:
                    # Straight
                    action_steer = 1
                    action_acc = 4
                else:
                    # Rotate
                    if 90 < a < 270:
                        # Anticlockwise
                        action_steer = 0
                        action_acc = 2
                    else:
                        # Clockwise
                        action_steer = 2
                        action_acc = 2

        action = np.array([action_steer, action_acc])  

        return action

    def controller_task2(self, config_filepath=None, render_mode=False):
        """
        This is the main controller function. You can modify it as required except for the parts specifically not to be modified.
        Additionally, you can define helper functions within the class if needed for your logic.
        """
        
        ################ Do NOT modify these lines ################
        pygame.init()
        fpsClock = pygame.time.Clock()

        if config_filepath is None:
            config_filepath = '../configs/config.json'

        time.sleep(3)
        ###########################################################

        # e is the number of the current episode, running it for 10 episodes
        for e in range(NUM_EPISODES):

            ################ Setting up the environment, do NOT modify these lines ################
            # To randomly initialize centers of the traps within a determined range
            ran_cen_1x = random.randint(120, 230)
            ran_cen_1y = random.randint(120, 230)
            ran_cen_1 = [ran_cen_1x, ran_cen_1y]

            ran_cen_2x = random.randint(120, 230)
            ran_cen_2y = random.randint(-230, -120)
            ran_cen_2 = [ran_cen_2x, ran_cen_2y]

            ran_cen_3x = random.randint(-230, -120)
            ran_cen_3y = random.randint(120, 230)
            ran_cen_3 = [ran_cen_3x, ran_cen_3y]

            ran_cen_4x = random.randint(-230, -120)
            ran_cen_4y = random.randint(-230, -120)
            ran_cen_4 = [ran_cen_4x, ran_cen_4y]

            ran_cen_list = [ran_cen_1, ran_cen_2, ran_cen_3, ran_cen_4]            
            eligible_list = []

            # To randomly initialize the car within a determined range
            for x in range(-300, 300):
                for y in range(-300, 300):

                    if x >= (ran_cen_1x - 110) and x <= (ran_cen_1x + 110) and y >= (ran_cen_1y - 110) and y <= (ran_cen_1y + 110):
                        continue

                    if x >= (ran_cen_2x - 110) and x <= (ran_cen_2x + 110) and y >= (ran_cen_2y - 110) and y <= (ran_cen_2y + 110):
                        continue

                    if x >= (ran_cen_3x - 110) and x <= (ran_cen_3x + 110) and y >= (ran_cen_3y - 110) and y <= (ran_cen_3y + 110):
                        continue

                    if x >= (ran_cen_4x - 110) and x <= (ran_cen_4x + 110) and y >= (ran_cen_4y - 110) and y <= (ran_cen_4y + 110):
                        continue

                    eligible_list.append((x,y))

            simulator = DrivingEnv('T2', eligible_list, render_mode=render_mode, config_filepath=config_filepath, ran_cen_list=ran_cen_list)
        
            # To keep track of the number of timesteps per episode
            cur_time = 0

            # To reset the simulator at the beginning of each episode
            state = simulator._reset(eligible_list=eligible_list)
            ###########################################################

            # The following code is a basic example of the usage of the simulator
            road_status = False

            for t in range(TIMESTEPS):
        
                # Checks for quit
                if render_mode:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()

                action = self.next_action(state, ran_cen_list)
                state, reward, terminate, reached_road, info_dict = simulator._step(action)
                fpsClock.tick(FPS)

                cur_time += 1

                if terminate:
                    road_status = reached_road
                    break

            print(str(road_status) + ' ' + str(cur_time))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="config filepath", default=None)
    parser.add_argument("-t", "--task", help="task number", choices=['T1', 'T2'])
    parser.add_argument("-r", "--random_seed", help="random seed", type=int, default=0)
    parser.add_argument("-m", "--render_mode", action='store_true')
    parser.add_argument("-f", "--frames_per_sec", help="fps", type=int, default=30) # Keep this as the default while running your simulation to visualize results
    args = parser.parse_args()

    config_filepath = args.config
    task = args.task
    random_seed = args.random_seed
    render_mode = args.render_mode
    fps = args.frames_per_sec

    FPS = fps

    random.seed(random_seed)
    np.random.seed(random_seed)

    if task == 'T1':
        
        agent = Task1()
        agent.controller_task1(config_filepath=config_filepath, render_mode=render_mode)

    else:

        agent = Task2()
        agent.controller_task2(config_filepath=config_filepath, render_mode=render_mode)
