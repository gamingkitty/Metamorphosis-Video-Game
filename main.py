import pygame
import sys
import text


def scale_background_image(image, screen_size):
    image_size = image.get_size()
    scene_scaler = min(screen_size[0] / image_size[0], screen_size[1] / image_size[1])
    scaled_image = pygame.transform.scale(image, (image_size[0] * scene_scaler, image_size[1] * scene_scaler))
    scaled_image_size = scaled_image.get_size()

    background_surface = pygame.Surface(screen_size)
    background_surface.fill((0, 0, 0))
    background_surface.blit(scaled_image, ((screen_size[0] - scaled_image_size[0]) / 2, (screen_size[1] - scaled_image_size[1]) / 2))
    return background_surface


def main():
    pygame.init()
    pygame.event.set_allowed([pygame.KEYDOWN, pygame.QUIT, pygame.KEYUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("The Metamorphosis")

    screen_size = screen.get_size()
    screen_width = screen_size[0]
    screen_height = screen_size[1]

    fps = 60
    clock = pygame.time.Clock()

    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    white = (255, 255, 255)
    gray = (40, 40, 40)

    font = pygame.font.SysFont("arial", 36)

    bed_scene_image = scale_background_image(pygame.image.load("./Images/Scenes/Bed Scene.webp"), screen_size)

    current_background = bed_scene_image
    effective_screen_size = current_background.get_size()

    text_box = pygame.image.load("./Images/Text Box.png")
    text_box = pygame.transform.scale(text_box, (current_background.get_width() - 500,
                                                 text_box.get_height() * ((current_background.get_width() - 500) / text_box.get_width())))
    test_text = text.Text("Hello this is a test let me test some more stuff now, like color, here I will do another color: \\c(255,0,12) this should be reddish now right, ok now lets turn back \\c(255,255,255) ok now lets try size: ok lets see if this worked lets test by going toa new line and seeing how it works lets go lmao I am not sure how this is going to work at all lololololol", text_box, ((screen_width - text_box.get_width()) / 2, effective_screen_size[1] - text_box.get_height() - 30))

    while True:
        screen.blit(bed_scene_image, (0, 0))
        delta_time = clock.tick(fps) / 1000
        test_text.load(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()


if __name__ == "__main__":
    main()
