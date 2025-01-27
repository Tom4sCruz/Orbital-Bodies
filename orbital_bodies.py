import pygame
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, LENGTH = 1600, 700
G = 1
FPS = 60

PLANET_POS = (WIDTH // 2, LENGTH // 2)
PLANET_RADIUS = 50
PLANET_MASS = 5000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 65)
RED = (255, 0, 0)
ORANGE = (255, 153, 51)

COLORS = [(200,0,0), (0,183,235), (0,200,0), (255,105,180), (255,215,0)]

screen = pygame.display.set_mode((WIDTH, LENGTH))
pygame.display.set_caption("Orbital bodies")

class Body:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.mass = 1
        self.color = color
        
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

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 5)
    
bodies = []

running = True
clock = pygame.time.Clock()
body = None
hasLooped = False
i = 0

while running:
    screen.fill(DARK_BLUE)
    pygame.draw.circle(screen, ORANGE, PLANET_POS, PLANET_RADIUS)
    
    for b in bodies:
        b.update_pos()
        b.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if len(bodies) == 5:
                aux_color = bodies.pop(0).color
            else:
                aux_color = COLORS[i]
                i += 1
            start_pos = pygame.mouse.get_pos()
            body = Body(start_pos[0], start_pos[1], aux_color)
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

    
    pygame.display.flip() # Redraws everything on screen
    clock.tick(FPS)

pygame.quit()
