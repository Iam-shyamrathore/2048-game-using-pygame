import pygame
import random
import math
import json
import os
from datetime import datetime

pygame.init()
pygame.mixer.init()

# Constants
FPS = 60
WIDTH, HEIGHT = 800, 900
ROWS = 4
COLS = 4
RECT_HEIGHT = 150
RECT_WIDTH = 150
PADDING = 10

# Theme System
THEMES = {
    "cozy": {
        'name': 'Cozy Cafe',
        'background': (246, 241, 235),
        'board_bg': (222, 211, 199),
        'outline': (193, 179, 165),
        'button': (180, 147, 117),
        'button_hover': (160, 127, 97),
        'text': (94, 80, 73),
        'score_bg': (180, 147, 117),
        'tile_colors': {
            2: (249, 241, 233),
            4: (245, 231, 216),
            8: (242, 213, 187),
            16: (239, 195, 158),
            32: (236, 177, 129),
            64: (233, 159, 100),
            128: (214, 184, 149),
            256: (204, 170, 129),
            512: (194, 156, 109),
            1024: (184, 142, 89),
            2048: (174, 128, 69),
        },
        'text_colors': {
            2: (119, 110, 101),
            4: (119, 110, 101),
            8: (249, 246, 242),
            16: (249, 246, 242),
            32: (249, 246, 242),
            64: (249, 246, 242),
            128: (249, 246, 242),
            256: (249, 246, 242),
            512: (249, 246, 242),
            1024: (249, 246, 242),
            2048: (249, 246, 242),
        },
        'particle_color': (180, 147, 117),
        'font': "Georgia"
    },
    "nerdy": {
        'name': 'Matrix',
        'background': (10, 15, 20),
        'board_bg': (20, 30, 40),
        'outline': (0, 255, 127),
        'button': (0, 100, 0),
        'button_hover': (0, 150, 0),
        'text': (0, 255, 127),
        'score_bg': (30, 45, 60),
        'tile_colors': {
            2: (0, 40, 0),
            4: (0, 60, 0),
            8: (0, 80, 0),
            16: (0, 100, 0),
            32: (0, 120, 0),
            64: (0, 140, 0),
            128: (0, 160, 0),
            256: (0, 180, 0),
            512: (0, 200, 0),
            1024: (0, 220, 0),
            2048: (0, 255, 0),
        },
        'text_colors': {
            2: (0, 255, 127),
            4: (0, 255, 127),
            8: (0, 255, 127),
            16: (0, 255, 127),
            32: (0, 255, 127),
            64: (0, 255, 127),
            128: (0, 255, 127),
            256: (0, 255, 127),
            512: (0, 255, 127),
            1024: (0, 255, 127),
            2048: (0, 255, 127),
        },
        'particle_color': (0, 255, 127),
        'font': "Courier New"
    },
    "dark": {
        'name': 'Midnight',
        'background': (25, 25, 35),
        'board_bg': (40, 40, 55),
        'outline': (80, 80, 100),
        'button': (70, 100, 170),
        'button_hover': (90, 120, 190),
        'text': (220, 220, 220),
        'score_bg': (50, 50, 70),
        'tile_colors': {
            2: (65, 75, 95),
            4: (75, 85, 110),
            8: (85, 100, 130),
            16: (100, 115, 150),
            32: (115, 130, 170),
            64: (130, 150, 190),
            128: (70, 130, 180),
            256: (80, 140, 200),
            512: (90, 150, 220),
            1024: (100, 160, 240),
            2048: (110, 170, 255),
        },
        'text_colors': {
            2: (220, 220, 220),
            4: (220, 220, 220),
            8: (220, 220, 220),
            16: (220, 220, 220),
            32: (220, 220, 220),
            64: (220, 220, 220),
            128: (220, 220, 220),
            256: (220, 220, 220),
            512: (220, 220, 220),
            1024: (220, 220, 220),
            2048: (220, 220, 220),
        },
        'particle_color': (100, 150, 255),
        'font': "Arial"
    }
}

CURRENT_THEME = "cozy"

