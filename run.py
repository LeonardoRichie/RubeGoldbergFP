import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Parkour')

tile_size = 50


bg_img = pygame.image.load('Background.png')

#def draw_grid():
    #for line in range(0, 20):
        #pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        #pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

run = True
while run:

    clock.tick(fps)
    screen.blit(bg_img,(0,0))

    world.draw()

    display_surface.blit(text,textRect)

    water_group.draw(screen)

    game_over = player.update(game_over)

    slug_group.update()
    slug_group.draw(screen)

    

    if game_over == -1: #when player died
        if restart_button.draw():
            player.reset(100, screen_height - 110)
            game_over = 0

    #draw_grid()

    print(world.tile_list)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()