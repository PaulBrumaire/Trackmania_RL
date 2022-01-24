from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Reshape
from tensorflow.keras.optimizers import Adam

def build_model(states, actions, dim=True):
    model = Sequential()
    if(dim):
        model.add(Flatten(input_shape=(1, states[0])))
    model.add(Dense(24, activation='relu', input_shape=states))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(actions, activation='linear'))
    return model

from rl.agents import DQNAgent
from rl.policy import LinearAnnealedPolicy, BoltzmannQPolicy, EpsGreedyQPolicy
from rl.memory import SequentialMemory

def build_agent(model, actions):

    policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=1., value_min=.1, value_test=.05,
                              nb_steps=100000)
    memory = SequentialMemory(limit=100000, window_length=1)
    dqn = DQNAgent(model=model, memory=memory, policy=policy, gamma=.99, train_interval=1, delta_clip=1.,
                   nb_actions=actions, nb_steps_warmup=10000, target_model_update=10000, batch_size=1)
    return dqn

import rl.callbacks
import numpy as np


class EpisodeLogger(rl.callbacks.Callback):
    def __init__(self):
        self.observations = {}
        self.rewards = {}
        self.actions = {}
        self.loss = {}
        self.mae = {}
        self.mean_q = {}

    def on_episode_begin(self, episode, logs):
        self.observations[episode] = []
        self.rewards[episode] = []
        self.actions[episode] = []
        self.loss[episode] = []
        self.mae[episode] = []
        self.mean_q[episode] = []

    def on_step_end(self, step, logs):
        episode = logs['episode']
        self.observations[episode].append(logs['observation'])
        self.rewards[episode].append(logs['reward'])
        self.actions[episode].append(logs['action'])
        self.loss[episode].append(logs['metrics'][0])
        self.mae[episode].append(logs['metrics'][1])
        self.mean_q[episode].append(logs['metrics'][2])

class EpisodeLoggerTest(rl.callbacks.Callback):
    def __init__(self):
        self.observations = {}
        self.rewards = {}
        self.actions = {}

    def on_episode_begin(self, episode, logs):
        self.observations[episode] = []
        self.rewards[episode] = []
        self.actions[episode] = []


    def on_step_end(self, step, logs):
        episode = logs['episode']
        self.observations[episode].append(logs['observation'])
        self.rewards[episode].append(logs['reward'])
        self.actions[episode].append(logs['action'])

def sumReward(arr):
    s = 0
    (m, n) = np.array([arr]).shape
    out = np.zeros(((m, n)))
    for i in range(n):
        out[0, i] = arr[i]+s
        s = out[0, i]
    return out[0]