# Fonts
FONT = None
SCORE_FONT = None
TITLE_FONT = None
MENU_FONT = None
SMALL_FONT = None

# Font function
def get_font(size, bold=False):
    theme_font = THEMES[CURRENT_THEME]['font']
    return pygame.font.SysFont(theme_font, size, bold=bold)

# Function to initialize fonts
def initialize_fonts():
    global FONT, SCORE_FONT, TITLE_FONT, MENU_FONT, SMALL_FONT
    FONT = get_font(50, True)
    SCORE_FONT = get_font(24, True)
    TITLE_FONT = get_font(60, True)
    MENU_FONT = get_font(35, True)
    SMALL_FONT = get_font(20)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Ultimate")

# Save file
SAVE_FILE = "game_data.json"

# Sound effects
def create_beep_sound(frequency=440, duration=100):
    sample_rate = 44100
    n_samples = int(round(duration * 0.001 * sample_rate))
    buf = numpy.zeros((n_samples, 2), dtype=numpy.int16)
    max_sample = 2**(16 - 1) - 1
    for s in range(n_samples):
        t = float(s) / sample_rate
        buf[s][0] = int(round(max_sample * math.sin(2 * math.pi * frequency * t)))
        buf[s][1] = int(round(max_sample * math.sin(2 * math.pi * frequency * t)))
    return pygame.sndarray.make_sound(buf)

try:
    import numpy
    MOVE_SOUND = create_beep_sound(300, 50)
    MERGE_SOUND = create_beep_sound(600, 100)
    WIN_SOUND = create_beep_sound(800, 500)
    GAME_OVER_SOUND = create_beep_sound(200, 300)
except:
    MOVE_SOUND = MERGE_SOUND = WIN_SOUND = GAME_OVER_SOUND = None

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 6)
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        self.life = random.randint(20, 40)
    
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 1
        self.size = max(0, self.size - 0.1)
        return self.life > 0
    
    def draw(self, window):
        alpha = min(255, self.life * 6)
        color = (*self.color, alpha)
        surf = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        pygame.draw.circle(surf, color, (self.size, self.size), self.size)
        window.blit(surf, (self.x - self.size, self.y - self.size))

class AnimatedBackground:
    def __init__(self):
        self.particles = []
        for _ in range(50):
            self.particles.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'speed': random.uniform(0.1, 0.5),
                'size': random.randint(1, 3)
            })
    
    def update(self):
        for p in self.particles:
            p['y'] += p['speed']
            if p['y'] > HEIGHT:
                p['y'] = 0
                p['x'] = random.randint(0, WIDTH)
    
    def draw(self, window):
        theme = THEMES[CURRENT_THEME]
        for p in self.particles:
            color = theme['particle_color'] + (50,)
            pygame.draw.circle(window, color, (int(p['x']), int(p['y'])), p['size'])

