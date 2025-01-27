import pygame
import math
from pygame.locals import * 

# Initialize pygame
pygame.init()

# Constants
WIDTH, LENGTH = 1600, 700
G = 1
FPS = 60

PLANET_POS = (WIDTH // 2, LENGTH // 2)
PLANET_RADIUS = 50
PLANET_MASS = 5000

PARTICLE_RADIUS = 5

BACKGROUND = (0, 0, 65)
PLANET_COLOR = (255, 153, 51) # Orange

# REDS

ON_RED = (237,29,36)
OFF_RED = (150, 0, 0)
RED_GLOW = (60,2,2)

REDS = [ON_RED, OFF_RED, RED_GLOW]

# BLUES

ON_BLUE = (0,174,239)
OFF_BLUE = (0,100,150) #(0,138,216)
BLUE_GLOW = (0,30,60)

BLUES = [ON_BLUE, OFF_BLUE, BLUE_GLOW]

# GREENS

ON_GREEN = (8,255,8)
OFF_GREEN = (0,100,0)
GREEN_GLOW = (2,60,2)

GREENS = [ON_GREEN, OFF_GREEN, GREEN_GLOW]

# PINKS

ON_PINK = (255,105,180)#(255,0,127)
OFF_PINK = (207,87,138)
PINK_GLOW = (60,0,20)

PINKS = [ON_PINK, OFF_PINK, PINK_GLOW]

# YELLOWS

ON_YELLOW = (255,222,0)
OFF_YELLOW = (205,150,0)
YELLOW_GLOW = (60,50,0)

YELLOWS = [ON_YELLOW, OFF_YELLOW, YELLOW_GLOW]


COLORS = [REDS, BLUES, GREENS, PINKS, YELLOWS]

#COLORS = [(200,0,0), (0,183,235), (0,200,0), (255,105,180), (255,215,0)]

screen = pygame.display.set_mode((WIDTH, LENGTH))
pygame.display.set_caption("Orbital bodies")


class Body:
    def __init__(self, x, y, colors):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.mass = 1
        self.colors = colors
        self.glow = False
        
    def update_pos(self):
        if not self.dragging:
            self.apply_gravity()
            self.x += self.vx
            self.y += self.vy

    def apply_gravity(self):
        dx = PLANET_POS[0] - self.x
        dy = PLANET_POS[1] - self.y
        dist = math.sqrt(dx**2 + dy**2)
        Fg = G * PLANET_MASS * self.mass / dist**2
        ax = Fg * dx / dist
        ay = Fg * dy / dist
        self.vx += ax
        self.vy += ay

    def circle_surf(self, r, color):
        surf = pygame.Surface((r*2, r*2))
        pygame.draw.circle(surf, color, (r, r), r)
        surf.set_colorkey((0,0,0))
        return surf
    
    def blink(self):
        self.glow = False if self.glow else True

    def glowing(self):
        if self.glow:
            self.draw(self.colors[0])
            screen.blit(self.circle_surf(PARTICLE_RADIUS*2, self.colors[2]), (self.x - PARTICLE_RADIUS*2, self.y - PARTICLE_RADIUS*2), special_flags=BLEND_RGB_ADD)
        else:
            self.draw(self.colors[1])

    def draw(self, color):
        pygame.draw.circle(screen, color, (self.x, self.y), PARTICLE_RADIUS)
    

bodies = []

running = True
clock = pygame.time.Clock()
body = None
hasLooped = False
i = 0

while running:
    screen.fill(BACKGROUND)
    pygame.draw.circle(screen, PLANET_COLOR, PLANET_POS, PLANET_RADIUS)
    
    for b in bodies:
        b.update_pos()
        b.glowing()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if len(bodies) == 5:
                aux_colors = bodies.pop(0).colors
            else:
                aux_colors = COLORS[i]
                i += 1
            start_pos = pygame.mouse.get_pos()
            body = Body(start_pos[0], start_pos[1], aux_colors)
            bodies.append(body)
            body.dragging = True

        if event.type == pygame.MOUSEBUTTONUP and body:
            end_pos = pygame.mouse.get_pos()
            body.vx = (body.x - end_pos[0])//25
            body.vy = (body.y - end_pos[1])//25
            body.dragging = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                i = 0
                bodies.clear()
            elif event.key == pygame.K_g:
                for b in bodies:
                    b.blink()

    
    pygame.display.flip() # Redraws everything on screen
    clock.tick(FPS)

pygame.quit()
