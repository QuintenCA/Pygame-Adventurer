import os
import pygame
import random
import level


class Player(pygame.Rect):
    def __init__(self, world:level.Level):
        super().__init__(0, 0, self.width, self.height)
        anims = {}

        for folder in os.listdir("player"):
            animlist = []
            for file in os.listdir("player/" + folder):
                animlist.append(pygame.image.load("player/" + folder + "/" + file).convert_alpha())
            anims.update({folder: animlist})

        self.world = world
        self.anims = anims
        self.current_animation = "idle"
        self.direction = "right"
        self.landed = False
        self.width = 30
        self.height = 60
        self.position = [0, 0]
        self.framecounter = 0
        self.image = self.anims[self.current_animation][0]
        self.animspeed = 0.5
        self.offset = [-35, -10]
        self.y_vel = 0
        self.x_vel = 0
        self.movespeed = 0.02
        self.accel = 0

    def run(self, direction="right"):
        if not self.landed:
            return

        if direction == "left":
            self.accel -= self.movespeed
        else:
            self.accel += self.movespeed

    def jump(self):
        if self.landed == False:
            return

        self.y_vel = -4
        self.landed = False

    def animate(self, a:str, loop=True, start=0):
        anim = self.anims[a]
        if a in ["idle", "run", "walk"]:
            self.current_animation = a

        if a != self.current_animation:
            self.framecounter = start

        frame = int(self.framecounter) % len(anim)
        if frame >= len(anim):
            self.framecounter = 0
            if not loop:
                frame = len(anim) - 1

        self.image = anim[frame]

        if self.direction == "left":

            self.image = pygame.transform.flip(self.image, True, False)

        self.world.screen.blit(self.image, [self.position[0] + self.offset[0], self.position[1] + self.offset[1]])
        self.framecounter += self.animspeed / 10

    def do(self):
        if self.x_vel > 0.1 and self.landed:
            self.direction = "right"
        elif self.x_vel < -0.1 and self.landed:
            self.direction = "left"

        self.animspeed = 1
        if abs(self.x_vel) > 1 and self. landed:
            self.animspeed = self.x_vel / 2
            self.animate("run")
        elif abs(self.x_vel) > 0.1 and self.landed:
            self.animspeed = self.x_vel
            self.animate("walk")
        elif self.y_vel < 0:
            self.animspeed = 0
            self.animate("jump", loop=False, start=2)

        elif self.yvel > 0 and not self.landed:
            self.animate("fall")
        else:
            self.animspeed = 0.5
            self.animate("idle")
        
        self.landed = False
        for tile in self.world.tiles:
            if self.colliderect(tile) and self.y_vel > 0:
                if self.bottom > tile.top:
                    self.position[1] = tile.top - self.height + 1
                    self.landed = True
                    self.y_vel = 0

        self.x_vel += self.accel
        
        self.position[0] += self.x_vel
        self.position[1] += self.y_vel

        self.update(self.position[0],
                    self.position[1],
                    self.width,
                    self.height)
        
        if self.landed and abs(self.x_vel) > 0:
            if self.accel == 0:
                self.x_vel *= 0.95
            else:
                self.x_vel *= 0.99
        else:
            self.x_vel *=  0.999

        if abs(self.x_vel) < 0.01:
            self.x_vel = 0
            
        self.y_vel += 0.1
        self.accel = 0