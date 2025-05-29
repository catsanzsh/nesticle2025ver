import pygame
import os
import sys
import random
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
FPS = 60
PIXEL_FONT = "assets/fonts/pixel_font.ttf"  # Placeholder for pixel font

# Colors - 90s aesthetic
BACKGROUND = (100, 100, 120)  # Dark gray-blue
PANEL_BG = (80, 80, 100)      # Darker panel background
ACCENT = (180, 0, 0)          # Blood red for highlights
TEXT_COLOR = (220, 220, 220)  # Light gray text
HIGHLIGHT = (255, 255, 200)   # Cream for highlights
BUTTON_NORMAL = (60, 60, 80)  # Button normal state
BUTTON_HOVER = (90, 90, 110)  # Button hover state
BUTTON_ACTIVE = (120, 0, 0)   # Button active state
SCREEN_BG = (20, 20, 40)      # Dark blue for screen background
SCREEN_GRID = (40, 40, 70)    # Screen grid lines

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nesticle v1.40 - Bloodlust Software")
clock = pygame.time.Clock()

# Create a simple pixel font if not available
def create_pixel_font():
    font = pygame.font.SysFont("courier", 16, bold=True)
    return font

# Create a retro-style button
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.state = "normal"  # normal, hover, active
        self.font = create_pixel_font()
        
    def draw(self, surface):
        # Draw button based on state
        if self.state == "normal":
            pygame.draw.rect(surface, BUTTON_NORMAL, self.rect)
            pygame.draw.rect(surface, (40, 40, 60), self.rect, 2)
        elif self.state == "hover":
            pygame.draw.rect(surface, BUTTON_HOVER, self.rect)
            pygame.draw.rect(surface, HIGHLIGHT, self.rect, 2)
        elif self.state == "active":
            pygame.draw.rect(surface, BUTTON_ACTIVE, self.rect)
            pygame.draw.rect(surface, HIGHLIGHT, self.rect, 2)
        
        # Draw button text
        text_surf = self.font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def update(self, mouse_pos, mouse_click):
        if self.rect.collidepoint(mouse_pos):
            if mouse_click:
                self.state = "active"
                return True
            else:
                self.state = "hover"
        else:
            self.state = "normal"
        return False

# Create the emulator screen display
class EmulatorScreen:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.grid_size = 8
        self.pixels = []
        self.generate_demo_pixels()
        
    def generate_demo_pixels(self):
        # Create a grid of "pixels" for demo effect
        for y in range(0, self.rect.height, self.grid_size):
            for x in range(0, self.rect.width, self.grid_size):
                # Randomly decide if this should be a "pixel"
                if random.random() > 0.7:
                    color = random.choice([
                        (200, 30, 30),   # Red
                        (30, 200, 30),   # Green
                        (30, 30, 200),   # Blue
                        (200, 200, 30),  # Yellow
                        (200, 30, 200),  # Purple
                    ])
                    self.pixels.append((x, y, color))
    
    def draw(self, surface):
        # Draw screen background
        pygame.draw.rect(surface, SCREEN_BG, self.rect)
        
        # Draw grid lines
        for x in range(self.rect.left, self.rect.right, self.grid_size):
            pygame.draw.line(surface, SCREEN_GRID, (x, self.rect.top), (x, self.rect.bottom), 1)
        for y in range(self.rect.top, self.rect.bottom, self.grid_size):
            pygame.draw.line(surface, SCREEN_GRID, (self.rect.left, y), (self.rect.right, y), 1)
        
        # Draw border
        pygame.draw.rect(surface, ACCENT, self.rect, 3)
        
        # Draw demo pixels
        for x, y, color in self.pixels:
            pygame.draw.rect(surface, color, 
                            (self.rect.left + x, self.rect.top + y, 
                             self.grid_size-1, self.grid_size-1))
        
        # Draw title
        font = create_pixel_font()
        title = font.render("NESTICLE v1.40", True, HIGHLIGHT)
        surface.blit(title, (self.rect.centerx - title.get_width()//2, self.rect.top + 10))
        
        # Draw demo text
        demo_text = [
            "BLOODLUST SOFTWARE",
            "PRESENTS",
            "NES EMULATOR",
            "PRESS F1 FOR HELP"
        ]
        
        for i, text in enumerate(demo_text):
            text_surf = font.render(text, True, TEXT_COLOR)
            text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.centery - 30 + i*20))
            surface.blit(text_surf, text_rect)

