"""Crystal Cave Platformer - A simple Pygame Zero platformer game"""
import random
from pygame import Rect

WIDTH, HEIGHT = 800, 600
GRAVITY = 0.6

# Track whether the player is in menu, playing, or has won/lost
state = "menu"
sound_on = music_on = True
score = 0


class Character:
    """Parent class for all characters - handles sprite animation and position"""
    def __init__(self, x, y, idle_sprites, move_sprites):
        self.x = x
        self.y = y
        self.idle_sprites = idle_sprites
        self.move_sprites = move_sprites
        self.frame = 0
        self.moving = False
        self.facing_right = True
    
    def animate(self):
        self.frame = (self.frame + 0.15) % len(self.move_sprites)
    
    def get_rect(self):
        return Rect(self.x, self.y, 35, 35)
    
    def get_sprite(self):
        sprites = self.move_sprites if self.moving else self.idle_sprites
        return sprites[int(self.frame) % len(sprites)]


class Player(Character):
    """Ninja player with platformer some physics"""
    def __init__(self):
        idle = ['ninja_idle1', 'ninja_idle2']
        walk = ['ninja_walk1', 'ninja_walk2', 'ninja_walk3']
        super().__init__(50, 300, idle, walk)
        self.vx = self.vy = 0
        self.on_ground = False
    
    def update(self):
        # Check keyboard input to move left/right
        self.moving = False
        if keyboard.left:
            self.vx = -4
            self.moving = True
        elif keyboard.right:
            self.vx = 4
            self.moving = True
        else:
            self.vx = 0
        
        # Jump when space or up arrow is pressed and player is on ground
        if (keyboard.up or keyboard.space) and self.on_ground:
            self.vy = -13
            if sound_on:
                try: sounds.jump.play()
                except: pass
        
        # Apply gravity and update position based on velocity
        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy
        
        # Check if we're standing on a platform and handle landing/hitting head
        self.on_ground = False
        for plat in platforms:
            if self.get_rect().colliderect(plat):
                if self.vy > 0:  # Landing on platform from above
                    self.y = plat.top - 35
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:  # Jumping
                    self.y = plat.bottom
                    self.vy = 0
        
        self.x = max(0, min(self.x, WIDTH - 35))
        self.animate()


class Enemy(Character):
    """Walking or flying enemies that move back and forth in a patrol pattern"""
    def __init__(self, x, y, x1, x2, idle_sprites, move_sprites, flying=False):
        super().__init__(x, y, idle_sprites, move_sprites)
        self.x1, self.x2 = x1, x2
        self.speed = 2 if flying else 1.5
        self.flying = flying
        self.vy = 0
        self.moving = True
    
    def update(self):
        self.x += self.speed
        if self.x <= self.x1 or self.x >= self.x2:
            self.speed *= -1
            self.facing_right = not self.facing_right
        
        if not self.flying:
            self.vy += GRAVITY * 0.3
            self.y += self.vy
            for plat in platforms:
                if self.get_rect().colliderect(plat) and self.vy > 0:
                    self.y = plat.top - 35
                    self.vy = 0
        
        self.animate()


# Game objects that will be initialized when a new game starts
player = None
enemies = []
platforms = []
crystals = []


def init_game():
    """Initializing the game level"""
    global player, enemies, platforms, crystals, score, state
    
    player = Player()
    score = 0
    state = "playing"
    
    # Create the platformer level - arrange platforms from bottom to top
    platforms = [
        Rect(0, 560, 400, 40),      # Left ground
        Rect(500, 560, 300, 40),    # Right ground
        Rect(100, 470, 200, 25),    # First step
        Rect(350, 390, 200, 25),    # Second step
        Rect(100, 310, 200, 25),    # Third step
        Rect(400, 230, 200, 25),    # Fourth step
        Rect(150, 150, 200, 25),    # Fifth step
        Rect(500, 80, 150, 25)      # Goal platform
    ]
    
    # Set up enemy sprites and animations
    # Flying bats patrol the air
    # Slimes walk on platforms
    bat_idle = ['bat_idle1', 'bat_idle2'] 
    bat_move = ['bat_fly1', 'bat_fly2', 'bat_fly3']
    slime_idle = ['slime_idle1', 'slime_idle2']
    slime_move = ['slime_walk1', 'slime_walk2', 'slime_walk3']
    
    enemies = [
        Enemy(120, 400, 100, 280, bat_idle, bat_move, flying=True),      # Bat on platform 2
        Enemy(420, 160, 400, 580, bat_idle, bat_move, flying=True),      # Bat on platform 4
        Enemy(120, 440, 100, 270, slime_idle, slime_move),               # Slime on platform 2
        Enemy(420, 360, 350, 520, slime_idle, slime_move)                # Slime on platform 3
    ]
    
    # Collectible crystals
    crystals = [
        Rect(180, 445, 20, 20),     # On platform 2
        Rect(450, 365, 20, 20),     # On platform 3
        Rect(470, 205, 20, 20),     # On platform 4
        Rect(220, 125, 20, 20)      # On platform 5
    ]
    
    if music_on:
        try: music.play('background')
        except: pass


