import random
from Pygame import *

UP = 0
RIGHT = 1
LEFT = 2


class SnakeGame:
    def __init__(self, board_size=6):
        self.board_size = board_size
        self.res_x = int(width / self.board_size)
        self.res_y = int(height / self.board_size)

        self.food_pos = None, None

        self.x, self.y = int(board_size / 2), int(board_size / 2)
        self.pos_memory = []
        self.snake_size = 3
        self.x_speed, self.y_speed = 0, -1

    def copy(self):
        new = SnakeGame(self.board_size)
        new.food_pos = self.food_pos
        new.x, new.y = self.x, self.y
        new.pos_memory = self.pos_memory.copy()
        new.snake_size = self.snake_size
        new.x_speed, new.y_speed = self.x_speed, self.y_speed
        return new

    def change_food_pos(self):
        pos_found = False
        while not pos_found:
            x, y = random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)
            if (x, y) != (self.x, self.y):
                if (x, y) not in self.pos_memory:
                    pos_found = True
        self.food_pos = (x, y)

    def show(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if (i, j) == (self.x, self.y):  # head
                    pygame.draw.rect(screen, (255, 255, 0), ((i * self.res_x, j * self.res_y),
                                                           (self.res_x, self.res_y)))
                if (i, j) == self.food_pos:
                    pygame.draw.rect(screen, (255, 0, 0), ((i * self.res_x, j * self.res_y),
                                                           (self.res_x, self.res_y)))
                if (i, j) in self.pos_memory:
                    pygame.draw.rect(screen, (255, 255, 255), ((i * self.res_x, j * self.res_y),
                                                               (self.res_x, self.res_y)))

    def input(self, keytick):
        pressed = False
        if keytick > 20:
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and not pressed:
                pressed = True
            elif key[pygame.K_RIGHT] and not pressed:
                if self.x_speed != 0:
                    if self.x_speed == 1:
                        self.y_speed = 1
                    else:
                        self.y_speed = -1
                    self.x_speed = 0
                else:
                    if self.y_speed == 1:
                        self.x_speed = -1
                    else:
                        self.x_speed = 1
                    self.y_speed = 0
                pressed = True
            elif key[pygame.K_LEFT] and not pressed:
                if self.x_speed != 0:
                    if self.x_speed == 1:
                        self.y_speed = -1
                    else:
                        self.y_speed = 1
                    self.x_speed = 0
                else:
                    if self.y_speed == 1:
                        self.x_speed = 1
                    else:
                        self.x_speed = -1
                    self.y_speed = 0
                pressed = True
        return pressed

    def move(self, action):
        if action == UP:
            pass
        elif action == RIGHT:
            if self.x_speed != 0:
                if self.x_speed == 1:
                    self.y_speed = 1
                else:
                    self.y_speed = -1
                self.x_speed = 0
            else:
                if self.y_speed == 1:
                    self.x_speed = -1
                else:
                    self.x_speed = 1
                self.y_speed = 0
        elif action == LEFT:
            if self.x_speed != 0:
                if self.x_speed == 1:
                    self.y_speed = -1
                else:
                    self.y_speed = 1
                self.x_speed = 0
            else:
                if self.y_speed == 1:
                    self.x_speed = 1
                else:
                    self.x_speed = -1
                self.y_speed = 0

    def update(self):
        self.pos_memory.append((self.x, self.y))
        self.x, self.y = self.x + self.x_speed, self.y + self.y_speed
        dont = True
        if self.food_pos == (self.x, self.y):
            self.snake_size += 1
            self.change_food_pos()
            dont = False
        food_eaten = not dont
        if len(self.pos_memory) > self.snake_size - 1 and dont:
            self.pos_memory.pop(0)
        # if food_eaten:
        #     self.snake_size += 1

        dead = False
        if (self.x, self.y) in self.pos_memory:
            dead = True
        if self.x >= self.board_size or self.x < 0:
            dead = True
        if self.y >= self.board_size or self.y < 0:
            dead = True
        # print(self.x, self.y)
        return dead, food_eaten

    def reset(self):
        self.food_pos = None, None
        self.change_food_pos()
        self.x, self.y = int(self.board_size / 2), int(self.board_size / 2)
        self.pos_memory = []
        self.snake_size = 3
        self.x_speed, self.y_speed = 0, -1

    def get_state(self):
        def dir_danger(self, pos, dir):
            if (pos[0] + dir[0], pos[1] + dir[1]) in self.pos_memory:
                return 1
            else:
                return 0
        state = [dir_danger(self, (self.x, self.y), (self.x_speed, self.y_speed))]  # 1 block ahead sight block
        if self.x_speed != 0:
            if self.x_speed == 1:
                new_y_speed = 1
            else:
                new_y_speed = -1
            new_x_speed = 0
        else:
            if self.y_speed == 1:
                new_x_speed = -1
            else:
                new_x_speed = 1
            new_y_speed = 0
        state.append(dir_danger(self, (self.x,self.y), (new_x_speed, new_y_speed)))
        if self.x_speed != 0:
            if self.x_speed == 1:
                new_y_speed = -1
            else:
                new_y_speed = 1
            new_x_speed = 0
        else:
            if self.y_speed == 1:
                new_x_speed = 1
            else:
                new_x_speed = -1
            new_y_speed = 0
        state.append(dir_danger(self, (self.x,self.y), (new_x_speed, new_y_speed)))

        # if self.x != self.food_pos[0]:
        #     if self.x > self.food_pos[0]:
        #         state.append(1)
        #         state.append(0)
        #     else:
        #         state.append(0)
        #         state.append(1)
        # if self.y != self.food_pos[1]:
        #     if self.y > self.food_pos[1]:
        #         state.append(1)
        #         state.append(0)
        #     else:
        #         state.append(0)
        #         state.append(1)
        relative_pos = self.food_pos[0] - self.x, self.food_pos[1] - self.y  # relative position
        if relative_pos[0] > 0:
            state.append(1)
            state.append(0)
        elif relative_pos[0] < 0:
            state.append(0)
            state.append(1)
        else:
            state.append(0)
            state.append(0)
        if relative_pos[1] > 0:
            state.append(1)
            state.append(0)
        elif relative_pos[1] < 0:
            state.append(0)
            state.append(1)
        else:
            state.append(0)
            state.append(0)

        state.append(self.x_speed)  # self speed direction
        state.append(self.y_speed)

        return tuple(state)

