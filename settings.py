# settings.py
import pygame

# إعدادات الشاشة
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650
FPS = 60
GROUND_LEVEL = 550

# الألوان
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 0)
PURPLE = (150, 50, 200)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)

# ألوان الخلفية (تدرج السماء)
SKY_TOP = (135, 206, 235)
SKY_BOTTOM = (200, 230, 255)

# إعدادات اللاعب
PLAYER_WIDTH = 35
PLAYER_HEIGHT = 55
PLAYER_SPEED = 6
JUMP_FORCE = -14
GRAVITY = 0.7
SLIDE_HEIGHT = 25

# إعدادات العوائق
OBSTACLE_MIN_SPEED = 4
OBSTACLE_MAX_SPEED = 8
OBSTACLE_SPAWN_RATE = 120  # frames بين كل عقبة

# إعدادات العملات
COIN_SPAWN_RATE = 80
COIN_VALUE = 10

# إعدادات الصعوبة
DIFFICULTY_LEVELS = {
    1: {"speed": 4, "spawn_rate": 120, "coins": 80},
    2: {"speed": 5, "spawn_rate": 100, "coins": 70},
    3: {"speed": 6, "spawn_rate": 80, "coins": 60},
    4: {"speed": 7, "spawn_rate": 60, "coins": 50},
    5: {"speed": 8, "spawn_rate": 40, "coins": 40},
}