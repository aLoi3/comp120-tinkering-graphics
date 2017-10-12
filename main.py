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


# main thing
pygame.init()
picture = pygame.image.load('murica.png')
picture = picture.convert(24)
#palette = pygame.image.load('palette.png')
#palette = picture.convert(24)
screen = pygame.display.set_mode((640, 480))
colour_under_mouse = pygame.Color (0,0,0)
colour_on_palette = pygame.Color (255,255,255)

# test with hollywood-style whitewashing
#pixel_search(picture, pygame.Color(105, 54, 51), pygame.Color(231, 213, 201), 40)

# temporarily scale up the picture
picture = pygame.transform.scale(picture, (picture.get_width() * 4, picture.get_height() * 4))

running = True
while running:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT or
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
            running = False
        mouse_position = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            #pixel_search(picture, colour_under_mouse, pygame.Color(255, 255, 255), 20)
            thingy = picture.get_rect()
            if thingy.collidepoint(mouse_position):
                colour_under_mouse = picture.get_at(mouse_position)


    screen.blit(picture, (0, 0))
    #screen.blit(palette, (6, 36))
    pygame.display.flip()
