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

    clock_image = pygame.image.load("./Images/Scenes/Clock.png")
    clock_position = ((screen_width - clock_image.get_width()) / 2, (screen_height - clock_image.get_height()) / 2)

    brightness_screen = pygame.Surface(screen_size)
    brightness_screen.fill(black)

    effective_screen_size = bed_scene_image.get_size()

    text_box_img = pygame.image.load("./Images/Text/Text Box.png")
    text_box_img = pygame.transform.scale(text_box_img, (bed_scene_image.get_width() - 300,
                                                 text_box_img.get_height() * ((bed_scene_image.get_width() - 600) / text_box_img.get_width())))
    text_box = text.Text("text", text_box_img, ((screen_width - text_box_img.get_width()) / 2, effective_screen_size[1] - text_box_img.get_height() - 30))

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

    # How to format a scene, [texts], [(option 1 text, scene it goes to, cutscene to trigger), (option 2 text, scene it goes to, cutscene to trigger)], background_img
    # scenes = [
    #     [["\\r50 Oh can't I sleep a little longer? \\p1000 I wish I could just forget my job and sleep through this dreary weather.", "\\r50 But I must wake up to make my train, \\p500 after all I can't be late \\p500 . \\p500 . \\p500 . \\p1500 \\r30 Oh God, Its 6:00 already!", "Is my alarm clock broken? What am I supposed to say to the chief clerk?", "Surely he can't fire me for one slip up can he?"], [("Get out of bed", 0, None), ("Stay in bed", 0, None)], bed_scene_image]
    # ]
    # scenes = [
    #     [["\\r50 What is happening to me? \\p1000 My body, it feels strange, \\p500 heavy, \\p500 \\r30 monstrous.",
    #       "\\r50 I can barely move my legs, \\p1000 but they aren't legs anymore, \\c(200,0,0) are they?",
    #       "\\r50 Something's crawling beneath my skin, \\p500 twisting, \\p500 mutating \\p1000 . \\p500 . \\p500 .",
    #       "\\r30 \\c(200,0,0) Oh no, \\p500 I can see them \\p1000 \\r50 my hands \\p1000 they've become \\p1000 claws!",
    #       "The room is spinning, but \\r30 I must stay calm. \\p500 No one can know \\p1000 what I've turned into."],
    #      [("Look into the mirror", 1, None), ("Hide under the bed", 2, None)], bed_scene_image],
    #
    #     [["\\r50 \\c(255,255,255) \\p500 Slowly, you turn toward the mirror.",
    #       "\\p1000 Your reflection— \\r30 \\c(200,0,0) it isn't human \\p500 anymore.",
    #       "The thing staring back at you \\r50 has too many legs, \\p500 too many eyes.",
    #       "\\r30 Your face... \\p500 Where is your face?",
    #       "\\r50 \\p500 It’s replaced by a writhing \\c(200,0,0) mass of insects.",
    #       "Your mind screams, but no sound leaves your body."],
    #      [("Shatter the mirror", 3, None), ("Turn away", 4, None)], bed_scene_image],
    #
    #     [["\\r50 \\c(200,0,0) You crawl beneath the bed.",
    #       "\\r50 The shadows envelop you, and \\p500 you hear something \\r30 breathing beside you.",
    #       "\\r50 It sounds like \\p500 \\c(255,255,255) it's coming \\p500 from inside your own head.",
    #       "\\p1000 Is there something there \\r30 waiting \\p500 for you in the dark?",
    #       "\\r50 \\p500 Or \\p500 is it \\r30 you? \\c(200,0,0)"],
    #      [("Stay hidden", 5, None), ("Emerge slowly", 6, None)], bed_scene_image],
    #
    #     [["\\r50 \\c(255,0,0) The glass shatters \\p1000 into thousands of pieces.",
    #       "\\r50 Your reflection splinters into every shard, \\p1000 each twisted version of you \\r30 screaming silently.",
    #       "But they all show one thing: \\p500 \\c(255,0,0) your monstrous truth.",
    #       "This can’t be real, \\p500 you tell yourself.",
    #       "\\p1000 But it is."],
    #      [("Run from the room", 7, None), ("Collapse in shock", 8, None)], bed_scene_image],
    #
    #     [["\\r50 You turn away from the mirror \\p1000 as if denying what you saw \\p500 could make it untrue.",
    #       "\\r30 But you know it's there, \\p1000 lurking behind your reflection.",
    #       "\\r50 And worse, \\p500 you know it’s also inside you."],
    #      [("Run from the room", 7, None), ("Hide under the bed", 2, None)], bed_scene_image],
    #
    #     [["\\r50 You stay perfectly still under the bed.",
    #       "Your breathing slows, \\p500 matching the low growling \\p500 just inches away from your face.",
    #       "\\r30 Whatever it is, \\p500 it's close \\p500 and it knows you're here."],
    #      [("Remain silent", 5, None), ("Crawl out", 6, None)], bed_scene_image],
    #
    #     [["\\r50 \\c(255,255,255) Slowly, you crawl out from under the bed.",
    #       "\\p1000 The room is unnaturally quiet, \\p500 the air heavy with a presence you can’t explain.",
    #       "\\r30 Suddenly, \\p500 a soft clicking noise starts \\p500 behind you.",
    #       "\\r50 You turn to see \\p500 \\c(200,0,0) it’s coming closer."],
    #      [("Run", 7, None), ("Confront it", 9, None)], bed_scene_image],
    #
    #     [["\\r50 You burst out of the room, \\p1000 your twisted body barely fitting through the doorframe.",
    #       "\\p500 The walls seem to pulse as you run, \\p500 as though they too are \\c(255,0,0) alive.",
    #       "\\r30 But where are you running to? \\p1000 There’s no escape from this... from yourself."],
    #      [("Keep running", 10, None), ("Collapse", 8, None)], bed_scene_image],
    #
    #     [["\\r50 \\p1000 You collapse to the floor, \\p500 your body twitching violently.",
    #       "\\r30 The room spins, \\p500 your mind unravels.",
    #       "\\r50 What have you become?"],
    #      [("Surrender", 11, None)], bed_scene_image],
    #
    #     [["\\r50 \\c(255,0,0) You stand your ground.",
    #       "The thing crawling toward you from the darkness is \\r30 unspeakable, \\p500 all limbs and eyes and teeth.",
    #       "\\r50 But as it approaches, \\p1000 you feel a connection.",
    #       "\\r30 This is you."],
    #      [("Accept it", 12, None), ("Fight it", 12, None)], bed_scene_image],
    #
    #     [["\\r50 You keep running, \\p1000 but the corridors twist \\p500 and turn endlessly.",
    #       "\\r30 You’ll never outrun \\p500 what's inside you."],
    #      [("Surrender", 11, None)], bed_scene_image],
    #
    #     [["\\r50 \\p1000 You surrender to the transformation, \\p500 letting it consume you.",
    #       "\\r30 The pain vanishes, \\p500 and you feel nothing \\p1000 at all."],
    #      [("End", 0, "end")], bed_scene_image],
    #
    #     [["\\r50 You fight the creature, \\p1000 but your limbs are weak \\p500 and uncoordinated.",
    #       "\\r30 You can’t win \\p1000 against \\p500 \\c(200,0,0) yourself."],
    #      [("Surrender", 11, None)], bed_scene_image]
    # ]

    scenes = [
        [["\\r50 It's so early... \\p500 and yet my body feels \\r30 so heavy.",
          "\\r50 I can't move like I used to, \\p500 but that doesn't matter.",
          "\\r30 What matters is I'm late. \\p500 I'm \\c(255,0,0) so late for work.",
          "I can’t let my family down, \\p1000 \\c(255,255,255) not again. \\p1000 They need me."],
         [("Get out of bed", 1, None), ("Stay in bed", 2, None)], bed_scene_image],

        [["\\r50 \\p1000 With great effort, you swing \\r30 one leg \\p1000 out of bed.",
          "But \\p500 \\r30 it's not a leg. \\r50 It's \\p500 something else. \\c(255,0,0)",
          "\\r50 Does it even matter? \\p1000 You must get to work.",
          "\\r30 Your family is counting on you."],
         [("Crawl to the door", 3, None), ("Call for help", 4, None)], bed_scene_image],

        [["\\r50 You sink back into bed. \\p1000 The warmth is \\r30 soothing, \\p500 comforting.",
          "\\r50 But \\r30 the voice in your head \\r50 whispers: \\p500 \\c(255,0,0) 'You have failed.'",
          "\\r50 Failed your family. \\p500 Failed your father.",
          "\\r30 \\p1000 You can still hear his voice: \\c(255,255,255) 'Pathetic.'",
          "The options \\r30 echo in your mind."],
         [("Get out of bed", 1, None), ("Abandon your family", 5, None)], bed_scene_image],

        [["\\r50 You crawl across the floor, \\p1000 your new legs clacking against the wood.",
          "\\r30 You feel the weight of your own body, \\p500 \\r50 the grotesque form you’ve become, \\p500 but work, \\r30 work is all that matters.",
          "But when you reach the door, \\r30 you hear \\p1000 \\c(200,0,0) his footsteps \\p1000 outside.",
          "\\r50 Your father is pacing \\p500 back and forth.",
          "\\r30 \\c(255,255,255) What will he do if he sees you?"],
         [("Open the door", 6, None), ("Hide under the bed", 7, None)], bed_scene_image],

        [["\\r50 You call out, \\p1000 but the words don’t come \\p1000 as words anymore.",
          "\\r30 Instead, they emerge as \\p500 \\c(255,0,0) clicks, \\p500 hisses.",
          "\\r50 A language no one understands.",
          "\\r30 From the other side of the door, \\p500 you hear \\c(255,255,255) your father’s voice \\p1000 low, \\r30 dangerous:",
          "\\r50 'What \\p500 \\r30 is \\p500 that?'",
          "\\p1000 You cannot let him see you."],
         [("Hide", 7, None), ("Try again", 4, None)], bed_scene_image],

        [["\\r50 \\p500 Abandon them? \\p1000 Could you really? \\r30 You could \\p500 walk away now.",
          "\\r50 Just let them fend for themselves \\r30 and leave this... this nightmare behind.",
          "\\r50 But where would you go?",
          "\\r30 And \\p500 would they even care? \\r50 Would \\p500 \\c(255,255,255) he?",
          "The thought hangs over you, \\r30 like his presence always has."],
         [("Get out of bed", 1, None), ("Walk out forever", 8, None)], bed_scene_image],

        [["\\r50 You open the door, \\p1000 bracing yourself.",
          "Your father stands there, \\r30 towering over you, \\p500 his gaze cold and \\r30 disgusted.",
          "\\r50 You feel \\c(255,255,255) smaller \\p500 than you've ever felt before.",
          "\\r30 'You’re worthless,' \\p500 his voice cuts through you.",
          "\\r50 His hand clenches into a fist. \\p1000 What will he do to you now?"],
         [("Cower", 10, None), ("Stand your ground", 9, None)], bed_scene_image],

        [[
             "\\r50 You scuttle beneath the bed, \\p1000 as your father's heavy footsteps \\r30 shake the floor above you.",
             "\\r50 You can hear his breathing, \\p1000 harsh, \\p500 impatient.",
             "\\r30 Will he find you?",
             "\\r50 He always finds you."],
         [("Stay hidden", 11, None), ("Emerge", 12, None)], bed_scene_image],

        [["\\r50 \\p1000 You leave the room, \\p500 not looking back.",
          "\\r30 It’s easier this way. \\p1000 Isn’t it?",
          "But \\p1000 \\c(255,0,0) the guilt \\p1000 follows you, \\r30 whispers at the edge of your mind.",
          "\\r50 What will become of them \\p1000 \\r30 without you?"],
         [("Keep walking", 13, None), ("Go back", 14, None)], bed_scene_image],

        [["\\r50 You stand your ground \\p1000 despite the fear pulsing through you.",
          "\\r30 He looks at you \\p1000 like you're \\r50 nothing.",
          "\\r30 'What have you become?' \\p500 he sneers.",
          "\\r50 His voice shakes your very being."],
         [("Collapse", 9, None), ("Leave", 8, None)], bed_scene_image],

        [["\\r50 Your father’s anger \\p1000 is a storm, \\p500 but you cower beneath it.",
          "\\r30 You’ve been here before, \\p500 in his shadow, \\r30 and you’ll be here again.",
          "\\r50 But this time, \\p500 you’re \\c(255,0,0) not human \\p1000 anymore."],
         [("Escape", 8, None), ("Stay", 15, None)], bed_scene_image],

        [["\\r50 You stay perfectly still.",
          "His breathing \\r30 slows. \\p1000 You hear him walk away, \\p500 but the dread remains.",
          "\\r50 \\c(255,0,0) He’ll never stop watching you."],
         [("Get out of bed", 1, None), ("Abandon your family", 5, None)], bed_scene_image],

        [["\\r50 You emerge from the shadows, \\p500 but the room is \\r30 empty.",
          "\\r50 He’s gone, \\p500 but \\r30 the fear lingers.",
          "You wonder \\p500 if you'll ever be \\r30 free of him."],
         [("Leave", 8, None)], bed_scene_image],

        [["\\r50 You walk down the hallway, \\p1000 further and further away.",
          "\\r30 But the further you go, \\p500 the more you feel \\r30 \\c(255,0,0) lost.",
          "\\r50 Will you ever truly escape?"],
         [("End", 0, "end")], bed_scene_image],

        [["\\r50 You turn back.",
          "The weight of the house \\r30 presses down on you, \\p500 heavier than before.",
          "You will never leave.",
          "\\r50 \\c(255,255,255) This is your home now."],
         [("Get out of bed", 1, None)], bed_scene_image],

        [["\\r50 You stay in the room, \\p1000 shrinking beneath your father’s presence.",
          "\\r30 You’ve always been nothing \\r50 to him.",
          "You wonder, \\r30 if you ever \\p500 existed at all."],
         [("End", 0, "end")], bed_scene_image]
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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            continue

        current_scene.load(screen)
        current_scene.move(delta_time)

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
