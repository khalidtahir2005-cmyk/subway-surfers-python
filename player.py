# player.py
import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # إنشاء شخصية ثلاثية الأبعاد (مظهر احترافي)
        self.create_character()
        
        # الموقع
        self.rect = self.image.get_rect()
        self.rect.x = 150
        self.rect.y = GROUND_LEVEL - PLAYER_HEIGHT
        
        # الفيزياء
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = True
        self.is_sliding = False
        self.is_jumping = False
        
        # الصحة
        self.health = 100
        self.max_health = 100
        
        # المؤقتات
        self.invincible_timer = 0
        self.slide_timer = 0
        
        # حركة
        self.facing_right = True
        self.move_left_flag = False
        self.move_right_flag = False
        
    def create_character(self):
        """إنشاء شخصية احترافية بألوان وتفاصيل"""
        # الجسم الرئيسي
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
        
        # الجسم (قبعة)
        body_color = (50, 200, 255)  # أزرق فاتح
        pygame.draw.ellipse(self.image, body_color, (2, 10, 31, 35))
        
        # الرأس
        head_color = (255, 220, 180)  # لون بشرة
        pygame.draw.circle(self.image, head_color, (17, 15), 15)
        
        # العينين
        pygame.draw.circle(self.image, WHITE, (22, 12), 5)
        pygame.draw.circle(self.image, WHITE, (10, 12), 5)
        pygame.draw.circle(self.image, BLACK, (24, 12), 3)
        pygame.draw.circle(self.image, BLACK, (12, 12), 3)
        
        # القبعة
        hat_color = (255, 50, 50)  # أحمر
        pygame.draw.rect(self.image, hat_color, (2, 0, 31, 12))
        pygame.draw.rect(self.image, hat_color, (8, -5, 19, 8))
        
        # الفم (ابتسامة)
        pygame.draw.arc(self.image, BLACK, (8, 20, 18, 8), 0, 3.14, 2)
        
        # الأرجل
        leg_color = (50, 150, 200)
        pygame.draw.rect(self.image, leg_color, (5, 45, 8, 10))
        pygame.draw.rect(self.image, leg_color, (22, 45, 8, 10))
        
        # الأحذية
        shoe_color = (200, 50, 50)
        pygame.draw.rect(self.image, shoe_color, (3, 52, 12, 5))
        pygame.draw.rect(self.image, shoe_color, (20, 52, 12, 5))
        
    def update(self):
        """تحديث اللاعب"""
        self.handle_movement()
        self.apply_physics()
        self.check_collisions()
        self.update_timers()
        
    def handle_movement(self):
        """معالجة الحركة"""
        # حركة أفقية
        if self.move_left_flag:
            self.vel_x = -PLAYER_SPEED
            self.facing_right = False
        elif self.move_right_flag:
            self.vel_x = PLAYER_SPEED
            self.facing_right = True
        else:
            self.vel_x *= 0.85  # احتكاك
            
        # حركة عمودية
        if self.is_jumping and self.on_ground and not self.is_sliding:
            self.vel_y = JUMP_FORCE
            self.on_ground = False
            self.is_jumping = False
            
    def apply_physics(self):
        """تطبيق الفيزياء"""
        # الجاذبية
        self.vel_y += GRAVITY
        if self.vel_y > 15:
            self.vel_y = 15
            
        # تحديث الموقع
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        # حدود الشاشة
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.vel_x = 0
            
        # الأرض
        if self.rect.bottom >= GROUND_LEVEL:
            self.rect.bottom = GROUND_LEVEL
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False
            
    def check_collisions(self):
        """التحقق من التصادمات مع الأرض والعوائق"""
        pass  # يتم التعامل معها في main
        
    def update_timers(self):
        """تحديث المؤقتات"""
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
            
        if self.slide_timer > 0:
            self.slide_timer -= 1
            if self.slide_timer == 0:
                self.unslide()
                
    def jump(self):
        """القفز"""
        if self.on_ground and not self.is_sliding:
            self.is_jumping = True
            
    def slide(self):
        """الانزلاق"""
        if not self.is_sliding and self.on_ground:
            self.is_sliding = True
            self.slide_timer = 30  # مدة الانزلاق
            # تصغير حجم اللاعب
            self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, SLIDE_HEIGHT))
            self.rect.height = SLIDE_HEIGHT
            self.rect.y = GROUND_LEVEL - SLIDE_HEIGHT
            
    def unslide(self):
        """العودة من الانزلاق"""
        if self.is_sliding:
            self.is_sliding = False
            self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
            self.rect.height = PLAYER_HEIGHT
            self.rect.y = GROUND_LEVEL - PLAYER_HEIGHT
            
    def move_left(self, pressed=True):
        """التحرك لليسار"""
        self.move_left_flag = pressed
        if pressed:
            self.facing_right = False
            
    def move_right(self, pressed=True):
        """التحرك لليمين"""
        self.move_right_flag = pressed
        if pressed:
            self.facing_right = True
            
    def take_damage(self, damage=10):
        """أخذ ضرر"""
        if self.invincible_timer == 0:
            self.health -= damage
            self.invincible_timer = 60  # ثانية واحدة من الحصانة
            if self.health < 0:
                self.health = 0
                
    def heal(self, amount=10):
        """الشفاء"""
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
            
    def is_dead(self):
        """التحقق من الموت"""
        return self.health <= 0