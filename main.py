import pygame
import math


def replace_surface_colours(picture, find_colour, replacement_colour, threshold):
    pixels = pygame.PixelArray(picture)
    for x in xrange(picture.get_width()):
        for y in xrange(picture.get_height()):
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
palette = pygame.image.load('palette.png')
palette = palette.convert(24)
screen = pygame.display.set_mode((640, 480))
#colour_on_picture = pygame.Color(0, 0, 0)
#colour_on_palette = pygame.Color(255, 255, 255)

# temporarily scale up the picture
picture = pygame.transform.scale(picture, (picture.get_width() * 4, picture.get_height() * 4))

running = True
while running:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT or
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
            running = False
            pygame.image.save(picture, 'saved.png')
        mouse_position = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Act only if the mouse is in the areas of the picture or the palette.
            if picture.get_rect().collidepoint(mouse_position):
                colour_on_picture = picture.get_at(mouse_position)
            elif palette.get_rect().move(picture.get_width(), 0).collidepoint(mouse_position):  # unreadable?
                # Replace the prior chosen colour straight away (todo: add button?)
                relative_mouse_position = (mouse_position[0] - picture.get_width(), mouse_position[1])
                replace_surface_colours(picture, colour_on_picture, palette.get_at(relative_mouse_position), 20)

    screen.blit(picture, (0, 0))
    screen.blit(palette, (picture.get_width(), 0))
    pygame.display.flip()
