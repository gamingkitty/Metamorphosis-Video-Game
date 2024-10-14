class Scene:
    def __init__(self, texts, text_box, background_img, options):
        self.texts = texts
        self.current_text = 0

        self.text_box = text_box
        self.text_box.set_text(self.get_current_text())

        self.background_img = background_img
        self.options = options

        self.chosen_option = None

        self.option_click_cooldown = 0.5

    def load(self, screen):
        screen.blit(self.background_img, (0, 0))
        self.text_box.load(screen)
        if self.at_decision():
            for option in self.options:
                option.load(screen)

    def move(self, delta_time):
        self.text_box.move(delta_time)

        if self.at_decision():
            for option in self.options:
                option.move()

            if self.option_click_cooldown != 0:
                self.option_click_cooldown -= delta_time
                if self.option_click_cooldown < 0:
                    self.option_click_cooldown = 0

    def handle_mouse_down(self):
        if self.at_decision() and self.option_click_cooldown == 0:
            for option in self.options:
                option.handle_mouse_down()

        if not self.text_box.is_done():
            self.text_box.skip()
        elif not self.at_decision():
            self.current_text += 1
            self.text_box.set_text(self.get_current_text())

    def handle_mouse_up(self):
        if self.at_decision() and self.option_click_cooldown == 0:
            for option in self.options:
                if option.handle_mouse_up():
                    self.chosen_option = option
                    self.option_click_cooldown = 0.5

    def at_decision(self):
        return self.current_text >= len(self.texts) - 1 and self.text_box.is_done()

    def get_current_text(self):
        return self.texts[self.current_text]

    def get_chosen_option(self):
        return self.chosen_option

    def reset(self, texts, background_img, options):
        self.texts = texts
        self.current_text = 0

        self.text_box.set_text(self.get_current_text())

        self.background_img = background_img
        self.options = options

        self.chosen_option = None
