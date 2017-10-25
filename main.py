# Standard library imports
import pygame
import math
# Third party imports
import tkFileDialog

# Parameters
COLOUR_THRESHOLD = 20
PICTURE_WIDTH = 256
PICTURE_HEIGHT = 256


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
    """Saves the image to a user-selected file name

    Arguments:
        picture -- Image to save
    Returns:
        None
    """
    file_path = tkFileDialog.asksaveasfilename(
        title='Save image',
        filetypes=[('PNG image', '*.png'), ('JPG image', '*.jpg'),
                   ('BMP image', '*.bmp')])

    # Only save if file_path returned a valid path
    if file_path is not '':
        pygame.image.save(picture, file_path)


# Init PyGame
pygame.init()

# Load colour palette image
palette = pygame.image.load('palette.png')
palette = palette.convert(24)

# Load main image (scaled to PICTURE_WIDTH and HEIGHT)
picture = pygame.image.load('image.png')
picture = pygame.transform.scale(picture, (PICTURE_WIDTH, PICTURE_HEIGHT))
picture = picture.convert(24)

# Init image-related variables
colour_on_picture = None  # the user-selected picture colour to replace
colour_on_palette = None  # the user-selected replacement colour on the palette

picture_x = 0  # position of the editable picture
picture_y = 0
palette_x = picture.get_width()  # position of the palette
palette_y = 0

# Load minimalist UI and init variables
info_text_font = pygame.font.SysFont('Calibri', 24, True)
info_text_lines = ['Click somewhere on the picture to pick a colour',
                   'Then click on the palette to replace that colour!',
                   'Press ESC to save and quit']
info_text_surfaces = []

info_text_y = max(picture.get_height(), palette.get_height())
info_text_height = 0  # total height of UI text area

# Pre-render UI text from the list of text lines above
for index, line in enumerate(info_text_lines):
    info_text_surfaces.append(
        info_text_font.render(line, True, (255, 255, 255)))
    info_text_height += info_text_surfaces[index].get_height()

# Init window
window_width = picture.get_width() + palette.get_width()
window_height = info_text_y + info_text_height
screen = pygame.display.set_mode((window_width, window_height))

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

    # Clear the screen (needed for the text antialiasing to look good)
    screen.fill((0, 0, 0))

    # Render images
    screen.blit(picture, (picture_x, picture_y))
    screen.blit(palette, (palette_x, palette_y))

    # Render UI text
    current_y = info_text_y
    for text_surface in info_text_surfaces:
        screen.blit(text_surface, (0, current_y))
        current_y += text_surface.get_height()

    # Splat!
    pygame.display.flip()
