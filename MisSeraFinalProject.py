import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60


#screen size
screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Parkour') #title of the run application

#define game variables
tile_size = 50
game_over = 0

#upload image
bg_img = pygame.image.load('starsbackground.png')
bg_img = pygame.transform.scale(bg_img,(2016,1134))
restart_img = pygame.image.load('Restart.png')
level1_img = pygame.image.load('level1.png')
level1_img = pygame.transform.scale(level1_img,(200,100))
level2_img = pygame.image.load('level2.png')
level2_img = pygame.transform.scale(level2_img,(200,100))
back_img = pygame.image.load('back.png')
back_img = pygame.transform.scale(back_img,(100,50 ))

#def draw_grid():
    #for line in range(0, 20):
        #pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        #pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        #mouseposition
        position = pygame.mouse.get_pos()
        #pressing mouse
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:#leftclickmouse:
                action = True
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False


        #add button
        screen.blit(self.image, self.rect)

        return action


class Player():
    def __init__(self, x, y):
        self.reset(x, y)
        
    
    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 10

        if game_over == 0:

        #getkeypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False:
                self.vel_y = -11
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1

            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT]== False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            #animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            #add gravity
            self.vel_y += 1
            #if self.vel_y > 6:
                #self.vel_y = 6
            speedfall = self.vel_y
            

            dy += self.vel_y
            dx +=self.vel_x
            #check for collision
            for tile in world.tile_list:
                #collision x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    if dx > 0:
                        self.rect.x = self.rect.x-5
                        self.vel_x = self.vel_x - 10
                    if dx < 0:
                        self.rect.x = self.rect.x+5
                        self.vel_x = self.vel_x + 10
                    
                #collision y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below the ground jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = -speedfall+3
                        
        
            #check collision with enemies
            if pygame.sprite.spritecollide(self, slug_group, False):
                game_over = -1

            #check collision with water
            if pygame.sprite.spritecollide(self, water_group, False):
                game_over = -1

            #check collision with spike
            if pygame.sprite.spritecollide(self, spike_group, False):
                game_over = -1

            #update player coordinates
            self.rect.x += dx
            self.rect.y += dy

            if self.rect.bottom > screen_height:
                self.rect.bottom = screen_height
                dy = 0

        elif game_over == -1:
            self.image = self.dead_image

        #draw player unto screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255,255,255), self.rect, 2)

        return game_over

    def reset(self,x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(3,6):
            img_right = pygame.image.load(f'blueball.png')
            img_right = pygame.transform.scale(img_right, (35, 35))
            img_left = pygame.transform.flip(img_right, True, False )#flipimage
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        grave_image = pygame.image.load('blueball.png') #dead image
        self.dead_image = pygame.transform.scale(grave_image, (35, 35))# resizing to the game size
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.vel_x = 5
        self.jumped = False #jump by pressing the space 1 time (no holding spaces)
        self.direction = 0

class World():
    def __init__(self, data):
        self.tile_list = []

        #load image
        dirt_img = pygame.image.load('wood.jpg')
        dirtgrass_img = pygame.image.load('mushroom.png')
        water_img = pygame.image.load('starblock.png') 

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img,(tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile  = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(dirtgrass_img,(tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile  = (img, img_rect)
                    self.tile_list.append(tile)

                if tile == 3:
                    water = Water(col_count * tile_size, row_count * tile_size)
                    water_group.add(water)


                if tile == 4:
                    slug = Enemy(col_count * tile_size, row_count * tile_size + 15)
                    slug_group.add(slug)

                if tile == 5:
                    spike = Spike(col_count * tile_size, row_count * tile_size)
                    spike_group.add(spike)

                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1],2)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Centipede.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        

    def update(self):
        self.image = pygame.image.load('Centipede.png')
        self.rect.x += self.move_direction
        self.move_counter += 1
        if self.move_counter > 50:
            self.move_direction *= -1
            self.move_counter *= -1
        if self.move_direction < 0:
            self.image = pygame.image.load('Centipede.png')
        if self.move_direction > 0:
            self.image = pygame.transform.flip(self.image, True, False)

class Water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        water_img = pygame.image.load('Tile_10.png')
        self.image = pygame.transform.scale(water_img,(tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        spike_img = pygame.image.load('spike.png')
        self.image = pygame.transform.scale(spike_img,(tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        



        
#GAME WORLD DESIGN
world_data = [
[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
,
[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 5, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
,
[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 5, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
]

player = Player(100, screen_height - 900)

slug_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()


def runworld(x):
    world = World(x)
    return world

#create buttons
restart_button = Button(screen_width // 2 - 400, screen_height // 2 + 150, restart_img)
level1_button = Button(screen_width // 2 - 400, screen_height // 2 + 50, level1_img)
level2_button = Button(screen_width // 2 - 400, screen_height // 2 + 150, level2_img)
back_button = Button(screen_width-150, 50, back_img)
 
#  white .
white = (255, 255, 255)
 
# assigning values to X and Y variable
X = screen_width
Y = screen_height
 
# create the display surface object
# of specific dimension..e(X, Y).
display_surface = pygame.display.set_mode((X, Y))
 
# set the pygame window name
pygame.display.set_caption('Show Text')
 
# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pygame.font.Font('freesansbold.ttf', 15)
 
# create a text surface object,
# on which text is drawn on it.
content = """Rubes Goldberg Machine"""
text = font.render(content, True, white)
 
# create a rectangular object for the
# text surface object
textRect = text.get_rect()
 
# set the center of the rectangular object.
textRect.center = (screen_width // 2 - 350, screen_height // 2 + 420)

status = 0 #lobby

def createExtras():
    water_group.draw(screen)
    spike_group.draw(screen)
    slug_group.update()
    slug_group.draw(screen)
    
#GAME RUNNING
run = True
while run:
    clock.tick(fps)
    screen.blit(bg_img,(0,0))
    if status ==0:
        world = runworld(world_data[0])
        world.draw()
        if level1_button.draw():
            player.reset(100, screen_height - 900)
            status = 1
        if level2_button.draw():
            player.reset(100, screen_height - 900)
            status = 2
            
    if status ==1:
        createExtras()
        world = runworld(world_data[1])
        world.draw()
        if back_button.draw():
            player.reset(100, screen_height - 900)
            status = 0
            
    if status ==2:
        createExtras()
        world = runworld(world_data[2])
        world.draw()
        if back_button.draw():
            player.reset(100, screen_height - 900)
            status = 0
    #if x == world_data[0]:
        #if level1_button.draw():
            #world_data[1]
        #level2_button.draw()

    display_surface.blit(text,textRect)

    game_over = player.update(game_over)

    

    if game_over == -1: #when player died
        if restart_button.draw():
            player.reset(100, screen_height - 900)
            game_over = 0

    #draw_grid()

    print(world.tile_list)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()