class Button:
    def __init__(self, x, y, width, height, text, font, color=None, hover_color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        theme = THEMES[CURRENT_THEME]
        self.color = color or theme['button']
        self.hover_color = hover_color or theme['button_hover']
        self.hovered = False
        
    def draw(self, window):
        theme = THEMES[CURRENT_THEME]
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(window, color, self.rect, border_radius=8)
        pygame.draw.rect(window, theme['outline'], self.rect, 2, border_radius=8)
        
        text_surface = self.font.render(self.text, True, theme['text'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        window.blit(text_surface, text_rect)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def update_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)

class Tile:
    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * (RECT_WIDTH + PADDING) + PADDING + 50
        self.y = row * (RECT_HEIGHT + PADDING) + PADDING + 200
        self.target_x = self.x
        self.target_y = self.y
        self.merging = False
        self.particles = []
        self.scale = 0.1
        self.new_tile = True

    def get_color(self):
        theme = THEMES[CURRENT_THEME]
        return theme['tile_colors'].get(self.value, (60, 58, 50))

    def get_text_color(self):
        theme = THEMES[CURRENT_THEME]
        return theme['text_colors'].get(self.value, (249, 246, 242))

    def create_merge_particles(self):
        center_x = self.x + RECT_WIDTH / 2
        center_y = self.y + RECT_HEIGHT / 2
        for _ in range(15):
            self.particles.append(Particle(center_x, center_y, self.get_color()[:3]))

    def draw(self, window):
        # Update particles
        for particle in self.particles[:]:
            if not particle.update():
                self.particles.remove(particle)
            else:
                particle.draw(window)
        
        # Animation for new tiles
        if self.new_tile and self.scale < 1.0:
            self.scale = min(1.0, self.scale + 0.1)
        
        # Smooth movement
        if abs(self.x - self.target_x) > 1:
            self.x += (self.target_x - self.x) * 0.3
        else:
            self.x = self.target_x
            
        if abs(self.y - self.target_y) > 1:
            self.y += (self.target_y - self.y) * 0.3
        else:
            self.y = self.target_y
        
        color = self.get_color()
        
        # Draw with scale animation
        width = RECT_WIDTH * self.scale
        height = RECT_HEIGHT * self.scale
        center_x = self.x + RECT_WIDTH / 2
        center_y = self.y + RECT_HEIGHT / 2
        
        pygame.draw.rect(window, color, 
                        (center_x - width/2, center_y - height/2, width, height), 
                        border_radius=6)
        
        # Draw value with appropriate font size
        if self.value < 100:
            font_size = 50
        elif self.value < 1000:
            font_size = 40
        else:
            font_size = 30
            
        font = get_font(font_size, True)
        text = font.render(str(self.value), True, self.get_text_color())
        window.blit(text, (
            center_x - text.get_width() / 2,
            center_y - text.get_height() / 2,
        ))

    def move_to(self, row, col):
        self.target_x = col * (RECT_WIDTH + PADDING) + PADDING + 50
        self.target_y = row * (RECT_HEIGHT + PADDING) + PADDING + 200
        self.new_tile = False

class GameData:
    def __init__(self):
        self.high_scores = []
        self.settings = {'sound': True, 'animations': True, 'theme': 'cozy'}
        self.load_data()
    
    def load_data(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, 'r') as f:
                    data = json.load(f)
                    self.high_scores = data.get('high_scores', [])
                    self.settings = data.get('settings', {'sound': True, 'animations': True, 'theme': 'cozy'})
            except:
                self.high_scores = []
                self.settings = {'sound': True, 'animations': True, 'theme': 'cozy'}
    
    def save_data(self):
        try:
            with open(SAVE_FILE, 'w') as f:
                json.dump({
                    'high_scores': self.high_scores,
                    'settings': self.settings
                }, f)
        except:
            pass
    
    def add_score(self, score, player_name="Player", mode="Single Player"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.high_scores.append({
            'score': score,
            'player': player_name,
            'date': timestamp,
            'mode': mode,
            'theme': CURRENT_THEME
        })
        self.high_scores.sort(key=lambda x: x['score'], reverse=True)
        self.high_scores = self.high_scores[:10]
        self.save_data()
    
    def get_top_scores(self, n=10):
        return self.high_scores[:n]

class Game:
    def __init__(self, game_data):
        self.tiles = {}
        self.score = 0
        self.best_score = max([score['score'] for score in game_data.get_top_scores()]) if game_data.get_top_scores() else 0
        self.game_over = False
        self.won = False
        self.player_name = "Player"
        self.game_data = game_data
        self.continue_after_win = False
        self.paused = False
        
    def generate_tiles(self):
        self.tiles = {}
        for _ in range(2):
            self.add_random_tile()
    
    def add_random_tile(self):
        row, col = self.get_random_pos()
        value = 2 if random.random() < 0.9 else 4
        tile = Tile(value, row, col)
        self.tiles[f"{row}{col}"] = tile
    
    def get_random_pos(self):
        while True:
            row = random.randrange(0, ROWS)
            col = random.randrange(0, COLS)
            if f"{row}{col}" not in self.tiles:
                return row, col
    
    def check_game_over(self):
        if len(self.tiles) < ROWS * COLS:
            return False
        
        for tile in self.tiles.values():
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                adj_row, adj_col = tile.row + dr, tile.col + dc
                if 0 <= adj_row < ROWS and 0 <= adj_col < COLS:
                    adj_tile = self.tiles.get(f"{adj_row}{adj_col}")
                    if adj_tile and tile.value == adj_tile.value:
                        return False
        return True
    
    def check_win(self):
        for tile in self.tiles.values():
            if tile.value == 2048:
                return True
        return False
    
    def move(self, direction):
        if self.game_over or self.paused:
            return False
        
        moved = False
        vectors = {
            "left": (0, -1),
            "right": (0, 1),
            "up": (-1, 0),
            "down": (1, 0)
        }
        
        dx, dy = vectors[direction]
        
        # Sort tiles based on direction
        if direction in ["left", "up"]:
            sorted_tiles = sorted(self.tiles.values(), key=lambda t: t.row * ROWS + t.col)
        else:
            sorted_tiles = sorted(self.tiles.values(), key=lambda t: t.row * ROWS + t.col, reverse=True)
        
        merged_tiles = set()
        new_tiles = {}
        
        for tile in sorted_tiles:
            if tile.merging:
                continue
                
            current_row, current_col = tile.row, tile.col
            
            while True:
                next_row, next_col = current_row + dx, current_col + dy
                
                # Check if next position is valid
                if not (0 <= next_row < ROWS and 0 <= next_col < COLS):
                    break
                
                next_tile_key = f"{next_row}{next_col}"
                
                if next_tile_key in new_tiles:
                    next_tile = new_tiles[next_tile_key]
                    
                    # If tiles can merge
                    if (not next_tile.merging and tile.value == next_tile.value and 
                        next_tile not in merged_tiles and tile not in merged_tiles):
                        # Merge tiles
                        next_tile.value *= 2
                        self.score += next_tile.value
                        merged_tiles.add(next_tile)
                        tile.merging = True
                        
                        # Create merge particles
                        if self.game_data.settings.get('animations', True):
                            next_tile.create_merge_particles()
                        
                        # Play merge sound
                        if self.game_data.settings.get('sound', True) and MERGE_SOUND:
                            MERGE_SOUND.play()
                        
                        moved = True
                        break
                    else:
                        break
                else:
                    # Move tile to empty space
                    current_row, current_col = next_row, next_col
                    moved = True
            
            # Update tile position
            if not tile.merging:
                tile.row, tile.col = current_row, current_col
                tile.move_to(current_row, current_col)
                new_tiles[f"{current_row}{current_col}"] = tile
        
        # Update tiles dictionary
        self.tiles = new_tiles
        
        # Add new tile if moved
        if moved:
            if self.game_data.settings.get('sound', True) and MOVE_SOUND:
                MOVE_SOUND.play()
                
            self.add_random_tile()
            
            # Update best score
            if self.score > self.best_score:
                self.best_score = self.score
            
            # Check win condition
            if not self.won and self.check_win():
                self.won = True
                if self.game_data.settings.get('sound', True) and WIN_SOUND:
                    WIN_SOUND.play()
                if not self.continue_after_win:
                    self.game_data.add_score(self.score, self.player_name)
            
            # Check game over
            if self.check_game_over():
                self.game_over = True
                if self.game_data.settings.get('sound', True) and GAME_OVER_SOUND:
                    GAME_OVER_SOUND.play()
                if not self.won:
                    self.game_data.add_score(self.score, self.player_name)
        
        return moved
    
    def toggle_pause(self):
        self.paused = not self.paused
    
    def draw_grid(self, window):
        theme = THEMES[CURRENT_THEME]
        # Draw empty cells
        for row in range(ROWS):
            for col in range(COLS):
                x = col * (RECT_WIDTH + PADDING) + PADDING + 50
                y = row * (RECT_HEIGHT + PADDING) + PADDING + 200
                pygame.draw.rect(window, theme['board_bg'], (x, y, RECT_WIDTH, RECT_HEIGHT), border_radius=6)
    
    def draw(self, window):
        theme = THEMES[CURRENT_THEME]
        # Draw background
        window.fill(theme['background'])
        
        # Draw title
        title = TITLE_FONT.render("2048", True, theme['text'])
        window.blit(title, (50, 30))
        
        # Draw score area
        score_bg = pygame.Rect(WIDTH - 200, 30, 150, 60)
        pygame.draw.rect(window, theme['score_bg'], score_bg, border_radius=8)
        
        score_text = SCORE_FONT.render(f"Score: {self.score}", True, theme['text'])
        best_text = SCORE_FONT.render(f"Best: {self.best_score}", True, theme['text'])
        
        window.blit(score_text, (WIDTH - 180, 40))
        window.blit(best_text, (WIDTH - 180, 65))
        
        # Draw game board background
        board_bg = pygame.Rect(40, 180, 720, 720)
        pygame.draw.rect(window, theme['outline'], board_bg, border_radius=10)
        
        # Draw grid
        self.draw_grid(window)
        
        # Draw tiles
        for tile in self.tiles.values():
            tile.draw(window)
        
        # Draw pause overlay if game is paused
        if self.paused:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            window.blit(overlay, (0, 0))
            
            pause_text = TITLE_FONT.render("PAUSED", True, (255, 255, 255))
            window.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2 - 50))
            
            continue_text = MENU_FONT.render("Press P to continue", True, (255, 255, 255))
            window.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 + 20))
        
        # Draw game status
        elif self.won and not self.continue_after_win:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 180))
            window.blit(overlay, (0, 0))
            
            win_text = TITLE_FONT.render("You Win!", True, theme['text'])
            window.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - 50))
            
            continue_text = MENU_FONT.render("Press any key to continue", True, theme['text'])
            window.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 + 20))
        
        elif self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            window.blit(overlay, (0, 0))
            
            game_over_text = TITLE_FONT.render("Game Over!", True, (255, 255, 255))
            window.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
            
            score_text = MENU_FONT.render(f"Final Score: {self.score}", True, (255, 255, 255))
            window.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 + 20))

