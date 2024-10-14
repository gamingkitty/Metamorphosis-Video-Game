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


def set_scene(scene_obj, scene_parameters, options):
    options_in_scene = []
    for i in range(len(scene_parameters[1])):
        options[i].set_text(scene_parameters[1][i][0])
        options_in_scene.append(options[i])
    scene_obj.reset(scene_parameters[0], scene_parameters[2], options_in_scene)


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
    door_scene_image = scale_background_image(pygame.image.load("./Images/Scenes/Door Scene.png"), screen_size)

    clock_image = pygame.image.load("./Images/Scenes/Clock.png")
    clock_position = ((screen_width - clock_image.get_width()) / 2, (screen_height - clock_image.get_height()) / 2)

    brightness_screen = pygame.Surface(screen_size)
    brightness_screen.fill(black)

    effective_screen_size = bed_scene_image.get_size()

    text_box_img = pygame.image.load("./Images/Text/Text Box.png")
    text_box_img = pygame.transform.scale(text_box_img, (bed_scene_image.get_width() - 300,
                                                 text_box_img.get_height() * ((bed_scene_image.get_width() - 600) / text_box_img.get_width())))
    text_box = text.Text("text", text_box_img, ((screen_width - text_box_img.get_width()) / 2, effective_screen_size[1] - text_box_img.get_height() - 30))
    cutscene_text_box = text.Text("text", text_box_img, ((screen_width - text_box_img.get_width()) / 2, effective_screen_size[1] - text_box_img.get_height() - 30))
    set_text = False

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

    hurt_sound = pygame.mixer.Sound("./Sound/Hurt.mp3")
    hurt_sound.set_volume(0.5)
    hurt_played = False

    door_bell_sound = pygame.mixer.Sound("./Sound/Door Bell.mp3")
    door_bell_played = False

    glitch_overlay = pygame.transform.scale(pygame.image.load("./Images/Effects/Glitch.png"), effective_screen_size)
    overlay_location = ((screen_size[0] - effective_screen_size[0]) / 2, (screen_size[1] - effective_screen_size[1]) / 2)
    glitched = False

    glitch_sound = pygame.mixer.Sound("./Sound/Glitch.mp3")
    glitch_played = False

    hurt_overlay = pygame.Surface(effective_screen_size)
    hurt_overlay.fill((100, 20, 20))

    hurt_times = 1
    set_hurt_times = False

    fall_sound = pygame.mixer.Sound("./Sound/Fall.mp3")
    fall_sound_played = False

    scurry_sound = pygame.mixer.Sound("./Sound/Scurry.mp3")
    scurry_sound_played = False

    door_open_sound = pygame.mixer.Sound("./Sound/Door Open.mp3")
    door_open_played = False

    door_slam_sound = pygame.mixer.Sound("./Sound/Door Slam.mp3")
    door_slam_played = False

    # How to format a scene, [texts], [(option 1 text, scene it goes to, cutscene to trigger), (option 2 text, scene it goes to, cutscene to trigger)], background_img
    scenes = [
        [["\\r50 Oh can't I sleep a little longer? \\p1000 I wish I could just forget my job and sleep through this dreary weather.",
          "\\r50 But I must wake up to make my train, \\p500 after all I can't be late to work \\p500 . \\p500 . \\p500 .",
          "Oh God, Its 6:00 already! \\p500 Is my alarm clock broken? \\p500 What am I supposed to say to the chief clerk?",
          "Surely he can't fire me for one slip up, \\p500 can he?",
          "It matters not, \\p500 if I get out of bed now I can make the 7:00 train if I hurry.",
          "I might be able to get a less severe punishment if I get out of bed now and rush to work."],
         [("Get out of bed", 1, "hurt1"), ("Stay in bed", 2, None)], bed_scene_image],
        # Get out of bed option
        [["\\r80 \\p1000 My body \\p500 . \\p500 . \\p500 . \\p500 it feels like its been torn apart just from trying to move.",
          "\\r80 My legs won't obey me, \\p500 my body is too wide.",
          "\\r50 I won't be able to get out of bed in this state, \\p500 I wish I could just continue to sleep.",
          "But I can't just lay down, \\p500 I have to get to work.",
          "These pains throughout my body are no excuse to stay in bed all day, \\p500 my family is probably worried sick."],
         [("Continue trying", 5, "hurt3"), ("Stay in bed", 3, None)], bed_scene_image],
        # Stay in bed option
        [["No, \\p500 I have to get to work, \\p500 even if I have these \\i strange aches \\i all across my body.",
          ". \\p500 . \\p500 .",
          "My morning delusions are no excuse to lay in bed all day, \\p500 I better get up.",
          "I'll miss the 7:00 train if I continue on like this!",
          "I can't stay in bed, I \\i have \\i to get to work. \\p500 My family is probably worried sick."],
         [("Get out of bed", 1, "hurt"), ("Stay in bed", 3, None)], bed_scene_image],
        # Continue stay in bed option
        [[". \\p500 . \\p500 .",
          "\\i \\c(100,100,200) \\o \"Gregor dear, \\p500 aren't you late to work? \\p500 You \\i need \\i to get out of bed!\"",
          "Oh! \\p500 My sweet mother, \\p500 always so kind and caring.",
          "\\i \"Yes mother, \\p500 I'm getting up right now.\"",
          ". \\p500 . \\p500 .",
          "\\i \\c(200,40,40) \\o \"Gregor! \\p500 Gregor! \\p500 Whats the matter with you?\"",
          "\\i \\c(200,200,30) \\o \"Gregor, are you hurt? \\p500 Do you need help?\"",
          "My entire family is worried, \\p500 they must be wondering what will happen if I lose my job \\p500 . \\p500 . \\p500 . \\p500 I don't even want to think about it.",
          "They probably would've come in to check on me by now and seen my condition if I hadn't left my door locked!",
          "I really have to get up now, \\p500 or my family will be disappointed.",
          "Oh god, \\p500 what do I do?"],
         [("Get out of bed", 10, "doorbellhurt"), ("Stay in bed", 4, "doorbell")], bed_scene_image],
        # Abandon family option
        [["Oh no, \\p500 the company must have sent someone to check on me!",
          "Please don't let them come in here to see me in this state!",
          "\\c(150,150,150) \\i \\o \"Where's Gregor?\"",
          "Wait, \\p500 that can't be, \\p500 the chief clerk himself came to see why I haven't come to work!",
          "Does the company think all their workers are just scoundrels?",
          "Do they not trust us even one bit?",
          "It doesn't matter, I have to calm the chief clerk if I want to keep my job.",
          "What will become of me if I am fired? \\p500 What would happen to my family?",
          "My family, \\p500 the company, \\p500 everyone is depending on me. \\p500 \\r50 I can't lose my job, \\p500 I simply \\i can't."],
         [("Talk to the chief clerk", 9, None), ("Abandon your family", 9, None)], bed_scene_image],
        # Continue trying option
        [["\\r80 I think I am making progress \\p500 . \\p500 . \\p500 . \\p500 but my body feels like its falling apart.",
          "I'll have to hurry to make even the 8:00 train once I manage to get out.",
          "\\i \\c(100,100,200) \\o \"Gregor dear, \\p500 aren't you late to work? \\p500 You \\i need \\i to get out of bed!\"",
          "Oh! \\p500 My sweet mother, \\p500 always so kind and caring.",
          "\\i \"Yes mother, \\p500 I'm getting up right now.\"",
          ". \\p500 . \\p500 .",
          "\\i \\c(200,40,40) \\o \"Gregor! \\p500 Gregor! \\p500 Whats the matter with you?\"",
          "\\i \\c(200,200,30) \\o \"Gregor, are you hurt? \\p500 Do you need help?\"",
          "My entire family is asking for me, I'd better hurry out and assure to them that I'm okay."],
         [("Make a final push", 6, "fall"), ("Stay in bed", 4, "doorbell")], bed_scene_image],
        # Final push to get out of bed option
        [["Oh no, \\p500 that must be someone from the office here to check on me.",
          "I don't have time to worry about the damage to my strange body, \\p500 I better greet them if I want to keep my job.",
          "\\c(150,150,150) \\i \\o \"Where's Gregor?\"",
          "Wait, \\p500 that can't be, \\p500 the chief clerk himself came to see why I haven't come to work!",
          "Does the company think all their workers are just scoundrels?",
          "Do they not trust us even one bit?",
          "It doesn't matter, I've already gotten this far, I better open the door.",
          "What will become of me if I am fired? \\p500 What would happen to my family?",
          "My family, \\p500 the company, \\p500 everyone is depending on me. \\p500 \\r50 I can't lose my job, \\p500 I simply \\i can't."],
         [("Open the door", 7, None), ("Cower", 8, None)], door_scene_image],
        # Open the door option
        [["I have to go grab the key.",
          "My arms won't exactly do to pick it up, \\p500 I'll have to use the pincers that are where my mouth used to be.",
          "\\i \\c(100,100,200) \\o \"Look! \\p500 Look! \\p500 He's opening the door!\"",
          "It feels like the key is contorting my pincers, but I have to open this door.",
          "\\i \\r50 \"Chief clerk sir, \\p500 I'll head straight to the office.\"",
          "\\i \\r50 \"I'll make sure to never be late again.\"",
          "\\c(150,150,150) \\i \\o \"Wh- \\p500 Whats \\i that? \\i \\p500 And \\r80 why is it making clicking noises?\"",
          "\\i \\c(100,100,200) \\o \"That's not Gregor! \\p500 What did it do to our Gregor?\"",
          "\\c(150,150,150) \\i \\o \"I have to go tell the company!\"",
          "\\i \\c(200,40,40) \\o \"Get back in the room! \\p500 Do you realize what you've done to us?\"",
          "I couldn't even convince the chief clerk to let me keep my job.",
          "My family was depending on me, \\p500 and I failed.",
          "I'm useless.",
          "Completely useless to my family now.",
          "\\r80 There is no point anymore.",
          "End"],
         [("End", 0, None)], door_scene_image],
        # Cower option
        [["I- \\p500 I can't face the chief clerk.",
          "\\r50 He'll just fire me, \\p500 and I'll be useless.",
          "\\c(150,150,150) \\i \\o \"Gregor! \\p500 Gregor! \\p500 I know your in there!\"",
          "\\i \\c(200,40,40) \\o \"Gregor! \\p500 You need to come out!\"",
          "Well, \\p500 I guess I already am useless, \\p500 hiding behind this door.",
          "\\r80 There is no point anymore.",
          "End"],
         [("End", 0, None)], door_scene_image],
        # Talk to chief clerk option
        [["\\i \"Chief clerk sir, \\p500 I'm sorry I missed the early train today.\"",
          "\\i \"I'll make sure it never happens again, \\p500 and I'll head into work straight away.\"",
          "\\i \"Would you tell me, \\p500 will you be letting me go?\"",
          "\\p500 . \\p500 . \\p500 .",
          "\\c(150,150,150) \\i \\o \"What are those clicking noises? \\p500 Is Gregor trying to make a mockery of us?\"",
          "\\i \\c(100,100,200) \\o \"He must not be well!\"",
          "I can't even communicate with them anymore it seems.",
          "Not that it matters anyway, \\p500 I've just stayed in bed all morning, \\p500 not even trying to get out and keep my job.",
          "I'm useless",
          "\\r80 There is no point anymore.",
          "End"],
         [("End", 0, None)], bed_scene_image],
        # Get out of bed late option
        [["It feels like my bodies been torn apart from trying to move, \\p500 and to make things worse, \\p500 there's someone at the door.",
          "It must be someone from the office coming to check on why I haven't come to work.",
          "My body is too wide and abnormal to get out of bed right now, \\p500 I'll have to talk them from my bed.",
          "\\c(150,150,150) \\i \\o \"Where's Gregor?\"",
          "Wait, \\p500 that can't be, \\p500 the chief clerk himself came to see why I haven't come to work!",
          "Does the company think all their workers are just scoundrels?",
          "Do they not trust us even one bit?",
          "It doesn't matter, I have to calm the chief clerk if I want to keep my job.",
          "What will become of me if I am fired? \\p500 What would happen to my family?",
          "My family, \\p500 the company, \\p500 everyone is depending on me. \\p500 \\r50 I can't lose my job, \\p500 I simply \\i can't."],
         [("Talk to the chief clerk", 9, None), ("Abandon your family", 9, None)], bed_scene_image]
    ]

    option_1.set_text(scenes[0][1][0][0])
    option_2.set_text(scenes[0][1][1][0])
    current_scene = scene.Scene(scenes[0][0], text_box, scenes[0][2], options)
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
            elif current_cutscene == "end":
                brightness_screen.set_alpha(min(50 * cutscene_time, 255))
                current_scene.load(screen)
                screen.blit(brightness_screen, (0, 0))
                if cutscene_time > 8:
                    pygame.quit()
                    sys.exit()
            elif current_cutscene == "glitch":
                current_scene.load(screen)
                if not glitch_played:
                    glitch_sound.play()
                    glitch_played = True

                if cutscene_time < 0.35:
                    screen.blit(glitch_overlay, overlay_location)
                else:
                    current_cutscene = None
                    cutscene_start_time = None
                    glitch_played = False
            elif current_cutscene[:4] == "hurt":
                if not set_hurt_times:
                    hurt_times = int(current_cutscene[4:])
                    set_hurt_times = True
                current_scene.load(screen)
                screen.blit(hurt_overlay, overlay_location)
                if not hurt_played:
                    hurt_sound.play()
                    hurt_played = True
                if cutscene_time < 0.6:
                    hurt_overlay.set_alpha((0.6 - cutscene_time) * 400)
                else:
                    if hurt_times == 1:
                        current_cutscene = None
                        cutscene_start_time = None
                        hurt_overlay.set_alpha(255)
                        hurt_played = False
                        set_hurt_times = False
                    else:
                        cutscene_start_time = current_time
                        hurt_played = False
                        hurt_times -= 1
            elif current_cutscene == "doorbell":
                if not set_text:
                    cutscene_text_box.set_text(". \\p500 . \\p500 . \\p500")
                    set_text = True

                screen.blit(bed_scene_image, overlay_location)
                cutscene_text_box.load(screen)

                if not cutscene_text_box.is_done():
                    cutscene_text_box.move(delta_time)
                if 4 < cutscene_time < 7:
                    if not door_bell_played:
                        door_bell_sound.play()
                        door_bell_played = True
                elif cutscene_time > 7:
                    current_cutscene = None
                    cutscene_start_time = None
                    door_bell_played = False
                    set_text = False
            elif current_cutscene == "fall":
                if cutscene_time < 2:
                    screen.fill(black)
                    if not fall_sound_played:
                        fall_sound.play()
                        fall_sound_played = True
                elif cutscene_time < 5:
                    if not set_text:
                        cutscene_text_box.set_text("\\r80 I have to get to the door.")
                        set_text = True
                    cutscene_text_box.load(screen)
                    cutscene_text_box.move(delta_time)
                elif cutscene_time < 8:
                    if not scurry_sound_played:
                        scurry_sound.play()
                        scurry_sound_played = True
                elif cutscene_time < 12:
                    brightness_screen.set_alpha((12 - cutscene_time) * 25 + 155)
                    screen.blit(door_scene_image, overlay_location)
                    screen.blit(brightness_screen, (0, 0))
                elif cutscene_time < 14:
                    if not door_bell_played:
                        door_bell_sound.play()
                        door_scene_image.blit(brightness_screen, (0, 0))
                        door_bell_played = True
                else:
                    current_cutscene = None
                    cutscene_start_time = None
                    scurry_sound_played = False
                    fall_sound_played = False
                    door_bell_played = False
                    set_text = False
            elif current_cutscene == "opendoor":
                screen.fill(black)
                if cutscene_time > 10:
                    current_cutscene = None
                    cutscene_start_time = None
            elif current_cutscene == "closedoor":
                brightness_screen.set_alpha(255 - (cutscene_time * 63))
                screen.blit(door_scene_image, (0, 0))
                screen.blit(brightness_screen, (0, 0))
                if cutscene_time > 4:
                    current_cutscene = None
                    cutscene_start_time = None
            elif current_cutscene == "doorbellhurt":
                current_scene.load(screen)
                if not hurt_played:
                    hurt_sound.play()
                    hurt_played = True
                if cutscene_time < 0.6:
                    hurt_overlay.set_alpha((0.6 - cutscene_time) * 400)
                    screen.blit(hurt_overlay, overlay_location)
                elif cutscene_time < 4:
                    if not door_bell_played:
                        door_bell_sound.play()
                        door_bell_played = True
                else:
                    current_cutscene = None
                    cutscene_start_time = None
                    door_bell_played = False
                    hurt_played = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            continue

        current_scene.load(screen)
        current_scene.move(delta_time)

        # Special cases
        if (scene_num == 4 and current_scene.get_chosen_option() == option_2 or scene_num == 10 and current_scene.get_chosen_option() == option_2) and not glitched:
            option_2.set_text("Talk to the chief clerk")
            current_scene.chosen_option = None
            current_cutscene = "glitch"
            glitched = True
        elif scene_num == 7 and current_scene.current_text == 4 and not door_open_played:
            dark_screen = pygame.Surface(screen_size)
            current_scene.background_img = dark_screen
            current_cutscene = "opendoor"
            door_open_sound.play()
            door_open_played = True
        elif scene_num == 7 and current_scene.current_text == 10 and not door_slam_played:
            current_cutscene = "closedoor"
            current_scene.background_img = door_scene_image
            door_slam_sound.play()
            door_slam_played = True
        elif scene_num == 7 and current_scene.current_text == 15:
            current_cutscene = "end"
        elif scene_num == 8 and current_scene.current_text == 6:
            current_cutscene = "end"
        elif scene_num == 9 and current_scene.current_text == 10:
            current_cutscene = "end"

        if current_scene.at_decision():
            for i in range(len(current_scene.options)):
                if current_scene.get_chosen_option() == current_scene.options[i]:
                    chosen_option_parameters = scenes[scene_num][1][i]
                    set_scene(current_scene, scenes[chosen_option_parameters[1]], options)
                    current_cutscene = chosen_option_parameters[2]
                    scene_num = chosen_option_parameters[1]
                    break

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
