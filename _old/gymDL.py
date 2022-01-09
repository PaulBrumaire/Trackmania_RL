from driver import reloadKey
from tensorflow.keras.optimizers import Adam
from _old.model import build_model, build_agent
from _old.customEnv import TMEnvGP,TMEnvSimple,TMEnvDistances
from time import time, sleep
import keyboard
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = "3"
from tensorflow.keras.utils import plot_model

# Records gameplay
# g - gooo recording
# f - stop recording
# q - quits recorder

# def data_getter():
#     global data
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect(("127.0.0.1", 9000))
#         while True:
#             data = myGetData.get_data(s)


# data_getter_thread = threading.Thread(target=data_getter, daemon=True)
# data_getter_thread.start()

print("ready")
scores = []

simple=False

if(simple):
    env = TMEnvSimple()
    states = env.observation_space.shape
    actions = env.action_space.n
else:
    env = TMEnvDistances()
    states = env.observation_space.shape
    actions = env.action_space.n


# MODEL

model = build_model(states, actions)

print(env.observation_space.sample(),states)


model.summary()
# plot_model(model, show_shapes=True)


if(True):
    dqn = build_agent(model, actions)
    dqn.compile(Adam(lr=1e-3), metrics=['mae'])
    dqn.fit(env, nb_steps=10000, visualize=False, verbose=1)

    scores = dqn.test(env, nb_episodes=100, visualize=False)
    print(np.mean(scores.history['episode_reward']))

    _ = dqn.test(env, nb_episodes=15, visualize=True)

    dqn.save_weights('w_distances.h5f', overwrite=True)    

#nb_epoch = 1
# while not keyboard.is_pressed('q'):
#     if not keyboard.is_pressed('g'):
#         continue
#     print("running...")
#     for i in range(nb_epoch):

#         _, _ = env.reset()
#         done = False
#         score = 0

#         reloadKey()
#         while not done:
#             # get random actions
#             action = env.action_space.sample()
#             # step gym
#             speed, distances, reward, done, info = env.step(action)
#             score += reward
#             # print(score)
#             sleep(0.1)

#             if keyboard.is_pressed('f'):
#                 print("finish")
#                 break

#             if(done):
#                 break
#         scores.append(score)
#     break

# print("finished")
# print(scores)
