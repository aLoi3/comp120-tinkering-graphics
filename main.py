# Standard library imports
import pygame
import math
# Third party imports
import tkFileDialog

# Parameters
PICTURE_SCALE = 4
COLOUR_THRESHOLD = 20


# Functions
def replace_surface_colours(picture,
                            find_colour,
                            replacement_colour,
                            threshold):
    """Replaces all colours on a Surface with another, when within a
       colour similarity threshold

    Arguments:
        picture (Surface) -- the Surface to be affected
        find_colour (pygame.Color) -- the colour to be replaced
        replacement_colour (pygame.Color) -- the colour to replace it
                                             with
        threshold (int) -- the tolerance when comparing pixels with
                           find_colour
    Returns:
        Nothing
    """
    pixels = pygame.PixelArray(picture)
    # Loop through all pixels in image to find and replace colours
    for x in xrange(picture.get_width()):
        for y in xrange(picture.get_height()):
            pixel_colour = picture.unmap_rgb(pixels[x, y])
            if colour_close_enough(pixel_colour, find_colour, threshold):
                pixel_colour = replacement_colour
            pixels[x, y] = picture.map_rgb(pixel_colour)
    del pixels


def colour_distance(colour_one, colour_two):
    """Finds the distance between two colours and returns this distance

    Arguments:
        colour_one -- First colour to check
        colour_two -- Second colour to check against
    Returns:
        (float) Distance between the colours
    """
    distance = math.sqrt(pow(colour_one.r - colour_two.r, 2)
                         + pow(colour_one.g - colour_two.g, 2)
                         + pow(colour_one.b - colour_two.b, 2))
    return distance


def colour_close_enough(colour_one, colour_two, threshold):
    """Returns whether two colours are within a certain distance to each
       other

    Arguments:
        colour_one -- First colour to check
        colour_two -- Second colour to check again
        threshold -- Distance threshold between them
    Returns:
        (bool) Whether the colour distance is smaller than the threshold
    """
    return colour_distance(colour_one, colour_two) < threshold


def save_image(picture):
    """Saves the image to a user-selected file name"""
    file_path = tkFileDialog.asksaveasfilename(
        title='Save image',
        filetypes=[('PNG image', '*.png'), ('JPG image', '*.jpg'),
                   ('BMP image', '*.bmp')])

    # Only save if file_path returned a valid path
    if file_path is not '':
        pygame.image.save(picture, file_path)


# Init PyGame
pygame.init()

# Load images
picture = pygame.image.load('murica.png')
palette = pygame.image.load('palette.png')
picture = picture.convert(24)
palette = palette.convert(24)

# Scale up the editable picture
picture = pygame.transform.scale(picture,
                                 (picture.get_width() * PICTURE_SCALE,
                                  picture.get_height() * PICTURE_SCALE))

# Init window
screen = pygame.display.set_mode((picture.get_width() + palette.get_width(),
                                  palette.get_height()))

# Init variables
colour_on_picture = None  # the user-selected picture colour to replace
colour_on_palette = None  # the user-selected replacement colour on the palette

picture_x = 0  # position of the editable picture
picture_y = 0
palette_x = picture.get_width()  # position of the palette
palette_y = 0

# Begin main loop
running = True
while running:
    # PyGame event loop
    for event in pygame.event.get():
        if (event.type == pygame.QUIT or
                (event.type == pygame.KEYDOWN and
                 event.key == pygame.K_ESCAPE)):
            save_image(picture)
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Prepare to compare mouse position to picture and palette
            # position
            mouse_position = pygame.mouse.get_pos()
            picture_rect = picture.get_rect().move(picture_x, picture_y)
            palette_rect = palette.get_rect().move(palette_x, palette_y)

            if picture_rect.collidepoint(mouse_position):
                # If mouse is within image, select the colour to replace
                relative_mouse_position = (
                    mouse_position[0] - picture_x,
                    mouse_position[1] - picture_y)

                colour_on_picture = picture.get_at(relative_mouse_position)
            elif palette_rect.collidepoint(mouse_position):
                # If the mouse is within the palette, replace the
                # colour(s) with the colour of the pixel under the mouse
                if colour_on_picture is not None:
                    relative_mouse_position = (
                        mouse_position[0] - palette_x,
                        mouse_position[1] - palette_y)

                    replace_surface_colours(
                        picture, colour_on_picture,
                        palette.get_at(relative_mouse_position),
                        COLOUR_THRESHOLD)

    # Render to screen
    screen.blit(picture, (picture_x, picture_y))
    screen.blit(palette, (palette_x, palette_y))
    pygame.display.flip()
