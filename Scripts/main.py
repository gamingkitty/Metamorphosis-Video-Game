import math
import pygame
import sys
import text
import option
import scene


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
    current_time = 0

    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    white = (255, 255, 255)
    gray = (40, 40, 40)

    bed_scene_image = scale_background_image(pygame.image.load("./Images/Scenes/Bed Scene.png"), screen_size)

    clock_image = pygame.image.load("./Images/Scenes/Clock.png")
    clock_position = ((screen_width - clock_image.get_width()) / 2, (screen_height - clock_image.get_height()) / 2)

    brightness_screen = pygame.Surface(screen_size)
    brightness_screen.fill(black)

    effective_screen_size = bed_scene_image.get_size()

    text_box = pygame.image.load("./Images/Text/Text Box.png")
    text_box = pygame.transform.scale(text_box, (bed_scene_image.get_width() - 300,
                                                 text_box.get_height() * ((bed_scene_image.get_width() - 600) / text_box.get_width())))
    text_box = text.Text("Hello this is a test let me \\p1000 test some more stuff now, like color, here I will do another color: \\c(255,0,12) this should be reddish now right, ok now lets turn back \\c(255,255,255) ok now lets try size: ok lets see if this worked lets test by going toa new line and seeing how it works lets go lmao I am not sure how this is going to work at all lololololol", text_box, ((screen_width - text_box.get_width()) / 2, effective_screen_size[1] - text_box.get_height() - 30))

    option_background = pygame.image.load("./Images/Text/Option Background.png")
    option_background = pygame.transform.scale(option_background, (option_background.get_width() * 2, option_background.get_height() * 2))

    option_1 = option.Option("Option 1", option_background, (screen_width / 2, (screen_height / 2) - 300))
    option_2 = option.Option("Option 2", option_background, (screen_width / 2, (screen_height / 2) - 100))
    options = [option_1, option_2]

    current_cutscene = "start"
    cutscene_start_time = None

    alarm_clock = pygame.mixer.Sound("./Sound/Alarm Clock Sound.mp3")
    alarm_clock_playing = False

    background_noise = pygame.mixer.Sound("./Sound/Background Noise.mp3")
    background_noise.set_volume(0.05)

    texts_opt_1 = ["u chose option 1", "Ok now go back to the start"]
    texts_opt_2 = ["u chose option 2", "Ok now you have to choose option 1"]

    current_scene = scene.Scene(["Text 1 blah blah blah more blah pause \\p1000 blah blah", "text 2 hi hello how are you", "text 3 hola, hablas espanol?", "which option would you like to choose?"], text_box, bed_scene_image, options)
    scene_num = 0
    while True:
        delta_time = clock.tick(fps) / 1000
        current_time += delta_time

        if current_cutscene is not None:
            if cutscene_start_time is None:
                cutscene_start_time = current_time

            cutscene_time = current_time - cutscene_start_time

            # Here are the different cutscenes
            if current_cutscene == "start":
                if cutscene_time < 3:
                    screen.fill(black)
                    if not alarm_clock_playing:
                        alarm_clock.play()
                        alarm_clock_playing = True
                elif 3 <= cutscene_time <= 9:
                    clock_image.set_alpha(int((-1 * 128 * math.cos((5.2 * (cutscene_time - 3))) + 128)))
                    screen.fill(black)
                    screen.blit(clock_image, clock_position)
                elif 9 <= cutscene_time <= 10:
                    screen.fill(black)
                elif cutscene_time < 14:
                    if alarm_clock_playing:
                        alarm_clock.stop()
                        alarm_clock_playing = False
                    brightness_screen.set_alpha(255 - (20 * (cutscene_time - 10)))
                    screen.blit(bed_scene_image, (0, 0))
                    screen.blit(brightness_screen, (0, 0))
                elif cutscene_time > 15:
                    current_cutscene = None
                    cutscene_start_time = None
                    bed_scene_image.blit(brightness_screen, (0, 0))
                    background_noise.play(-1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            continue

        current_scene.load(screen)
        current_scene.move(delta_time)

        if scene_num == 0 and current_scene.get_chosen_option() == option_1:
            option_1.set_text("Go back to start")
            option_2.set_text("Go back to start")
            current_scene.reset(texts_opt_1, bed_scene_image, options)
            scene_num = 1
        elif scene_num == 0 and current_scene.get_chosen_option() == option_2:
            option_1.set_text("Go to option 1")
            option_2.set_text("Go to option 1")
            current_scene.reset(texts_opt_2, bed_scene_image, options)
            scene_num = 2
        elif scene_num == 2 and current_scene.get_chosen_option() is not None:
            option_1.set_text("Go back to start")
            option_2.set_text("Go back to start")
            current_scene.reset(texts_opt_1, bed_scene_image, options)
            scene_num = 1
        elif scene_num == 1 and current_scene.get_chosen_option() is not None:
            option_1.set_text("Option 1")
            option_2.set_text("Option 2")
            current_scene = scene.Scene(["Text 1 blah blah blah more blah pause \\p1000 blah blah", "text 2 hi hello how are you", "text 3 hola, hablas espanol?", "which option would you like to choose?"], text_box, bed_scene_image, options)
            scene_num = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    current_scene.handle_mouse_down()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    current_scene.handle_mouse_up()

        pygame.display.flip()


if __name__ == "__main__":
    main()
