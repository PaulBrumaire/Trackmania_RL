import getData as myGetData
import socket
import threading
from gym import Env
from gym.spaces import Discrete, Box, Tuple
import numpy as np
import random
from PIL import Image
from screenshot import screenshot
from getLidar import getMesuresDistances
from time import time, sleep
from driver import controlGamepad, controlKey, reloadKey, releaseAllKeys, releaseGamepad,controlKey2
import vgamepad as vg

nb_lidar = 11
race_step = 800
gamepad = vg.VX360Gamepad()

def data_getter_function():
    global data
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", 9000))
        while True:
            data = myGetData.get_data(s)


data_getter_thread = threading.Thread(target=data_getter_function, daemon=True)
data_getter_thread.start()
sleep(0.1)


def getInfos():
    speed = data['speed']
    finish = data['finish']
    # screenshot
    frame = Image.fromarray(screenshot())
    # get distances
    distances = getMesuresDistances(frame)
    return distances, speed, finish

class TMEnvDistances(Env):
    def __init__(self):
        # Actions we can take
        self.action_space = Discrete(4)
        # Speed [{0:1000}]
        self.observation_space = Box(low=0, high=400, shape=(nb_lidar,))
        # Set start speed
        self.state = [0]*nb_lidar
        self.speed = 0
        # Set race length
        self.race_length = race_step

    def step(self, action):
        # Make ingame action 
        controlKey2(action)
        # Get data from game
        n_distances, n_speed, n_finish = getInfos()
        # Reduce race length by 1 second
        self.race_length -= 1 
        # Calculate reward
        reward = 0
        reward += n_speed - self.speed
        # Save speed
        self.speed = n_speed
        self.state = n_distances
        # Check if race is done
        if self.race_length <= 0 or n_finish: 
            done = True
            reward += (self.race_length)*100
            # Restart game
            reloadKey()
        else:
            done = False
        
        # Set placeholder for info
        info = {}
        
        # Return step information
        return self.state, reward, done, info

    def render(self):
        # The game is the visual representation
        pass
    
    def reset(self):
        # Restart the game
        releaseAllKeys()
        reloadKey()
        # Reset speed
        self.state = [0]*nb_lidar
        self.speed = 0
        # Reset race time
        self.race_length = race_step
        return self.state

class TMEnvSimple(Env):
    def __init__(self):
        # Actions we can take
        self.action_space = Discrete(4)
        # Speed [{0:1000}]
        self.observation_space = Box(low=np.array([0]), high=np.array([1000]))
        # Set start speed
        self.state = 0
        # Set race length
        self.race_length = race_step

    def step(self, action):
        # Make ingame action 
        controlKey2(action)
        # Get data from game
        n_distances, n_speed, n_finish = getInfos()
        # Reduce race length by 1 second
        self.race_length -= 1 
        # Calculate reward
        reward = 0
        reward += n_speed - self.state
        # Save speed
        self.state = n_speed
        # Check if race is done
        if self.race_length <= 0 or n_finish: 
            done = True
            reward += (self.race_length)*100
            # Restart game
            reloadKey()
        else:
            done = False
        
        # Set placeholder for info
        info = {}
        
        # Return step information
        return self.state, reward, done, info

    def render(self):
        # The game is the visual representation
        pass
    
    def reset(self):
        # Restart the game
        releaseAllKeys()
        reloadKey()
        # Reset speed
        self.state = 0
        # Reset race time
        self.race_length = race_step
        return self.state


class TMEnvGP(Env):
    def __init__(self):
        # actions possibles (gas , break, steer)
        self.action_space = Discrete(4)#Box(low=np.array([0,0,-1]), high=np.array([1,1,1]))#Box(low=0, high=1, shape=(3,))
        # observation possibles
        self.observation_speed = Box(low=0, high=1000, shape=(1,))
        self.observation_space = Box(low=0, high=400, shape=(nb_lidar,))
        # état de la voiture et environnement acuel
        self.speed = 0
        self.state = [0]*nb_lidar
        # init race time
        self.race_length = race_step

    def step(self, action):
        # do action
        #controlGamepad(gamepad, action)
        controlKey2(action)
        # get data
        n_distances, n_speed, n_finish = getInfos()
        self.race_length -= 1 
        # speed reward
        reward = 0
        reward += n_speed - self.speed

        # update states
        self.speed = n_speed
        self.state = n_distances
        # nb actions
        info = {}
        # reward finish
        if self.race_length <= 0 or n_finish:
            done = True
            reward += (self.race_length)*100
            reloadKey()
        else:
            done = False
        return np.concatenate(( [self.speed],self.state)), reward, done, info
        # speed, distances, reward, done, info

    def render(self):
        pass

    def reset(self):
        releaseAllKeys()
        reloadKey()
        self.speed = 0
        self.state = [0]*nb_lidar
        self.race_length = race_step
        return np.concatenate(( [self.speed],self.state))


if(False):
    env = TMEnvDistances()
    states = env.observation_space.shape
    actions = env.action_space.n
    # MODEL
    env.step(1)