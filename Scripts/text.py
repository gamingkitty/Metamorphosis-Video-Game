import pygame

pygame.font.init()
pygame.mixer.init()

default_font = pygame.font.SysFont("calibri", 36)
talk_sound = pygame.mixer.Sound("./Sound/Talk Noise.mp3")
talk_sound.set_volume(0.4)


def wrap_text(text, max_width):
    words = text.split()
    lines = []
    current_line = ""

    special_char_length = 0

    for word in words:
        if word[:2] == "\\c" or word[:2] == "\\p":
            current_line = current_line + word + " "
            special_char_length += default_font.size(word + " ")[0]
        else:
            test_line = current_line + word + " "
            # Check if the line width exceeds the max width
            if default_font.size(test_line)[0] - special_char_length > max_width:
                lines.append(current_line.strip())  # Add the current line to lines
                current_line = word + " "  # Start a new line with the current word
                special_char_length = 0
            else:
                current_line = test_line

    if current_line:
        lines.append(current_line.strip())  # Add the last line

    return lines


class Text:
    def __init__(self, text, text_box, text_box_position):
        self.lines = [[word + " " for word in line.split()] for line in wrap_text(text, text_box.get_width() - 60)]
        for line in self.lines:
            line[-1] = line[-1][:-1]

        self.text_box = text_box
        self.text_box_position = text_box_position
        self.text_surface = pygame.Surface((text_box.get_width() - 60, self.text_box.get_height() - 60))
        self.text_surface.fill((0, 0, 0))
        self.text_surface_position = (self.text_box_position[0] + ((self.text_box.get_width() - (text_box.get_width() - 60)) / 2), self.text_box_position[1] + 30)

        self.char_blit_position = (0, 0)
        self.reveal_cooldown = 0.03
        self.reveal_timer = 0

        self.sound_cooldown = 0.125
        self.sound_timer = 0

        self.current_line = 0
        self.current_word = 0
        self.current_char = 0

        self.current_color = (255, 255, 255)

    def load(self, screen):
        screen.blit(self.text_box, self.text_box_position)
        screen.blit(self.text_surface, self.text_surface_position)

    def get_current_char(self):
        return self.lines[self.current_line][self.current_word][self.current_char]

    def get_current_word(self):
        return self.lines[self.current_line][self.current_word]

    def get_current_line(self):
        return self.lines[self.current_line]

    def is_done(self):
        return self.current_line >= len(self.lines)

    def increment_char(self):
        self.current_char += 1
        is_new_line = False
        if self.current_char >= len(self.get_current_word()):
            self.current_char = 0
            self.current_word += 1
            if self.current_word >= len(self.get_current_line()):
                self.current_word = 0
                self.current_line += 1
                is_new_line = True

            if self.is_done():
                return

            new_word_text = self.get_current_word()
            if new_word_text[:2] == "\\c" or new_word_text[:2] == "\\p":
                if new_word_text[:2] == "\\c":
                    rgb = new_word_text[3:len(new_word_text) - 1].split(",")
                    self.current_color = (int(rgb[0]), int(rgb[1]), int(rgb[2][:-1]))
                else:
                    time = int(new_word_text[2:len(new_word_text)]) / 1000
                    self.reveal_timer -= time

                self.current_char = 0
                self.current_word += 1
                if self.current_word >= len(self.get_current_line()):
                    self.current_word = 0
                    self.current_line += 1
                    is_new_line = True

        return is_new_line

    def render_next_char(self):
        rendered_char = default_font.render(self.get_current_char(), True, self.current_color)
        self.text_surface.blit(rendered_char, self.char_blit_position)
        if self.increment_char():
            self.char_blit_position = (0, self.char_blit_position[1] + rendered_char.get_height())
        else:
            self.char_blit_position = (self.char_blit_position[0] + rendered_char.get_width(), self.char_blit_position[1])

    def move(self, delta_time):
        if self.current_line < len(self.lines):
            self.reveal_timer += delta_time
            if self.reveal_timer >= self.reveal_cooldown:
                self.reveal_timer -= self.reveal_cooldown

                self.render_next_char()

            if self.reveal_timer >= 0:
                self.sound_timer += delta_time
                if self.sound_timer >= self.sound_cooldown:
                    self.sound_timer -= self.sound_cooldown
                    talk_sound.play()

    def skip(self):
        while not self.is_done():
            self.render_next_char()

    def set_text(self, text):
        self.current_line = 0
        self.current_word = 0
        self.current_char = 0
        self.current_color = (255, 255, 255)
        self.char_blit_position = (0, 0)

        self.text_surface = pygame.Surface((self.text_box.get_width() - 60, self.text_box.get_height() - 60))
        self.text_surface.fill((0, 0, 0))

        self.reveal_timer = 0

        self.lines = [[word + " " for word in line.split()] for line in wrap_text(text, self.text_box.get_width() - 60)]
        for line in self.lines:
            line[-1] = line[-1][:-1]
