# import torch
import random
# import numpy as np
from collections import deque

from ml.ml_training.pytorch.tetris_pytorch import TetrisGame

MAX_MEMORY = 100.000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self) -> None:
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        # self.model = Linear_QNet(11, 256, 3)
        # self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
    
    def get_move(self, state):
        ...


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = TetrisGame()

    while True:
        # get old state
        state_old = game.get_state()
        # agent.get_state(game)

        # get move
        final_move = agent.get_move(state_old)
        # agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.make_move(final_move)
        state_new = game.get_state()

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            # print('Game', agent.n_games, 'Score', score, 'Record:', record)

            # plot_scores.append(score)
            # total_score += score
            # mean_score = total_score / agent.n_games
            # plot_mean_scores.append(mean_score)
            # plot(plot_scores, plot_mean_scores)