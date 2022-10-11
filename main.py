import pygame
import sys
import PIL
import player
import level

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.key.set_repeat(1)
clock = pygame.time.Clock()

screenWidth = 1280
screenHeight = 720
bgcolor = [33, 38, 63]

screen = pygame.display.set_mode([screenWidth, screenHeight])
screen.fill(bgcolor)

world = level.Level(screen)
adv = player.Player(world)

while True:
    screen.fill(bgcolor)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        adv.run("right")
    if keys[pygame.K_a]:
        adv.run("left")
    if keys[pygame.K_w]:
        adv.jump()
    
    world.do()
    adv.do()
    world.doLiquid()

    debug = [f"speed: {str(adv.x_vel)}",
            f"xpos: {str(adv.position[0])}",
            f"ypos: {str(adv.position[1])}",
            f"landed: {str(adv.landed)}"]
            
    font = pygame.font.SysFont("arial", 16)
    for i in range(len(debug)):
        text = font.render(debug[i], True, "white")
        screen.blit(text, [0, i * 32])

    clock.tick(120)
    pygame.display.flip()