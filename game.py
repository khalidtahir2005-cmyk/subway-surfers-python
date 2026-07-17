# game.py
import pygame
import sys
import random
from settings import *
from player import Player
from obstacle import Obstacle
from coin import Coin

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        # إعدادات الصوت
        self.setup_sounds()
        
        # الشاشة
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🏃 Subway Surfers - Python Edition")
        pygame.display.set_icon(self.create_icon())
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.game_over_state = False
        
        # النتائج
        self.score = 0
        self.high_score = self.load_high_score()
        self.coins = 0
        self.level = 1
        self.distance = 0
        
        # المجموعات
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.coins_group = pygame.sprite.Group()
        
        # إنشاء اللاعب
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # مؤقتات التوليد
        self.obstacle_timer = 0
        self.coin_timer = 0
        self.difficulty_timer = 0
        
        # الخلفية
        self.bg_scroll = 0
        
        # القائمة
        self.show_menu = True
        
        # الخطوط
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
    def setup_sounds(self):
        """إعداد المؤثرات الصوتية"""
        try:
            self.jump_sound = pygame.mixer.Sound("assets/sounds/jump.wav")
            self.coin_sound = pygame.mixer.Sound("assets/sounds/coin.wav")
            self.game_over_sound = pygame.mixer.Sound("assets/sounds/game_over.wav")
        except:
            # إذا ما كانتش الملفات الصوتية موجودة
            self.jump_sound = None
            self.coin_sound = None
            self.game_over_sound = None
            
    def create_icon(self):
        """إنشاء أيقونة اللعبة"""
        icon = pygame.Surface((32, 32))
        icon.fill(BLUE)
        pygame.draw.circle(icon, YELLOW, (16, 16), 10)
        pygame.draw.rect(icon, RED, (8, 8, 16, 16), 2)
        return icon
        
    def load_high_score(self):
        """تحميل أعلى نتيجة"""
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read())
        except:
            return 0
            
    def save_high_score(self):
        """حفظ أعلى نتيجة"""
        try:
            with open("highscore.txt", "w") as f:
                f.write(str(self.high_score))
        except:
            pass
            
    def handle_events(self):
        """معالجة الأحداث"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_p and not self.game_over_state:
                    self.paused = not self.paused
                elif event.key == pygame.K_SPACE and self.game_over_state:
                    self.reset_game()
                elif event.key == pygame.K_RETURN and self.show_menu:
                    self.show_menu = False
                    
            # التحكم باللاعب
            if not self.paused and not self.game_over_state and not self.show_menu:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                        self.player.jump()
                        if self.jump_sound:
                            self.jump_sound.play()
                    elif event.key == pygame.K_DOWN:
                        self.player.slide()
                    elif event.key == pygame.K_LEFT:
                        self.player.move_left(True)
                    elif event.key == pygame.K_RIGHT:
                        self.player.move_right(True)
                        
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.player.move_left(False)
                    elif event.key == pygame.K_RIGHT:
                        self.player.move_right(False)
                        
    def update(self):
        """تحديث اللعبة"""
        if self.paused or self.game_over_state or self.show_menu:
            return
            
        # تحديث كل السبرايتات
        self.all_sprites.update()
        self.obstacles.update()
        self.coins_group.update()
        
        # تحديث المسافة
        self.distance += 0.1
        
        # توليد العوائق
        self.obstacle_timer += 1
        speed_mult = DIFFICULTY_LEVELS[min(self.level, 5)]["speed"] / 4
        spawn_rate = DIFFICULTY_LEVELS[min(self.level, 5)]["spawn_rate"]
        
        if self.obstacle_timer >= spawn_rate:
            self.obstacle_timer = 0
            if random.random() < 0.7:  # 70% فرصة لتوليد عقبة
                obstacle = Obstacle(speed_mult)
                self.all_sprites.add(obstacle)
                self.obstacles.add(obstacle)
                
        # توليد العملات
        self.coin_timer += 1
        coin_rate = DIFFICULTY_LEVELS[min(self.level, 5)]["coins"]
        
        if self.coin_timer >= coin_rate:
            self.coin_timer = 0
            if random.random() < 0.5:  # 50% فرصة لتوليد عملات
                # توليد مجموعة عملات
                num_coins = random.randint(1, 5)
                for i in range(num_coins):
                    coin = Coin(
                        x=SCREEN_WIDTH + 50 + i * 30,
                        y=random.randint(200, GROUND_LEVEL - 50)
                    )
                    self.all_sprites.add(coin)
                    self.coins_group.add(coin)
                    
        # تحديث الصعوبة
        self.difficulty_timer += 1
        if self.difficulty_timer >= 600:  # كل 10 ثواني
            self.difficulty_timer = 0
            if self.level < 5:
                self.level += 1
                
        # التصادم مع العوائق
        if pygame.sprite.spritecollide(self.player, self.obstacles, True):
            self.player.take_damage(20)
            if self.player.is_dead():
                self.game_over()
                
        # جمع العملات
        collected = pygame.sprite.spritecollide(self.player, self.coins_group, True)
        for coin in collected:
            self.coins += coin.value
            self.score += coin.value
            if self.coin_sound:
                self.coin_sound.play()
                
        # تحديث النتيجة
        self.score += 1
        
        # تحديث أعلى نتيجة
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
            
        # إزالة العناصر خارج الشاشة
        for sprite in self.all_sprites:
            if sprite.rect.right < -100:
                sprite.kill()
                
    def render(self):
        """رسم كل شيء"""
        # الخلفية المتدرجة
        for y in range(SCREEN_HEIGHT):
            t = y / SCREEN_HEIGHT
            color = (
                SKY_TOP[0] + (SKY_BOTTOM[0] - SKY_TOP[0]) * t,
                SKY_TOP[1] + (SKY_BOTTOM[1] - SKY_TOP[1]) * t,
                SKY_TOP[2] + (SKY_BOTTOM[2] - SKY_TOP[2]) * t
            )
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
            
        # الأرض
        pygame.draw.rect(self.screen, (50, 150, 50), (0, GROUND_LEVEL, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_LEVEL))
        pygame.draw.rect(self.screen, (100, 200, 100), (0, GROUND_LEVEL, SCREEN_WIDTH, 5))
        
        # خطوط السكة الحديدية
        for x in range(-50, SCREEN_WIDTH + 50, 60):
            x_pos = (x - self.bg_scroll) % (SCREEN_WIDTH + 100) - 50
            pygame.draw.rect(self.screen, (80, 80, 80), (x_pos, GROUND_LEVEL + 10, 8, 40))
            pygame.draw.rect(self.screen, (80, 80, 80), (x_pos + 20, GROUND_LEVEL + 10, 8, 40))
            
        # رسم السبرايتات
        self.all_sprites.draw(self.screen)
        
        # رسم الـ UI
        self.draw_ui()
        
        # رسم القوائم
        if self.show_menu:
            self.draw_menu()
        elif self.paused:
            self.draw_pause()
        elif self.game_over_state:
            self.draw_game_over()
            
        # تحديث الشاشة
        pygame.display.flip()
        
    def draw_ui(self):
        """رسم واجهة المستخدم"""
        # نقاط
        score_text = self.font_medium.render(f"🏆 {self.score}", True, WHITE)
        score_rect = score_text.get_rect(topleft=(20, 20))
        pygame.draw.rect(self.screen, (0, 0, 0, 128), score_rect.inflate(20, 10))
        pygame.draw.rect(self.screen, WHITE, score_rect.inflate(20, 10), 2)
        self.screen.blit(score_text, score_rect)
        
        # عملات
        coin_text = self.font_small.render(f"🪙 {self.coins}", True, YELLOW)
        coin_rect = coin_text.get_rect(topleft=(20, 70))
        pygame.draw.rect(self.screen, (0, 0, 0, 128), coin_rect.inflate(20, 10))
        self.screen.blit(coin_text, coin_rect)
        
        # مستوى
        level_text = self.font_small.render(f"Level {self.level}", True, CYAN)
        level_rect = level_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        pygame.draw.rect(self.screen, (0, 0, 0, 128), level_rect.inflate(20, 10))
        self.screen.blit(level_text, level_rect)
        
        # أعلى نتيجة
        high_text = self.font_small.render(f"Best: {self.high_score}", True, YELLOW)
        high_rect = high_text.get_rect(topright=(SCREEN_WIDTH - 20, 60))
        pygame.draw.rect(self.screen, (0, 0, 0, 128), high_rect.inflate(20, 10))
        self.screen.blit(high_text, high_rect)
        
        # صحة اللاعب
        health_bar_width = 150
        health_ratio = self.player.health / self.player.max_health
        health_x = SCREEN_WIDTH // 2 - health_bar_width // 2
        health_y = 20
        
        pygame.draw.rect(self.screen, RED, (health_x, health_y, health_bar_width, 20))
        pygame.draw.rect(self.screen, GREEN, (health_x, health_y, health_bar_width * health_ratio, 20))
        pygame.draw.rect(self.screen, WHITE, (health_x, health_y, health_bar_width, 20), 2)
        
        health_text = self.font_small.render(f"❤️ {self.player.health}", True, WHITE)
        health_rect = health_text.get_rect(center=(SCREEN_WIDTH // 2, health_y + 10))
        self.screen.blit(health_text, health_rect)
        
        # تعليمات
        if self.distance < 100:
            controls_text = self.font_small.render("⬆️ Jump | ⬇️ Slide | ⬅️➡️ Move | P Pause", True, WHITE)
            controls_rect = controls_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
            pygame.draw.rect(self.screen, (0, 0, 0, 128), controls_rect.inflate(20, 10))
            self.screen.blit(controls_text, controls_rect)
            
    def draw_menu(self):
        """رسم قائمة البداية"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # العنوان
        title_text = self.font_large.render("🏃 SUBWAY SURFERS", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # النسخة
        version_text = self.font_small.render("Python Edition v2.0", True, WHITE)
        version_rect = version_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(version_text, version_rect)
        
        # زر البداية
        start_text = self.font_medium.render("Press ENTER to Start", True, GREEN)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
        pygame.draw.rect(self.screen, (0, 100, 0), start_rect.inflate(40, 20), 3)
        self.screen.blit(start_text, start_rect)
        
        # أعلى نتيجة
        high_text = self.font_small.render(f"🏆 Best Score: {self.high_score}", True, YELLOW)
        high_rect = high_text.get_rect(center=(SCREEN_WIDTH // 2, 450))
        self.screen.blit(high_text, high_rect)
        
        # تعليمات
        controls = [
            "⬆️ / SPACE: Jump",
            "⬇️: Slide",
            "⬅️ ➡️: Move",
            "P: Pause"
        ]
        y = 500
        for text in controls:
            control_text = self.font_small.render(text, True, WHITE)
            control_rect = control_text.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(control_text, control_rect)
            y += 30
            
    def draw_pause(self):
        """رسم شاشة الإيقاف المؤقت"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.font_large.render("⏸ PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(pause_text, pause_rect)
        
        resume_text = self.font_small.render("Press P to Resume", True, CYAN)
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(resume_text, resume_rect)
        
    def draw_game_over(self):
        """رسم شاشة نهاية اللعبة"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # النص الرئيسي
        game_over_text = self.font_large.render("💀 GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(game_over_text, game_over_rect)
        
        # النتيجة
        score_text = self.font_medium.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
        self.screen.blit(score_text, score_rect)
        
        # العملات
        coins_text = self.font_medium.render(f"🪙 Coins: {self.coins}", True, YELLOW)
        coins_rect = coins_text.get_rect(center=(SCREEN_WIDTH // 2, 310))
        self.screen.blit(coins_text, coins_rect)
        
        # أعلى نتيجة
        high_text = self.font_medium.render(f"🏆 Best: {self.high_score}", True, YELLOW)
        high_rect = high_text.get_rect(center=(SCREEN_WIDTH // 2, 370))
        self.screen.blit(high_text, high_rect)
        
        # المستوى
        level_text = self.font_small.render(f"Level Reached: {self.level}", True, CYAN)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, 420))
        self.screen.blit(level_text, level_rect)
        
        # إعادة البداية
        restart_text = self.font_medium.render("Press SPACE to Restart", True, GREEN)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 500))
        pygame.draw.rect(self.screen, (0, 100, 0), restart_rect.inflate(40, 20), 3)
        self.screen.blit(restart_text, restart_rect)
        
        # خروج
        quit_text = self.font_small.render("Press ESC to Quit", True, WHITE)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, 560))
        self.screen.blit(quit_text, quit_rect)
        
    def game_over(self):
        """نهاية اللعبة"""
        self.game_over_state = True
        if self.game_over_sound:
            self.game_over_sound.play()
            
    def reset_game(self):
        """إعادة تعيين اللعبة"""
        # إعادة تعيين النتائج
        self.score = 0
        self.coins = 0
        self.level = 1
        self.distance = 0
        self.obstacle_timer = 0
        self.coin_timer = 0
        self.difficulty_timer = 0
        
        # إعادة تعيين اللاعب
        self.player.health = self.player.max_health
        self.player.rect.x = 150
        self.player.rect.y = GROUND_LEVEL - PLAYER_HEIGHT
        self.player.vel_x = 0
        self.player.vel_y = 0
        self.player.on_ground = True
        self.player.is_dead = False
        
        # تنظيف المجموعات
        self.all_sprites.empty()
        self.obstacles.empty()
        self.coins_group.empty()
        
        # إضافة اللاعب مرة أخرى
        self.all_sprites.add(self.player)
        
        # إعادة تعيين الحالة
        self.game_over_state = False
        
    def run(self):
        """تشغيل اللعبة"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()