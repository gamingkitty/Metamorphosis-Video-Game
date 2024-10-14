import pygame

pygame.font.init()
pygame.mixer.init()

default_font = pygame.font.SysFont("calibri", 36)
italic_default_font = pygame.font.SysFont("calibri", 36, italic=True)
talk_sound = pygame.mixer.Sound("./Sound/Talk Noise.mp3")
talk_sound.set_volume(0.4)

other_talk_sound = pygame.mixer.Sound("./Sound/Other Talk Noise.mp3")
other_talk_sound.set_volume(0.4)


def wrap_text(text, max_width):
    words = text.split()
    lines = []
    current_line = ""

    special_char_length = 0

    for word in words:
        if word[:2] == "\\c" or word[:2] == "\\p" or word[:2] == "\\r" or word[:2] == "\\i" or word[:2] == "\\o":
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

        self.sound_cooldown = 0.12
        self.sound_timer = 0.12
        self.is_other_sound = False

        self.current_line = 0
        self.current_word = 0
        self.current_char = 0

        self.current_color = (255, 255, 255)
        self.is_italic = False

        special_char_check = self.lines[0][0]

        while special_char_check[:2] == "\\c" or special_char_check[:2] == "\\p" or special_char_check[:2] == "\\r" or special_char_check[:2] == "\\i" or special_char_check[:2] == "\\o":
            self.handle_special_char(special_char_check)
            self.current_char = 0
            self.current_word += 1
            if not self.is_done():
                special_char_check = self.get_current_word()
            else:
                break

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
                return False

            new_word_text = self.get_current_word()
            while new_word_text[:2] == "\\c" or new_word_text[:2] == "\\p" or new_word_text[:2] == "\\r" or new_word_text[:2] == "\\i" or new_word_text[:2] == "\\o":
                self.handle_special_char(new_word_text)

                self.current_char = 0
                self.current_word += 1
                if self.current_word >= len(self.get_current_line()):
                    self.current_word = 0
                    self.current_line += 1
                    is_new_line = True

                if not self.is_done():
                    new_word_text = self.get_current_word()
                else:
                    break

        return is_new_line

    def render_next_char(self):
        rendered_char = None
        if self.is_italic:
            rendered_char = italic_default_font.render(self.get_current_char(), True, self.current_color)
        else:
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

            self.sound_timer += delta_time
            if self.reveal_timer < 0:
                self.sound_timer = min(self.sound_timer, self.sound_cooldown)
            if self.reveal_timer >= 0 and self.sound_timer >= self.sound_cooldown:
                self.sound_timer -= self.sound_cooldown
                if not self.is_other_sound:
                    talk_sound.play()
                else:
                    other_talk_sound.play()

    def skip(self):
        while not self.is_done():
            self.render_next_char()

    def handle_special_char(self, special_char):
        if special_char[:2] == "\\c":
            rgb = special_char[3:len(special_char)].split(",")
            rgb[2] = rgb[2].rstrip(" ")
            self.current_color = (int(rgb[0]), int(rgb[1]), int(rgb[2][:-1]))
        elif special_char[:2] == "\\p":
            time = int(special_char[2:len(special_char)]) / 1000
            self.reveal_timer -= time
        elif special_char[:2] == "\\r":
            new_cooldown = int(special_char[2:len(special_char)]) / 1000
            self.reveal_cooldown = new_cooldown
            self.sound_cooldown = new_cooldown * 4
        elif special_char[:2] == "\\i":
            self.is_italic = not self.is_italic
        else:
            self.is_other_sound = not self.is_other_sound

    def set_text(self, text):
        self.current_line = 0
        self.current_word = 0
        self.current_char = 0
        self.current_color = (255, 255, 255)
        self.char_blit_position = (0, 0)

        self.text_surface = pygame.Surface((self.text_box.get_width() - 60, self.text_box.get_height() - 60))
        self.text_surface.fill((0, 0, 0))

        self.reveal_timer = 0
        self.reveal_cooldown = 0.03

        self.sound_cooldown = 0.12
        self.sound_timer = 0.12
        self.is_other_sound = False

        self.is_italic = False

        self.lines = [[word + " " for word in line.split()] for line in wrap_text(text, self.text_box.get_width() - 60)]
        for line in self.lines:
            line[-1] = line[-1][:-1]

        special_char_check = self.lines[0][0]

        while special_char_check[:2] == "\\c" or special_char_check[:2] == "\\p" or special_char_check[:2] == "\\r" or special_char_check[:2] == "\\i" or special_char_check[:2] == "\\o":
            self.handle_special_char(special_char_check)
            self.current_char = 0
            self.current_word += 1
            if not self.is_done():
                special_char_check = self.get_current_word()
            else:
                break
