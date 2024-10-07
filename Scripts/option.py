import pygame


pygame.font.init()


default_font = pygame.font.SysFont("georgia", 36)


class Option:
    def __init__(self, text, background, location):
        self.rendered_text = default_font.render(text, True, (255, 255, 255))
        self.text_location = (location[0] - self.rendered_text.get_width() / 2,
                              location[1] - self.rendered_text.get_height() / 2)
        self.background = background
        self.rect = pygame.Rect((0, 0), self.background.get_size())
        self.rect.center = location
        self.darken_surface = pygame.transform.scale(pygame.image.load("./Images/Text/Option Darken Surface.png"), self.rect.size)
        self.darken_surface.set_alpha(0)

        self.clicked = False

    def load(self, screen):
        screen.blit(self.background, self.rect)
        screen.blit(self.rendered_text, self.text_location)
        screen.blit(self.darken_surface, self.rect)

    def move(self):
        if not self.clicked:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.darken_surface.set_alpha(40)
            else:
                self.darken_surface.set_alpha(0)

    def handle_mouse_down(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.clicked = True
            self.darken_surface.set_alpha(87)

    def handle_mouse_up(self):
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            self.clicked = False
            self.darken_surface.set_alpha(0)
            return False
        elif self.clicked:
            return True

    def set_text(self, text):
        self.rendered_text = default_font.render(text, True, (255, 255, 255))
        self.text_location = (self.rect.centerx - self.rendered_text.get_width() / 2,
                              self.rect.centery - self.rendered_text.get_height() / 2)
        self.clicked = False
