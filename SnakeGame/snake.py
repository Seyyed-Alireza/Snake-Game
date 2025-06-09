import pygame
import random
from food import food_coordinate
from score import add_score
from sound import eat_sound


class Tail:
    def __init__(self, x_now, y_now, x_before, y_before):
        self.x_now = x_now
        self.y_now = y_now
        self.moves_before = []
        self.x_before = x_before
        self.y_before = y_before
        self.color = (random.randint(70, 225), random.randint(70, 225), random.randint(70, 225))

def reset_snake():
    global go_right 
    global go_up 
    global go_left 
    global go_down 
    global before_move 
    global move_done 
    global x_before 
    global y_before 
    global moves_before
    go_right = False
    go_up = False
    go_left = False
    go_down = False
    before_move = None
    move_done = True
    x_before = None
    y_before = None
    moves_before = []

go_right = False
go_up = False
go_left = False
go_down = False
before_move = None
move_done = True
x_before = None
y_before = None
moves_before = []
move_step = 3

def food_ate(width, height, step, tails):
    global x_before
    global y_before
    global FOODS
    add_score(1)
    food_x, food_y, food_imoji = food_coordinate(width, height, step)
    if len(tails) != 0:
        # if tails[-1].x_before != None and tails[-1].y_before == None:
        tail = Tail(tails[-1].x_before, tails[-1].y_before, None, None)
        tails.append(tail)
    else:
        tail = Tail(x_before, y_before, None, None)
        tails.append(tail)
    return (food_x, food_y, tails, food_imoji)

def game(width, height, step, x, y, food_x, food_y, tails, food_imoji):
    global go_right
    global go_up 
    global go_left 
    global go_down 
    global before_move 
    global move_done 
    global x_before
    global y_before
    global moves_before
    global move_step

    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN] and not go_up and move_done:
        before_move = 'gr' if go_right else 'gl'
        go_up, go_right, go_down, go_left = (False, False, True, False)
        move_done = False
    if keys[pygame.K_RIGHT] and not go_left and move_done:
        before_move = 'gu' if go_up else 'gd'
        go_up, go_right, go_down, go_left = (False, True, False, False)
        move_done = False
    if keys[pygame.K_UP] and not go_down and move_done:
        before_move = 'gr' if go_right else 'gl'
        go_up, go_right, go_down, go_left = (True, False, False, False)
        move_done = False
    if keys[pygame.K_LEFT] and not go_right and move_done:
        before_move = 'gu' if go_up else 'gd'
        go_up, go_right, go_down, go_left = (False, False, False, True)
        move_done = False
    if x < 0 or y < 0 or x + step > width or y + step > height:
        return (x, y, food_x, food_y, True, tails, food_imoji, 'gu' if go_up else 'gr' if go_right else 'gd' if go_down else 'gl' if go_left else None)

    if go_up:
        if x % step == 0:
            y -= move_step
            move_done = True
            if y % step == 0:
                y_before = y 
                x_before = x
            if y < food_y + step and y >= food_y and x == food_x:
                eat_sound()
                food_x, food_y, tails, food_imoji = food_ate(width, height, step, tails)
        elif before_move == 'gr':
            x += move_step
        elif before_move == 'gl':
            x -= move_step

    elif go_right:
        if y % step == 0:
            x += move_step
            move_done = True
            if x % step == 0:
                x_before = x 
                y_before = y
            if x + step > food_x and x <= food_x and y == food_y:
                eat_sound()
                food_x, food_y, tails, food_imoji = food_ate(width, height, step, tails)
        elif before_move == 'gu':
            y -= move_step
        elif before_move == 'gd':
            y += move_step

    elif go_down:
        if x % step == 0:
            y += move_step
            move_done = True
            if y % step == 0:
                y_before = y
                x_before = x
            if y + step > food_y and y <= food_y and x == food_x:
                eat_sound()
                food_x, food_y, tails, food_imoji = food_ate(width, height, step, tails)
        elif before_move == 'gr':
            x += move_step
        elif before_move == 'gl':
            x -= move_step

    elif go_left:
        if y % step == 0:
            x -= move_step
            move_done = True
            if x % step == 0:
                x_before = x
                y_before = y
            if x < food_x + step and x >= food_x and y == food_y:
                eat_sound()
                food_x, food_y, tails, food_imoji = food_ate(width, height, step, tails)
        elif before_move == 'gu':
            y -= move_step
        elif before_move == 'gd':
            y += move_step

    if len(moves_before) >= step // 3 - 2:
        x_before, y_before = moves_before[0]
        moves_before.pop(0)
    moves_before.append([x, y])

    if len(tails) != 0:
        if len(tails[0].moves_before) >= step // 3 - 2:
            tails[0].x_before, tails[0].y_before = tails[0].moves_before[0]
            tails[0].moves_before.pop(0)
        tails[0].moves_before.append([tails[0].x_now, tails[0].y_now])
        tails[0].x_now = x_before
        tails[0].y_now = y_before
        for i in range(1, len(tails)):
            if len(tails[i].moves_before) >= step // 3 - 2:
                tails[i].x_before, tails[i].y_before = tails[i].moves_before[0]
                tails[i].moves_before.pop(0)
            tails[i].moves_before.append([tails[i].x_now, tails[i].y_now])
            tails[i].x_now = tails[i - 1].x_before
            tails[i].y_now = tails[i - 1].y_before

    return (x, y, food_x, food_y, False, tails, food_imoji, 'gu' if go_up else 'gr' if go_right else 'gd' if go_down else 'gl' if go_left else None)
