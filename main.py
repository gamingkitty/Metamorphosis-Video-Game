import pygame
import sys


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

    while True:
        screen.fill(black)
        delta_time = clock.tick(fps) / 1000
        screen.blit(font.render("Hello, World!", True, white), (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()


if __name__ == "__main__":
    main()
