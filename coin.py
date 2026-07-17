# coin.py
import pygame
import math
from settings import *

class Coin(pygame.sprite.Sprite):
    def __init__(self, x=None, y=None):
        super().__init__()
        
        # إنشاء عملة ذهبية
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.create_coin()
        
        # الموقع
        self.rect = self.image.get_rect()
        if x is None:
            self.rect.x = SCREEN_WIDTH + random.randint(50, 300)
        else:
            self.rect.x = x
            
        if y is None:
            self.rect.y = random.randint(200, GROUND_LEVEL - 50)
        else:
            self.rect.y = y
            
        # تأثيرات
        self.animation_frame = 0
        self.value = COIN_VALUE
        
    def create_coin(self):
        """إنشاء عملة ذهبية مع تأثير لمعان"""
        # الدائرة الذهبية
        pygame.draw.circle(self.image, (255, 215, 0), (10, 10), 9)
        pygame.draw.circle(self.image, (255, 200, 50), (10, 10), 7)
        
        # نقش العملة
        pygame.draw.circle(self.image, (200, 150, 0), (10, 10), 5, 1)
        pygame.draw.line(self.image, (200, 150, 0), (5, 10), (15, 10), 1)
        
        # تأثير اللمعان
        pygame.draw.arc(self.image, (255, 255, 200), (2, 2, 12, 12), 0, 1.5, 2)
        
        # إضافة إطار
        pygame.draw.circle(self.image, (200, 150, 0), (10, 10), 9, 2)
        
    def update(self):
        """تحديث العملة (حركة ودوران)"""
        self.rect.x -= 3
        
        # تأثير الدوران (تغيير الحجم)
        self.animation_frame += 0.1
        scale = 1 + 0.2 * math.sin(self.animation_frame)
        center = self.rect.center
        self.rect.width = int(20 * scale)
        self.rect.height = int(20 * scale)
        self.rect.center = center