# Create file browser panel
class FileBrowser:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = create_pixel_font()
        self.files = ["super_mario.nes", "zelda.nes", "metroid.nes", 
                      "contra.nes", "castlevania.nes", "mega_man.nes",
                      "ninja_gaiden.nes", "tetris.nes", "double_dragon.nes"]
        self.selected = 0
        
    def draw(self, surface):
        # Draw panel background
        pygame.draw.rect(surface, PANEL_BG, self.rect)
        pygame.draw.rect(surface, (60, 60, 80), self.rect, 2)
        
        # Draw title
        title = self.font.render("ROM Browser", True, ACCENT)
        surface.blit(title, (self.rect.x + 10, self.rect.y + 10))
        
        # Draw files
        for i, file in enumerate(self.files):
            color = HIGHLIGHT if i == self.selected else TEXT_COLOR
            file_surf = self.font.render(file, True, color)
            surface.blit(file_surf, (self.rect.x + 20, self.rect.y + 40 + i*25))
        
        # Draw scroll indicators
        pygame.draw.polygon(surface, TEXT_COLOR, [
            (self.rect.right - 20, self.rect.y + 50),
            (self.rect.right - 10, self.rect.y + 50),
            (self.rect.right - 15, self.rect.y + 40)
        ])
        
        pygame.draw.polygon(surface, TEXT_COLOR, [
            (self.rect.right - 20, self.rect.bottom - 50),
            (self.rect.right - 10, self.rect.bottom - 50),
            (self.rect.right - 15, self.rect.bottom - 40)
        ])

# Create status panel
class StatusPanel:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = create_pixel_font()
        self.messages = [
            "CPU: 6502 @ 1.79MHz",
            "PPU: 2C02",
            "APU: Enabled",
            "Input: Keyboard",
            "State: Ready"
        ]
        
    def draw(self, surface):
        # Draw panel background
        pygame.draw.rect(surface, PANEL_BG, self.rect)
        pygame.draw.rect(surface, (60, 60, 80), self.rect, 2)
        
        # Draw title
        title = self.font.render("System Status", True, ACCENT)
        surface.blit(title, (self.rect.x + 10, self.rect.y + 10))
        
        # Draw status messages
        for i, msg in enumerate(self.messages):
            msg_surf = self.font.render(msg, True, TEXT_COLOR)
            surface.blit(msg_surf, (self.rect.x + 20, self.rect.y + 40 + i*25))

# Create the UI
emulator_screen = EmulatorScreen(20, 20, 320, 240)
file_browser = FileBrowser(360, 20, 220, 180)
status_panel = StatusPanel(360, 210, 220, 170)

# Create buttons
buttons = [
    Button(40, 270, 80, 30, "RUN"),
    Button(130, 270, 80, 30, "RESET"),
    Button(220, 270, 80, 30, "CONFIG"),
    Button(40, 310, 80, 30, "SAVE"),
    Button(130, 310, 80, 30, "LOAD"),
    Button(220, 310, 80, 30, "EXIT")
]

# Main loop
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = False
    
    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_click = True
    
    # Update buttons
    for button in buttons:
        if button.update(mouse_pos, mouse_click):
            # Button was clicked
            print(f"Button clicked: {button.text}")
    
    # Update file browser selection with mouse
    if file_browser.rect.collidepoint(mouse_pos):
        rel_y = mouse_pos[1] - file_browser.rect.y - 40
        if rel_y >= 0:
            idx = rel_y // 25
            if 0 <= idx < len(file_browser.files):
                file_browser.selected = idx
    
    # Drawing
    screen.fill(BACKGROUND)
    
    # Draw decorative scanlines
    for y in range(0, HEIGHT, 3):
        pygame.draw.line(screen, (60, 60, 80, 100), (0, y), (WIDTH, y), 1)
    
    # Draw UI elements
    emulator_screen.draw(screen)
    file_browser.draw(screen)
    status_panel.draw(screen)
    
    # Draw buttons
    for button in buttons:
        button.draw(screen)
    
    # Draw title and footer
    title_font = create_pixel_font()
    title = title_font.render("NESTICLE - NES Emulator v1.40", True, HIGHLIGHT)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 5))
    
    footer = title_font.render("Bloodlust Software © 1997", True, ACCENT)
    screen.blit(footer, (WIDTH//2 - footer.get_width()//2, HEIGHT - 25))
    
    # Draw decorative border
    pygame.draw.rect(screen, (50, 50, 70), (0, 0, WIDTH, HEIGHT), 4)
    pygame.draw.rect(screen, ACCENT, (0, 0, WIDTH, HEIGHT), 2)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
