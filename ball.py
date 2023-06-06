import pygame
from pygame.locals import *
import sys

# Initialize Pygame
pygame.init()

# Set up the window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rube Goldberg Simulator")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Constants for physics simulation
GRAVITY = 9.8  # Gravitational acceleration
TIME_STEP = 0.01  # Simulation time step
BOUNCE_FACTOR = 0.8  # Bounce factor (coefficient of restitution)

# Create an empty list to hold objects
objects = []

# Ball class
class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = RED
        self.velocity_x = 0  # Initial velocity in the x-direction
        self.velocity_y = 0  # Initial velocity in the y-direction

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def update(self):
        # Apply gravitational force
        self.velocity_y += GRAVITY * TIME_STEP

        # Update position based on velocity
        self.x += self.velocity_x * TIME_STEP
        self.y += self.velocity_y * TIME_STEP

        # Check for collision with block
        if self.y + self.radius >= block.rect.top:
            if block.rect.left <= self.x <= block.rect.right:
                # Reverse the vertical velocity with a bounce factor
                self.velocity_y = -self.velocity_y * BOUNCE_FACTOR

# Block class
class Block:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BLUE

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

# Create a ball object
ball = Ball(100, 100, 20)
objects.append(ball)

# Create a block object exactly below the ball
block = Block(ball.x - 50, ball.y + ball.radius, 100, 20)
objects.append(block)

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Update the ball
    ball.update()

    # Draw objects
    for obj in objects:
        obj.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit the program
pygame.quit()
sys.exit()
