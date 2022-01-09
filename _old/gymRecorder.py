from PIL import Image
import threading
from struct import unpack
import socket
import sys
import pathlib
import numpy as np
from time import time, sleep
import myGetData as myGetData
from myScreenshot import screenshot
import keyboard
import vgamepad as vg
from getLidar import getMesuresDistances
from customEnv import TMEnvSimple, TMEnvGP

# Records gameplay
# g - gooo recording
# f - stop recording
# q - quits recorder

gp = True
gamepad = vg.VX360Gamepad()

random=False

print("ready")
scores = []
env = TMEnvSimple()
nb_epoch = 1

while not keyboard.is_pressed('q'):
    if not keyboard.is_pressed('g'):
        continue
    print("running...")
    for i in range(nb_epoch):

        _ = env.reset()
        done = False
        score = 0

        while not done:
            # get random actions
            if(random):
                action = env.action_space.sample()
            else:
                action = None
            # step gym
            state, reward, done, info = env.step(action)
            score += reward
            # print(score)
            sleep(0.01)

            if keyboard.is_pressed('f'):
                print("finish")
                break

            if(done):
                break
        scores.append(score)
    break

print("finished")
print(scores)


