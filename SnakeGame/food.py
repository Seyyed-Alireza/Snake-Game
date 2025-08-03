import numpy as np

FOODS = ['🍗', '🎂', '🌭', '🥨', '🧀', '🍊', '🍉', '🍒', '🥕']
# xx = 240
def food_coordinate(width, height, step):
    global FOODS
    food_imoji = np.random.choice(FOODS)
    return (np.random.choice(range(0, width, step)), np.random.choice(range(0, height, step)), food_imoji)
