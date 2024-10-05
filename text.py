import pygame


pygame.font.init()


default_font = pygame.font.SysFont("georgia", 22)


def change_font_size(new_size):
    return pygame.font.SysFont("courier", new_size)


def make_text_surface(max_width, text, pos, font):
    color = (255, 255, 255)
    words = [word.split(' ') for word in text.splitlines()]
    space_width, space_height = font.size(' ')
    words_to_draw = []
    x, y = pos
    longest_line = 0
    for line in words:
        word_height = 0
        for word in line:
            # Check for color, which will be indicated by \\c followed by rgb, like \\c(255,255,255)
            if word[:2] == "\\c":
                rgb = word[3:len(word) - 1].split(",")
                color = (int(rgb[0]), int(rgb[1]), int(rgb[2]))
            # Check for size, changes the size of the text.
            elif word[:2] == "\\s":
                new_size = int(word[2:])
                font = change_font_size(new_size)
            else:
                word_surface = font.render(word, True, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    if x > longest_line:
                        longest_line = x
                    x = pos[0]
                    y += word_height
                words_to_draw.append([x, y, word_surface])
                x += word_width + space_width
        if x > longest_line:
            longest_line = x
        x = pos[0]
        y += word_height

    text_surface = pygame.Surface((longest_line, y))

    for word_to_draw in words_to_draw:
        text_surface.blit(word_to_draw[2], (word_to_draw[0], word_to_draw[1]))

    return text_surface


def wrap_text(text, max_width):
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            if word[:2] == "\\c":
                current_line = word + " "
            else:
                test_line = current_line + word + " "
                # Check if the line width exceeds the max width
                if default_font.size(test_line)[0] > max_width:
                    lines.append(current_line.strip())  # Add the current line to lines
                    current_line = word + " "  # Start a new line with the current word
                else:
                    current_line = test_line

        if current_line:
            lines.append(current_line.strip())  # Add the last line

        return lines


class Text:
    def __init__(self, text, text_box, text_box_position):
        self.lines = wrap_text(text, text_box.get_width() - 60)
        self.text_box = text_box
        self.text_box_position = text_box_position
        self.text_surface = pygame.Surface((text_box.get_width() - 60, self.text_box.get_height() - 60))
        self.text_surface.fill((0, 0, 0))
        self.text_surface_position = (self.text_box_position[0] + ((self.text_box.get_width() - (text_box.get_width() - 60)) / 2),
                                      self.text_box_position[1] + 30)
        self.reveal_cooldown = 0.5
        self.reveal_timer = 0

        self.current_line = 0
        self.current_char = 0

    def load(self, screen):
        screen.blit(self.text_box, self.text_box_position)
        screen.blit(self.text_surface, self.text_surface_position)

    def increment_char(self):
        self.current_char += 1
        if self.current_char >= len(self.lines[self.current_line]):
            self.current_char = 0
            self.current_line += 1

    def move(self, delta_time):
        self.reveal_timer += delta_time
        if self.reveal_timer >= self.reveal_cooldown:
            self.reveal_timer -= self.reveal_cooldown
            chat_to_print


