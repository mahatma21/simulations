import math

CYAN = (0, 245, 245)
LIGHTING_COLOR = (0, 40, 40)
BG_COLOR = (20, 10, 50)

SCREEN_SIZE = WIN_SIZE = 1600, 900
SCREEN_MID = WIN_MID = tuple(n / 2 for n in WIN_SIZE)
SCREEN_LENGTH = math.sqrt(SCREEN_SIZE[0] ** 2 + SCREEN_SIZE[1] ** 2)