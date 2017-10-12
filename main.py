import pygame
import math

pygame.init()
picture = pygame.image.load('murica.jpg')
screen = pygame.display.set_mode((640,480))

def pixelSearch(picture, area, colour):
    pixels = pygame.PixelArray(picture)
    for x in xrange(0, picture.get_width()):
        for y in xrange(0, picture.get_height()):
            pixelColour = picture.unmap_rgb(pixels[x, y])
    del pixels

def colourDistance(colourOne, colourTwo):
    distance = math.sqrt(pow(colourOne.r-colourTwo.r, 2) + pow(colourOne.g-colourTwo.g, 2) + pow(colourOne.b-colourTwo.b, 2))
    return distance

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    screen.blit(picture, (0, 0))
    pygame.display.flip()