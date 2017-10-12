import pygame
import math

def pixel_search(picture, find_colour, replacement_colour, threshold):
    pixels = pygame.PixelArray(picture)
    for x in xrange(0, picture.get_width()):
        for y in xrange(0, picture.get_height()):
            pixel_colour = picture.unmap_rgb(pixels[x, y])
            if colour_close_enough(pixel_colour, find_colour, threshold):
                pixel_colour = replacement_colour
            pixels[x, y] = picture.map_rgb(pixel_colour)
    del pixels


def colour_distance(colour_one, colour_two):
    distance = math.sqrt(pow(colour_one.r-colour_two.r, 2)
                         + pow(colour_one.g-colour_two.g, 2)
                         + pow(colour_one.b-colour_two.b, 2))
    return distance


def colour_close_enough(colour_one, colour_two, threshold):
    return colour_distance(colour_one, colour_two) < threshold

pygame.init()
picture = pygame.image.load('murica.jpg')
picture = picture.convert(24)
screen = pygame.display.set_mode((640, 480))

# temporarily scale up the picture
picture = pygame.transform.scale(picture, (picture.get_width() * 4, picture.get_height() * 4))

# test with hollywood-style whitewashing
pixel_search(picture, pygame.Color(105, 54, 51), pygame.Color(231, 213, 201), 40)

running = True
while running:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT or
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
            running = False

    screen.blit(picture, (0, 0))
    pygame.display.flip()
