import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
import time
pygame.init()

pygame.display.set_caption("Python-Platformer")

WIDTH,HEIGHT = 1920,1000
FPS = 60
PLAYER_VEL = 6
LEVEL=1
PLAYER_HEALTH=200
GAME_OVER = False
END = False
HEALTH_COLOR=(0,250,0)


window = pygame.display.set_mode((WIDTH, HEIGHT))

def flip(sprites):
    return [pygame.transform.flip(sprite ,True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("/home/yogi/workspace/PMA/Python-Platformer/assets",dir1,dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}
    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites=[]
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width,height),pygame.SRCALPHA,32)
            rect = pygame.Rect(i * width,0, width, height)
            surface.blit(sprite_sheet,(0,0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png","") + "_right"] = sprites
            all_sprites[image.replace(".png","") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png","")] = sprites

    return all_sprites

def get_block(size):
    path = join("/home/yogi/workspace/PMA/Python-Platformer/assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size,size), pygame.SRCALPHA, 32)
    bloc=0
    if LEVEL == 2:
        bloc = 64
    rect = pygame.Rect(96, bloc, size, size)
    surface.blit(image, (0,0), rect)
    return pygame.transform.scale2x(surface)

class Player(pygame.sprite.Sprite):
    COLOR=(255,0,0)
    GRAVITY = 1
    SPRITES= load_sprite_sheets("MainCharacters", "MaskDude", 32, 32, True)
    ANIMATION_DELAY=3

    def __init__(self,x,y,width,height):
        super().__init__()
        self.rect = pygame.Rect(x,y,width,height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x +=dx
        self.rect.y +=dy

    def make_hit(self):
        global PLAYER_HEALTH
        global GAME_OVER
        PLAYER_HEALTH-=5
        if PLAYER_HEALTH <= 0:
            GAME_OVER = True
        self.hit = True
        self.hit_count = 0

    def move_left(self,vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0
    
    def move_right(self,vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel,self.y_vel)

        if self.hit:
            self.hit_count+=1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1
    
    def update_sprite(self):
        sprite_sheet="idle"
        if self.hit:
            sprite_sheet = "hit"
        if self.y_vel < 0 :
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"    
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name=sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x,self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)


    def draw(self, win, offset_x):
        win.blit(self.sprite,(self.rect.x - offset_x,self.rect.y))

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width,height),pygame.SRCALPHA)
        self.width=width
        self.height=height
        self.name=name
    
    def draw(self,win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block= get_block(size)
        self.image.blit(block,(0,0))
        self.mask = pygame.mask.from_surface(self.image)


class End(Object):
    ANIMATION_DELAY = 5
    def __init__(self,x,y, width, height):
        super().__init__(x,y,width,height,"end")
        self.end = load_sprite_sheets("Items/Checkpoints","End",width,height)
        self.image = self.end["End (Pressed) (64x64)"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count=0
        self.animation_name="End (Pressed) (64x64)"

    def loop(self):
        sprites = self.end[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x,self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0



class Fire(Object):
    ANIMATION_DELAY = 3
    def __init__(self,x,y, width, height):
        super().__init__(x,y,width,height,"fire")
        self.fire = load_sprite_sheets("Traps","Fire",width,height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count=0
        self.animation_name="off"

    def on(self):
        self.animation_name="on"

    def off(self):
        self.animation_name="off"

    def loop(self):

        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x,self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


def get_background(name):
    image = pygame.image.load(join("/home/yogi/workspace/PMA/Python-Platformer/assets","Background",name))
    _,_,width,height = image.get_rect()
    tiles=[]

    for i in range(WIDTH // width +1):
        for j in range(HEIGHT // height +1):
            pos = (i * width,j * height)
            tiles.append(pos)
    return tiles,image

def draw(window, background, bg_image, player, objects, offset_x):
    global GAME_OVER
    global HEALTH_COLOR
    pygame.draw.rect(window, (0,0,0), pygame.Rect(30, 30, 60, 60))
    if GAME_OVER == True:
        window.fill((255,50,50))
        pygame.display.flip()

        font = pygame.font.SysFont("Impact", 75)
        txtsurf = font.render("GAME OVER!!", True, (255,255,0))
        window.blit(txtsurf,(WIDTH // 2 - 150, HEIGHT // 2))
        pygame.display.update()

        time.sleep(2)
        return        
    
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)
    player.draw(window, offset_x)
    
    if PLAYER_HEALTH < 200 and PLAYER_HEALTH > 150:
        HEALTH_COLOR = (63.75,191.25,0)
    elif PLAYER_HEALTH < 150 and PLAYER_HEALTH > 100:
        HEALTH_COLOR = (127.5,127.5,0)
    elif PLAYER_HEALTH < 100 and PLAYER_HEALTH > 50:
        HEALTH_COLOR = (191.25,63.75,0)
    elif PLAYER_HEALTH < 50 and PLAYER_HEALTH > 0:
        HEALTH_COLOR = (255,0,0)
    


    pygame.draw.rect(window, HEALTH_COLOR, pygame.Rect(1650, 60, PLAYER_HEALTH, 30))
    pygame.display.update()

def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player,obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()
            collided_objects.append(obj)

    return collided_objects

def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object=None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break
    
    player.move(-dx, 0)
    player.update()
    return collided_object

def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)


    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left,collide_right, *vertical_collide]
    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()
        if obj and obj.name == "end":
            next_level()

def getObjects(level,block_size):
    floor=getFloor(1,block_size)
    fires=getFire(level,block_size)
    end=getEnd(level,block_size)
    blocks=getBlocks(level,block_size)
    obj=[*floor]
    for block in blocks:
        obj.append(block)
    for fire in fires:
        obj.append(fire)
    obj.append(end)
    return obj, fires, end

def getBlocks(level,block_size):
    if level == 1:
        blocks=[Block(310, HEIGHT - block_size * 2, block_size),Block(block_size * 7, HEIGHT - block_size * 4, block_size),Block(block_size * 8, HEIGHT - block_size * 4, block_size)
        ,Block(block_size * 9, HEIGHT - block_size * 4, block_size),Block(block_size * 10, HEIGHT - block_size * 4, block_size),Block(block_size * 15, HEIGHT - block_size * 2, block_size),
        Block(block_size * 18, HEIGHT - block_size * 2, block_size),Block(block_size * 18, HEIGHT - block_size * 3, block_size),Block(block_size * 18, HEIGHT - block_size * 4, block_size),
        Block(block_size * 21, HEIGHT - block_size * 2, block_size),Block(block_size * 21, HEIGHT - block_size * 3, block_size),Block(block_size * 21, HEIGHT - block_size * 4, block_size),
        Block(block_size * 21, HEIGHT - block_size * 5, block_size),Block(block_size * 21, HEIGHT - block_size * 6, block_size)]
    
    if level == 2:
        blocks=[Block(380 , HEIGHT - block_size * 3, block_size),Block(380 , HEIGHT - block_size * 4, block_size),Block(380 , HEIGHT - block_size * 5, block_size),Block(380 , HEIGHT - block_size * 6, block_size),
        Block(380 , HEIGHT - block_size * 7, block_size),Block(380 , HEIGHT - block_size * 8, block_size),Block(380 , HEIGHT - block_size * 9, block_size),Block(380 , HEIGHT - block_size * 10, block_size),Block(380 , HEIGHT - block_size * 11, block_size),
        Block(845 , HEIGHT - block_size * 3, block_size),Block(940 , HEIGHT - block_size * 3, block_size),Block(1035 , HEIGHT - block_size * 3, block_size),Block(1130 , HEIGHT - block_size * 3, block_size),Block(1225 , HEIGHT - block_size * 2, block_size),
        Block(1225 , HEIGHT - block_size * 3, block_size),Block(1225 , HEIGHT - block_size * 4, block_size),Block(1225 , HEIGHT - block_size * 5, block_size),Block(1225 , HEIGHT - block_size * 6, block_size),
        Block(1225 , HEIGHT - block_size * 7, block_size),Block(1225 , HEIGHT - block_size * 8, block_size),Block(1225 , HEIGHT - block_size * 9, block_size),Block(1225 , HEIGHT - block_size * 10, block_size),Block(1225 , HEIGHT - block_size * 11, block_size),
        Block(475 , HEIGHT - block_size * 5, block_size),Block(570 , HEIGHT - block_size * 5, block_size),Block(940 , HEIGHT - block_size * 7, block_size),Block(1035 , HEIGHT - block_size * 7, block_size),Block(1130 , HEIGHT - block_size * 7, block_size)]
    return blocks

def getEnd(level,block_size):
    if level == 1:
        end=End(2500, HEIGHT - block_size - 300, 64, 64)
    if level == 2:
        end=End(1115, HEIGHT - block_size * 8.3, 64, 64)
    return end

def getFire(level,block_size):
    fires=[]
    if level == 1:
        fires=[Fire(800, HEIGHT - block_size - 350, 16, 32),Fire(1300, HEIGHT - block_size - 64, 16, 32),Fire(1575, HEIGHT - block_size - 64, 16, 32),Fire(1670, HEIGHT - block_size - 64, 16, 32),
        Fire(1875, HEIGHT - block_size - 64, 16, 32),Fire(1950, HEIGHT - block_size - 64, 16, 32)]
    
    if level == 2:
        fires=[Fire(700, HEIGHT - block_size - 64, 16, 32)]

    return fires


def getFloor(level,block_size):
        return [Block(i*block_size, HEIGHT - block_size,block_size) for i in range(-WIDTH // block_size,WIDTH * 4// block_size)]

def next_level():
    global LEVEL, END
    if LEVEL == 1:
        LEVEL += 1
        main()
    else:
        END = True

def main():
    global window
    clock = pygame.time.Clock()
    block_size = 96
    player = Player(100,100,50,50)


    if LEVEL ==1:
        background,bg_image = get_background("Blue.png")
        objects, fires, end = getObjects(1,block_size)
    else:
        background,bg_image = get_background("Green.png")
        objects, fires, end = getObjects(2,block_size)

    for fire in fires:
        fire.on()

    offset_x = 0
    scroll_area_width = 200
    
    run = True
    while run:
        clock.tick(FPS)

        if END == True:
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        player.loop(FPS)
        for fire in fires:
            fire.loop()
        end.loop()
        handle_move(player, objects)
        draw(window, background, bg_image, player, objects, offset_x)

        if(player.rect.right - offset_x >= WIDTH - scroll_area_width and player.x_vel > 0) or ((player.rect.left - offset_x <= scroll_area_width) and player.x_vel<0):
            offset_x += player.x_vel

        if GAME_OVER == True:
            run = False
    
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()