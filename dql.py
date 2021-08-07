from Snake import *
import pickle
import random


class QL:
    def __init__(self, size):
        self.size = size
        self.snake = SnakeGame(size)
        self.snake.reset()

        self.q = {}

    # def reward(self, action):
    #     cpy = self.s.copy()
    def load(self, file):
        temp = pickle.load(file)
        self.snake = temp.snake
        self.q = temp.q
        self.size = temp.size

    def save(self, file):
        pickle.dump(self, file)

    def get_q_values(self, state):
        if state in self.q:
            return self.q[state]
        else:
            self.q[state] = [random.random() for i in range(3)]
            return self.q[state]

    def train(self, lr, dis, episodes, ep):
        food = 0
        for _ in range(episodes):
                epsilon = _ / episodes
                self.snake.reset()
                dead = False
                count = 0
                while not dead and count < 50:
                    count += 1
                    possible_actions = [UP, RIGHT, LEFT]
                    if random.random() < epsilon:
                        idx = self.get_trained_move()
                        action = possible_actions[idx]
                    else:
                        action = random.choice(possible_actions)
                         # self.snake.move(action)
                    next_snake = self.snake.copy()
                    next_snake.move(action)
                    dead, food_eaten = next_snake.update()
                    next_q_val = self.get_q_values(next_snake.get_state())
                    if food_eaten:
                        reward = 100
                        food += 1
                        count = 0
                    else:
                        reward = 0
                    if dead:
                        reward = -100
                    q_val = self.get_q_values(self.snake.get_state())
                    q_val[action] += lr * (reward + (dis * max(next_q_val)) - q_val[action])

                    self.snake = next_snake
                    # print(count)
                    # print(self.snake.snake_size)
                    if self.snake.snake_size == self.size ** 2 - 1:
                        break
                print(f'episode:{_} with epsilon:{epsilon}')

    def get_trained_move(self):
        moves = self.get_q_values(self.snake.get_state())
        return moves.index(max(moves))