class MultiplayerGame:
    def __init__(self, game_data):
        self.player1 = Game(game_data)
        self.player2 = Game(game_data)
        self.player1.player_name = "Player 1"
        self.player2.player_name = "Player 2"
        self.current_player = 1
        self.turn_count = 0
        self.game_data = game_data
        self.paused = False
        
    def generate_tiles(self):
        self.player1.generate_tiles()
        self.player2.generate_tiles()
    
    def switch_player(self):
        self.current_player = 2 if self.current_player == 1 else 1
        self.turn_count += 1
    
    def get_current_game(self):
        return self.player1 if self.current_player == 1 else self.player2
    
    def is_game_over(self):
        return self.player1.game_over and self.player2.game_over
    
    def get_winner(self):
        if self.player1.score > self.player2.score:
            return "Player 1", self.player1.score
        elif self.player2.score > self.player1.score:
            return "Player 2", self.player2.score
        else:
            return "Tie", self.player1.score
    
    def toggle_pause(self):
        self.paused = not self.paused
        self.player1.paused = self.paused
        self.player2.paused = self.paused
    
    def draw(self, window):
        current_game = self.get_current_game()
        current_game.draw(window)
        
        # Draw player info
        theme = THEMES[CURRENT_THEME]
        player_bg = pygame.Rect(WIDTH // 2 - 150, 100, 300, 50)
        pygame.draw.rect(window, theme['score_bg'], player_bg, border_radius=8)
        
        player_text = MENU_FONT.render(f"{current_game.player_name}'s Turn", True, theme['text'])
        window.blit(player_text, (WIDTH // 2 - player_text.get_width() // 2, 110))
        
        # Draw pause overlay for multiplayer
        if self.paused:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            window.blit(overlay, (0, 0))
            
            pause_text = TITLE_FONT.render("PAUSED", True, (255, 255, 255))
            window.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2 - 50))
            
            continue_text = MENU_FONT.render("Press P to continue", True, (255, 255, 255))
            window.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 + 20))

