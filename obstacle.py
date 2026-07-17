# obstacle.py
import pygame
import random
from settings import *

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed_multiplier=1.0):
        super().__init__()
        
        # أنواع العوائق
        self.type = random.choice(['train', 'barrier', 'cone', 'box'])
        self.create_obstacle()
        
        # الموقع
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + random.randint(50, 200)
        self.rect.y = GROUND_LEVEL - self.rect.height
        
        # السرعة
        self.speed = random.uniform(OBSTACLE_MIN_SPEED, OBSTACLE_MAX_SPEED) * speed_multiplier
        
        # إضافات
        self.damage = 20
        self.points = 5
        
    def create_obstacle(self):
        """إنشاء عقبة حسب النوع"""
        if self.type == 'train':
            self.image = pygame.Surface((60, 40), pygame.SRCALPHA)
            # عربة قطار
            pygame.draw.rect(self.image, (100, 100, 200), (0, 0, 60, 40))
            pygame.draw.rect(self.image, (50, 50, 150), (5, 5, 15, 30))
            pygame.draw.rect(self.image, (50, 50, 150), (40, 5, 15, 30))
            pygame.draw.circle(self.image, (200, 200, 50), (30, 40), 8)
            
        elif self.type == 'barrier':
            self.image = pygame.Surface((40, 50), pygame.SRCALPHA)
            # حاجز
            pygame.draw.rect(self.image, (200, 50, 50), (0, 0, 40, 50))
            pygame.draw.rect(self.image, (255, 200, 50), (5, 5, 30, 10))
            pygame.draw.rect(self.image, (255, 200, 50), (5, 20, 30, 10))
            pygame.draw.rect(self.image, (255, 200, 50), (5, 35, 30, 10))
            
        elif self.type == 'cone':
            self.image = pygame.Surface((30, 40), pygame.SRCALPHA)
            # مخروط
            pygame.draw.polygon(self.image, (255, 150, 50), [(15, 0), (0, 40), (30, 40)])
            pygame.draw.polygon(self.image, (255, 200, 50), [(15, 5), (5, 35), (25, 35)])
            
        else:  # box
            self.image = pygame.Surface((35, 35), pygame.SRCALPHA)
            # صندوق
            pygame.draw.rect(self.image, (150, 100, 50), (0, 0, 35, 35))
            pygame.draw.rect(self.image, (100, 50, 20), (5, 5, 25, 25))
            pygame.draw.line(self.image, (100, 50, 20), (17, 0), (17, 35), 2)
            pygame.draw.line(self.image, (100, 50, 20), (0, 17), (35, 17), 2)
            
        # إضافة حدود
        pygame.draw.rect(self.image, BLACK, self.image.get_rect(), 2)
        
    def update(self):
        """تحريك العقبة"""
        self.rect.x -= self.speed