def update():
    """Called each frame - update player, enemies, check for collisions and win/lose conditions"""
    global state, score
    
    if state == "playing":
        player.update()
        
        for enemy in enemies:
            enemy.update()
            if player.get_rect().colliderect(enemy.get_rect()):
                state = "lose"
                if sound_on:
                    try: sounds.hit.play()
                    except: pass
                try: music.stop()
                except: pass
        
        for crystal in crystals[:]:
            if player.get_rect().colliderect(crystal):
                crystals.remove(crystal)
                score += 10
                if sound_on:
                    try: sounds.collect.play()
                    except: pass
        
        if player.x > 500 and player.y < 120:
            state = "win"
            try: music.stop()
            except: pass
        
        if player.y > HEIGHT:
            state = "lose"
            try: music.stop()
            except: pass


def draw():
    """Called in each frame - menu, game screen, or game over screen"""
    screen.clear()
    
    if state == "menu":
        screen.fill((20, 20, 40))
        screen.draw.text("NINJA CRYSTAL CAVE", center=(400, 100), fontsize=60, color=(150, 200, 255))
        screen.draw.text("PLATFORMER", center=(400, 150), fontsize=40, color=(100, 150, 200))
        
        draw_button(300, 220, 200, 50, "START GAME", (100, 150, 200))
        draw_button(300, 290, 200, 50, f"SOUND: {'ON' if sound_on else 'OFF'}", (100, 150, 200))
        draw_button(300, 360, 200, 50, f"MUSIC: {'ON' if music_on else 'OFF'}", (100, 150, 200))
        draw_button(300, 430, 200, 50, "EXIT", (100, 150, 200))
    
    elif state == "playing":
        screen.fill((30, 20, 50))
        for plat in platforms:
            screen.draw.filled_rect(plat, (80, 70, 60))
        for crystal in crystals:
            screen.draw.filled_rect(crystal, (150, 200, 255))
        
        draw_character(player)
        for enemy in enemies:
            draw_character(enemy)
        
        screen.draw.text(f"SCORE: {score}", (20, 20), fontsize=30, color="white")
        screen.draw.text("ARROWS: Move | UP/SPACE: Jump", (20, 55), fontsize=20, color=(180, 180, 180))
        screen.draw.text("REACH TOP RIGHT!", (550, 20), fontsize=25, color=(200, 200, 100))
    
    else:  # win or lose
        screen.fill((20, 20, 40))
        msg = "YOU WIN!" if state == "win" else "GAME OVER"
        color = (100, 200, 100) if state == "win" else (200, 100, 100)
        screen.draw.text(msg, center=(400, 150), fontsize=70, color=color)
        screen.draw.text(f"SCORE: {score}", center=(400, 250), fontsize=40, color="white")
        draw_button(300, 350, 200, 50, "MENU", (100, 150, 200))


def draw_button(x, y, w, h, text, color):
    """Draw a menu button"""
    screen.draw.filled_rect(Rect(x, y, w, h), color)
    screen.draw.text(text, center=(x + w//2, y + h//2), fontsize=28, color="white")


def draw_character(char):
    """Draw character using sprite images"""
    sprite_name = char.get_sprite()
    
    # Display the sprite (flips automatically based on direction)
    if char.facing_right:
        screen.blit(sprite_name, (char.x, char.y))
    else:
        screen.blit(sprite_name, (char.x, char.y))


def on_mouse_down(pos):
    """Handle button clicks"""
    global state, sound_on, music_on
    
    if state == "menu":
        if Rect(300, 220, 200, 50).collidepoint(pos):
            init_game()
        elif Rect(300, 290, 200, 50).collidepoint(pos):
            sound_on = not sound_on
        elif Rect(300, 360, 200, 50).collidepoint(pos):
            music_on = not music_on
        elif Rect(300, 430, 200, 50).collidepoint(pos):
            exit()
    elif state in ["win", "lose"]:
        if Rect(300, 350, 200, 50).collidepoint(pos):
            state = "menu"