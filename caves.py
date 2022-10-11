import pygame


def cave():
    sheet = pygame.image.load("cavesofgallet\cavesofgallet_tiles.png").convert()
    sheet = pygame.transform.scale(sheet, [sheet.get_width()*5, sheet.get_height()*5])
    sheet.set_colorkey([33, 38, 63])

    splitsheet = []
    for row in range(12):
        splitrow = []
        for col in range(8):
            tile = sheet.subsurface([col * 40, row * 40, 40, 40])
            splitrow.append(tile)
        splitsheet.append(splitrow)
    
    return splitsheet

def display():
    pygame.init()
    display = pygame.display.set_mode([1280, 720])
    
    sheet = cave()
    display.blit(sheet[1][2], [0, 0])

    while True:
        pygame.display.flip()