def draw_menu(window, background):
    theme = THEMES[CURRENT_THEME]
    window.fill(theme['background'])
    
    # Draw animated background
    background.draw(window)
    
    title = TITLE_FONT.render("2048 ULTIMATE", True, theme['text'])
    window.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    
    subtitle = SMALL_FONT.render(f"Theme: {theme['name']}", True, theme['text'])
    window.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 170))
    
    buttons = [
        Button(WIDTH//2 - 150, 250, 300, 60, "Single Player", MENU_FONT),
        Button(WIDTH//2 - 150, 330, 300, 60, "Multiplayer", MENU_FONT),
        Button(WIDTH//2 - 150, 410, 300, 60, "Scoreboard", MENU_FONT),
        Button(WIDTH//2 - 150, 490, 300, 60, "Settings", MENU_FONT),
        Button(WIDTH//2 - 150, 570, 300, 60, "How to Play", MENU_FONT),
        Button(WIDTH//2 - 150, 650, 300, 60, "Quit", MENU_FONT),
    ]
    
    return buttons

def draw_scoreboard(window, game_data):
    theme = THEMES[CURRENT_THEME]
    window.fill(theme['background'])
    
    title = TITLE_FONT.render("TOP SCORES", True, theme['text'])
    window.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
    
    scores = game_data.get_top_scores()
    y_pos = 150
    
    # Headers
    headers = ["Rank", "Player", "Score", "Theme"]
    for i, header in enumerate(headers):
        header_text = SMALL_FONT.render(header, True, theme['text'])
        x_pos = 50 + i * 180
        window.blit(header_text, (x_pos, y_pos - 30))
    
    for i, entry in enumerate(scores):
        rank_color = (255, 215, 0) if i == 0 else (192, 192, 192) if i == 1 else (205, 127, 50) if i == 2 else theme['text']
        
        rank_text = SMALL_FONT.render(f"#{i+1}", True, rank_color)
        player_text = SMALL_FONT.render(entry['player'], True, theme['text'])
        score_text = SMALL_FONT.render(str(entry['score']), True, theme['text'])
        theme_text = SMALL_FONT.render(entry.get('theme', 'default').title(), True, theme['text'])
        
        window.blit(rank_text, (70, y_pos))
        window.blit(player_text, (150, y_pos))
        window.blit(score_text, (330, y_pos))
        window.blit(theme_text, (510, y_pos))
        
        y_pos += 40
    
    if not scores:
        no_scores = MENU_FONT.render("No scores yet!", True, theme['text'])
        window.blit(no_scores, (WIDTH//2 - no_scores.get_width()//2, HEIGHT//2))
    
    back_button = Button(WIDTH//2 - 150, 750, 300, 60, "Back", MENU_FONT)
    return [back_button]

def draw_settings(window, game_data):
    theme = THEMES[CURRENT_THEME]
    window.fill(theme['background'])
    
    title = TITLE_FONT.render("SETTINGS", True, theme['text'])
    window.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
    
    # Sound toggle
    sound_text = MENU_FONT.render("Sound:", True, theme['text'])
    window.blit(sound_text, (WIDTH//2 - 200, 150))
    
    sound_button = Button(WIDTH//2 + 50, 150, 150, 50, 
                         "ON" if game_data.settings.get('sound', True) else "OFF", 
                         MENU_FONT,
                         color=(100, 200, 100) if game_data.settings.get('sound', True) else (200, 100, 100))
    
    # Animations toggle
    anim_text = MENU_FONT.render("Animations:", True, theme['text'])
    window.blit(anim_text, (WIDTH//2 - 200, 230))
    
    anim_button = Button(WIDTH//2 + 50, 230, 150, 50, 
                        "ON" if game_data.settings.get('animations', True) else "OFF", 
                        MENU_FONT,
                        color=(100, 200, 100) if game_data.settings.get('animations', True) else (200, 100, 100))
    
    # Theme selector
    theme_text = MENU_FONT.render("Theme:", True, theme['text'])
    window.blit(theme_text, (WIDTH//2 - 200, 310))
    
    theme_names = list(THEMES.keys())
    current_index = theme_names.index(CURRENT_THEME)
    theme_button = Button(WIDTH//2 + 50, 310, 150, 50, 
                         THEMES[CURRENT_THEME]['name'], 
                         SMALL_FONT)
    
    back_button = Button(WIDTH//2 - 150, 500, 300, 60, "Back", MENU_FONT)
    
    return [sound_button, anim_button, theme_button, back_button]

def draw_how_to_play(window):
    theme = THEMES[CURRENT_THEME]
    window.fill(theme['background'])
    
    title = TITLE_FONT.render("HOW TO PLAY", True, theme['text'])
    window.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
    
    instructions = [
        "Use ARROW KEYS to move tiles",
        "Tiles with same numbers merge into one",
        "Try to reach the 2048 tile!",
        "",
        "SINGLE PLAYER: Beat your high score",
        "MULTIPLAYER: Take turns, highest score wins",
        "",
        "CONTROLS:",
        "P - Pause/Resume game",
        "ESC - Back to menu",
        "Arrow Keys - Move tiles",
        "",
        "Enjoy the game! 🎮"
    ]
    
    y_pos = 150
    for line in instructions:
        text = SMALL_FONT.render(line, True, theme['text'])
        window.blit(text, (WIDTH // 2 - text.get_width() // 2, y_pos))
        y_pos += 35
    
    back_button = Button(WIDTH//2 - 150, 750, 300, 60, "Back", MENU_FONT)
    return [back_button]

def draw_game_over(window, is_multiplayer=False, winner_info=None):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(220)
    overlay.fill((0, 0, 0))
    window.blit(overlay, (0, 0))
    
    if is_multiplayer and winner_info:
        winner, score = winner_info
        if winner == "Tie":
            title_text = TITLE_FONT.render("It's a Tie!", True, (255, 215, 0))
        else:
            title_text = TITLE_FONT.render(f"{winner} Wins!", True, (255, 215, 0))
        score_text = SCORE_FONT.render(f"Winning Score: {score}", True, (255, 255, 255))
    else:
        title_text = TITLE_FONT.render("Game Over!", True, (255, 255, 255))
        score_text = SCORE_FONT.render("Good job! Try again!", True, (255, 255, 255))
    
    window.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 300))
    window.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 380))
    
    buttons = [
        Button(150, 500, 200, 60, "Play Again", MENU_FONT),
        Button(450, 500, 200, 60, "Main Menu", MENU_FONT),
    ]
    
    return buttons

def main():
    clock = pygame.time.Clock()
    game_data = GameData()
    background = AnimatedBackground()
    
    # Set initial theme
    global CURRENT_THEME
    CURRENT_THEME = game_data.settings.get('theme', 'cozy')
    initialize_fonts()
    
    state = "menu"
    game = None
    multiplayer = None
    buttons = []
    
    # Create back and pause buttons
    back_button = Button(20, 100, 80, 40, "Back", SMALL_FONT)
    pause_button = Button(WIDTH - 100, 100, 80, 40, "Pause", SMALL_FONT)
    
    run = True
    while run:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        
        # Update animated background
        if state == "menu":
            background.update()
        
        # Update button hover states
        for button in buttons:
            button.update_hover(mouse_pos)
        back_button.update_hover(mouse_pos)
        pause_button.update_hover(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if state in ["game", "multiplayer"]:
                        state = "menu"
                    elif state in ["scoreboard", "how_to_play", "settings"]:
                        state = "menu"
                    elif state == "game_over":
                        state = "menu"
                
                elif event.key == pygame.K_p:  # Pause key
                    if state == "game" and game:
                        game.toggle_pause()
                    elif state == "multiplayer" and multiplayer:
                        multiplayer.toggle_pause()
                
                elif state == "game" and game:
                    if not game.paused and not game.game_over:
                        moved = False
                        if event.key == pygame.K_LEFT:
                            moved = game.move("left")
                        elif event.key == pygame.K_RIGHT:
                            moved = game.move("right")
                        elif event.key == pygame.K_UP:
                            moved = game.move("up")
                        elif event.key == pygame.K_DOWN:
                            moved = game.move("down")
                        
                        # Continue after win
                        if game.won and not game.continue_after_win:
                            game.continue_after_win = True
                
                elif state == "multiplayer" and multiplayer:
                    current_game = multiplayer.get_current_game()
                    if not multiplayer.paused and not current_game.game_over:
                        moved = False
                        if event.key == pygame.K_LEFT:
                            moved = current_game.move("left")
                        elif event.key == pygame.K_RIGHT:
                            moved = current_game.move("right")
                        elif event.key == pygame.K_UP:
                            moved = current_game.move("up")
                        elif event.key == pygame.K_DOWN:
                            moved = current_game.move("down")
                        
                        if moved and not current_game.game_over:
                            multiplayer.switch_player()
                        
                        if multiplayer.is_game_over():
                            state = "game_over"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Handle back and pause buttons
                if state in ["game", "multiplayer"]:
                    if back_button.is_clicked(mouse_pos):
                        state = "menu"
                    elif pause_button.is_clicked(mouse_pos):
                        if state == "game" and game:
                            game.toggle_pause()
                        elif state == "multiplayer" and multiplayer:
                            multiplayer.toggle_pause()
                
                # Handle other buttons
                for i, button in enumerate(buttons):
                    if button.is_clicked(mouse_pos):
                        if state == "menu":
                            if i == 0:  # Single Player
                                game = Game(game_data)
                                game.generate_tiles()
                                state = "game"
                            elif i == 1:  # Multiplayer
                                multiplayer = MultiplayerGame(game_data)
                                multiplayer.generate_tiles()
                                state = "multiplayer"
                            elif i == 2:  # Scoreboard
                                state = "scoreboard"
                            elif i == 3:  # Settings
                                state = "settings"
                            elif i == 4:  # How to Play
                                state = "how_to_play"
                            elif i == 5:  # Quit
                                run = False
                        
                        elif state == "scoreboard":
                            state = "menu"
                        
                        elif state == "settings":
                            if i == 0:  # Sound toggle
                                game_data.settings['sound'] = not game_data.settings.get('sound', True)
                                game_data.save_data()
                            elif i == 1:  # Animations toggle
                                game_data.settings['animations'] = not game_data.settings.get('animations', True)
                                game_data.save_data()
                            elif i == 2:  # Theme cycle
                                theme_names = list(THEMES.keys())
                                current_index = theme_names.index(CURRENT_THEME)
                                CURRENT_THEME = theme_names[(current_index + 1) % len(theme_names)]
                                game_data.settings['theme'] = CURRENT_THEME
                                game_data.save_data()
                                # Update fonts for new theme
                                initialize_fonts()
                            elif i == 3:  # Back
                                state = "menu"
                        
                        elif state == "how_to_play":
                            state = "menu"
                        
                        elif state == "game_over":
                            if i == 0:  # Play Again
                                if multiplayer:
                                    multiplayer = MultiplayerGame(game_data)
                                    multiplayer.generate_tiles()
                                    state = "multiplayer"
                                else:
                                    game = Game(game_data)
                                    game.generate_tiles()
                                    state = "game"
                            elif i == 1:  # Main Menu
                                state = "menu"
                                game = None
                                multiplayer = None
        
        # Drawing
        if state == "menu":
            buttons = draw_menu(WINDOW, background)
            for button in buttons:
                button.draw(WINDOW)
        
        elif state == "game":
            if game:
                game.draw(WINDOW)
                # Draw back and pause buttons
                back_button.draw(WINDOW)
                pause_button.draw(WINDOW)
        
        elif state == "multiplayer":
            if multiplayer:
                multiplayer.draw(WINDOW)
                # Draw back and pause buttons
                back_button.draw(WINDOW)
                pause_button.draw(WINDOW)
        
        elif state == "scoreboard":
            buttons = draw_scoreboard(WINDOW, game_data)
            for button in buttons:
                button.draw(WINDOW)
        
        elif state == "settings":
            buttons = draw_settings(WINDOW, game_data)
            for button in buttons:
                button.draw(WINDOW)
        
        elif state == "how_to_play":
            buttons = draw_how_to_play(WINDOW)
            for button in buttons:
                button.draw(WINDOW)
        
        elif state == "game_over":
            if multiplayer:
                winner_info = multiplayer.get_winner()
                buttons = draw_game_over(WINDOW, True, winner_info)
            else:
                buttons = draw_game_over(WINDOW)
            for button in buttons:
                button.draw(WINDOW)
        
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()