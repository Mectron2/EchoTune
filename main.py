import pygame
import json
from datetime import datetime, timedelta
import pygame_shaders
import time
import random
import os
from font_calc import modify_json_lyrics
import pygame_widgets
from pygame_widgets.slider import Slider
from speed import pitch

def parse_time(time_str):
    min, sec = map(int, time_str.split(':'))
    return timedelta(minutes=min, seconds=sec)

def load_lyrics(filename):
    with open(filename, 'r', encoding="utf-8") as file:
        data = json.load(file)
    return data['lyrics']

def matching_percentage(str1, str2):
    if len(str1) != len(str2):
        if len(str1) < len(str2):
            str1 += "#"*(len(str2)-len(str1))
        else:
            str2 += "#"*(len(str1)-len(str2))

    match_count = sum(1 for a, b in zip(str1, str2) if a == b)
    percentage = (match_count / len(str1)) * 100
    return percentage

def average_percentage(percentages):
    if not percentages:
        return 0
    return sum(percentages) / len(percentages)

def get_grade(average):
    if average >= 95:
        return 'SS'
    elif average >= 85:
        return 'S'
    elif average >= 75:
        return 'A'
    elif average >= 65:
        return 'B'
    elif average >= 50:
        return 'C'
    else:
        return 'D'

shaders = True
running = True
start_screen = True

def main(shader):
    pygame.init()
        
    if shader:
        display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.OPENGL)
        display_info = pygame.display.Info()
        screen_width, screen_height = display_info.current_w, display_info.current_h
        shader = pygame_shaders.Shader(pygame_shaders.DEFAULT_VERTEX_SHADER, "fragment.glsl", display)
        radius = 15
        texOffsetX = 1.0 / screen_width
        texOffsetY = 1.0 / screen_height
        bloomIntensity = 0.7
        shader.send("radius", radius)
        shader.send("texOffsetX", texOffsetX)
        shader.send("texOffsetY", texOffsetY)
        shader.send("bloomIntensity", bloomIntensity)
        shader.send("stretchFactorX", 6)
    else:
        display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        display_info = pygame.display.Info()
        screen_width, screen_height = display_info.current_w, display_info.current_h

    pygame.display.set_caption("Echo$Tune")
    slider = Slider(display, screen_width//2-screen_width//8, int(screen_height*0.65), screen_width//4, 20, min=0.5, max=1.5, step=0.1, colour=(50,50,50), handleColour=(200,200,200))

    font = pygame.font.Font("retro_computer_personal_use.ttf", 36)
    current_line = 0
    user_input = ''
    selected = False
    key_backspace_timer = 0
    key_backspace_delay = 100
    last_checked = None
    last_check_half_correct = None
    clock = pygame.time.Clock()
    start_time = datetime.now()
    last_check_time = None
    check_delay = timedelta(seconds=1)
    last_check_correct = False
    correct_percentages = []
    color = (255, 255, 255)
    progress_bar_size = screen_width//2
    progress_bar_height = 10
    initial_progress_bar_size = screen_width//2
    progress_bar_size = initial_progress_bar_size
    progress_bar_color = [255,255,0]
    hint_font = pygame.font.Font("retro_computer_personal_use.ttf", screen_height//75)
    error_font = pygame.font.Font("retro_computer_personal_use.ttf", screen_height//50)
    hint_text = hint_font.render("""K_LEFT/K_RIGHT - scroll maps
    RETURN - confirm choice
    S - turn on/off shaders""", True, (255, 255, 255))
    hint_text_rect = hint_text.get_rect(center=(screen_width//2, screen_height*0.87))
    wait_font = pygame.font.Font("retro_computer_personal_use.ttf", screen_height//45)
    input_text_font = pygame.font.Font("retro_computer_personal_use.ttf", screen_height//45)
    endscreen_font = pygame.font.Font("retro_computer_personal_use.ttf", screen_height//30)

    path = '.\\maps\\'

    directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    if directories == []:
        directories.append("No maps found")

    menu_order = 0

    if shader:
        start_screen_image = pygame.image.load("start_screen.png").convert_alpha()
        start_screen_image = pygame.transform.scale(start_screen_image, (screen_width, screen_height))
        background_image = pygame.image.load("back.png").convert_alpha()
        background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
        background_image_correct = pygame.image.load("back_correct.png").convert_alpha()
        background_image_correct = pygame.transform.scale(background_image_correct, (screen_width, screen_height))
        background_image_half_correct = pygame.image.load("back_half_correct.png").convert_alpha()
        background_image_half_correct = pygame.transform.scale(background_image_half_correct, (screen_width, screen_height))
        background_image_incorrect = pygame.image.load("back_incorrect.png").convert_alpha()
        background_image_incorrect = pygame.transform.scale(background_image_incorrect, (screen_width, screen_height))
        background_overlay = pygame.image.load("back_overlay.png").convert_alpha()
        background_overlay = pygame.transform.scale(background_overlay, (screen_width, screen_height))
        background_overlay_left = pygame.image.load("back_overlay_left.png").convert_alpha()
        background_overlay_left = pygame.transform.scale(background_overlay_left, (screen_width, screen_height))
        background_overlay_right = pygame.image.load("back_overlay_right.png").convert_alpha()
        background_overlay_right = pygame.transform.scale(background_overlay_right, (screen_width, screen_height))
    else:
        start_screen_image = pygame.image.load("start_screen.png")
        start_screen_image = pygame.transform.scale(start_screen_image, (screen_width, screen_height))
        background_image = pygame.image.load("back.png")
        background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
        background_image_correct = pygame.image.load("back_correct.png")
        background_image_correct = pygame.transform.scale(background_image_correct, (screen_width, screen_height))
        background_image_incorrect = pygame.image.load("back_incorrect.png")
        background_image_incorrect = pygame.transform.scale(background_image_incorrect, (screen_width, screen_height))
        background_image_half_correct = pygame.image.load("back_half_correct.png")
        background_image_half_correct = pygame.transform.scale(background_image_half_correct, (screen_width, screen_height))
        background_overlay = pygame.image.load("back_overlay.png").convert_alpha()
        background_overlay = pygame.transform.scale(background_overlay, (screen_width, screen_height))
        background_overlay_left = pygame.image.load("back_overlay_left.png").convert_alpha()
        background_overlay_left = pygame.transform.scale(background_overlay_left, (screen_width, screen_height))
        background_overlay_right = pygame.image.load("back_overlay_right.png").convert_alpha()
        background_overlay_right = pygame.transform.scale(background_overlay_right, (screen_width, screen_height))

    def animate_text_change(current_text, new_text, direction):
        animation_duration = 15 
        for frame in range(animation_duration):
            display.blit(background_image, (0, 0))
            if direction == 'right':
                current_x = int((screen_width / 2) - (frame * (screen_width / animation_duration)))
                new_x = int(screen_width + (screen_width / 2) - (frame * (screen_width / animation_duration)))
            else:
                current_x = int((screen_width / 2) + (frame * (screen_width / animation_duration)))
                new_x = int(-screen_width / 2 + (frame * (screen_width / animation_duration)))

            current_text_rect = current_text.get_rect(center=(current_x, screen_height // 2))
            new_text_rect = new_text.get_rect(center=(new_x, screen_height // 2))

            display.blit(current_text, current_text_rect)
            display.blit(new_text, new_text_rect)
            if direction == 'right':
                display.blit(background_overlay_right, (0,0))
            else:
                display.blit(background_overlay_left, (0,0))
            display.blit(hint_text, hint_text_rect)
            display.blit(speed_text, speed_text_rect)
            pygame_widgets.update(events)

            if shader:
                try:
                    bloomIntensity = random.uniform(0.3, 0.9)
                    shader.send("bloomIntensity", bloomIntensity)
                    shader.render_direct(pygame.Rect(0, 0, screen_width, screen_height))
                except Exception as e:
                    print(e)
                    pygame.quit()

            pygame.display.flip()
            clock.tick(60)

    global running
    global shaders
    global start_screen

    if start_screen:
        display.blit(start_screen_image, (0,0))
        if shader:
            try:
                shader.send("bloomIntensity", 0)
                shader.render_direct(pygame.Rect(0, 0, screen_width, screen_height))
            except Exception as e:
                print(e)
                pygame.quit()
        pygame.display.flip()
        clock.tick(60)
        pygame.time.wait(4000)
        start_screen=False

    while running:
        if not selected:
            events = pygame.event.get()
            start_time = datetime.now()
            text = font.render(f"{directories[menu_order]}", True, (255, 255, 255))
            text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
            display.blit(background_image, (0, 0))
            display.blit(text, text_rect)
            display.blit(background_overlay, (0,0))
            display.blit(hint_text, hint_text_rect)
            speed = round(slider.getValue(), 2)
            speed_text = hint_font.render(f"speed: {speed}", True, (255, 255, 255))
            speed_text_rect = speed_text.get_rect(center=(screen_width//2, screen_height*0.7))
            display.blit(speed_text, speed_text_rect)
            for event in events:
                if event.type == pygame.QUIT:
                    return False, shaders
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        new_menu_order = (menu_order + 1) % len(directories)
                        new_text = font.render(f"{directories[new_menu_order]}", True, (255, 255, 255))
                        animate_text_change(text, new_text, 'right')
                        menu_order = new_menu_order
                        text = new_text
                        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
                    elif event.key == pygame.K_LEFT:
                        new_menu_order = (menu_order - 1) % len(directories)
                        new_text = font.render(f"{directories[new_menu_order]}", True, (255, 255, 255))
                        animate_text_change(text, new_text, 'left')
                        menu_order = new_menu_order
                        text = new_text
                        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
                    elif event.key == pygame.K_RETURN:
                        selected_path_lyrics = f"maps\\{directories[menu_order]}\\lyrics.json"
                        selected_path_music = f"maps\\{directories[menu_order]}\\music.wav"
                        try:
                            if speed != 1:
                                pitch_elapsed_time = pitch(f"maps\\{directories[menu_order]}\\music.wav", f"maps\\{directories[menu_order]}\\pitched.wav", speed)
                                selected_path_music = f"maps\\{directories[menu_order]}\\pitched.wav"
                            else:
                                pitch_elapsed_time = timedelta(seconds=0)
                            elapsed_time = modify_json_lyrics(selected_path_lyrics, speed, screen_width, screen_height)
                            if speed != 1:
                                selected_path_lyrics = f"maps\\{directories[menu_order]}\\lyrics_{speed}.json"
                            lyrics = load_lyrics(selected_path_lyrics)
                            pygame.mixer.init()
                            pygame.mixer.music.load(selected_path_music)
                            pygame.mixer.music.play()
                            pygame.mixer.music.pause()
                            end_time = parse_time(lyrics[-1]['end'])
                            end_time_formated = f"{end_time.seconds//60:02}:{end_time.seconds%60:02}"
                            selected = True
                        except:
                            error_text = error_font.render(f'The map appears to be damaged. Make sure there are files "song.wav" and "lyrics.json" in the path ./maps/{directories[menu_order]}', True, (255, 255, 255))
                            error_text_rect = error_text.get_rect(center=(screen_width//2, screen_height//2))
                            display.fill((0,0,0))
                            display.blit(error_text, error_text_rect)
                            if shader:
                                try:
                                    bloomIntensity = random.uniform(0.3, 0.9)
                                    shader.send("bloomIntensity", bloomIntensity)
                                    shader.render_direct(pygame.Rect(0, 0, screen_width, screen_height))
                                except Exception as e:
                                    print(e)
                                    pygame.quit()
                            
                            pygame.display.flip()
                            clock.tick(60)
                            pygame.time.delay(5000)

                    elif event.key == pygame.K_s:
                        
                        if not shaders:
                            shaders = True
                        else:
                            shaders = False
                        running = False

            pygame_widgets.update(events)

            if shader:
                try:
                    bloomIntensity = random.uniform(0.3, 0.9)
                    shader.send("bloomIntensity", bloomIntensity)
                    shader.render_direct(pygame.Rect(0, 0, screen_width, screen_height))
                except Exception as e:
                    print(e)
                    pygame.quit()
              
            pygame.display.flip()
            clock.tick(60)

        elif selected:
            current_time = (datetime.now() - start_time - elapsed_time - pitch_elapsed_time)
            if current_time < timedelta(seconds=3):
                if current_time > timedelta(seconds=2):
                    display.blit(background_image, (0,0))
                    count_font = pygame.font.Font("retro_computer_personal_use.ttf", screen_height//10)
                    one = count_font.render("ONE", True, (255, 0, 0))
                    one_rect = one.get_rect(center=(screen_width // 2, screen_height // 2))
                    display.blit(one, one_rect)
                elif current_time > timedelta(seconds=1):
                    display.blit(background_image, (0,0))
                    count_font = pygame.font.Font("retro_computer_personal_use.ttf", screen_height//13)
                    two = count_font.render("TWO", True, (255, 255, 0))
                    two_rect = two.get_rect(center=(screen_width // 2, screen_height // 2))
                    display.blit(two, two_rect)
                elif current_time > timedelta(seconds=0):
                    display.blit(background_image, (0,0))
                    count_font = pygame.font.Font("retro_computer_personal_use.ttf", screen_height//15)
                    three = count_font.render("THREE", True, (0, 255, 0))
                    three_rect = three.get_rect(center=(screen_width // 2, screen_height // 2))
                    display.blit(three, three_rect)
                if shader:
                    try:
                        bloomIntensity = random.uniform(0.3, 0.9)
                        shader.send("bloomIntensity", bloomIntensity)
                        shader.render_direct(pygame.Rect(0, 0, screen_width, screen_height))
                    except Exception as e:
                        print(e)
                        pygame.quit()
                
                pygame.display.flip()
                clock.tick(60)
            else:
                current_time = (datetime.now() - start_time - elapsed_time - pitch_elapsed_time - timedelta(seconds=3))
                pygame.mixer.music.unpause()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False, shaders
                    elif event.type == pygame.KEYDOWN:
                        mods = pygame.key.get_mods()
                        if event.key == pygame.K_BACKSPACE:
                            if time.time() * 1000 - key_backspace_timer > key_backspace_delay:
                                user_input = user_input[:-1]
                                key_backspace_timer = time.time() * 1000
                        elif event.unicode.isprintable():
                            if (((user_input).lower()).strip() != (((lyrics[current_line]['line'])).lower()).strip()) and (len(user_input) <= len((lyrics[current_line]['line'].lower()).strip())):
                                if mods & pygame.KMOD_SHIFT:
                                    if event.unicode == " ":
                                        if len(user_input) > 0:
                                            user_input += event.unicode
                                    else:
                                        user_input += event.unicode
                                else:
                                    user_input += event.unicode
                                
                keys = pygame.key.get_pressed()
                if keys[pygame.K_BACKSPACE]:
                    if time.time() * 1000 - key_backspace_timer > key_backspace_delay:
                        user_input = user_input[:-1]
                        key_backspace_timer = time.time() * 1000
                
                #Endscreen

                if current_time >= end_time:
                    percentage = matching_percentage(user_input.lower().strip(), lyrics[current_line]['line'].lower().strip())
                    correct_percentages.append(percentage)
                    pygame.mixer.music.set_volume(0.08)
                    average_correct = average_percentage(correct_percentages)
                    grade = get_grade(average_correct)
                    end_text = endscreen_font.render(f"Your Average: {round((average_correct), 2)}%", True, (255, 255, 255))
                    grade_text = endscreen_font.render(f"Your Grade: {grade}", True, (255, 255, 255))
                    end_text_rect = end_text.get_rect(center=(screen_width // 2, screen_height // 2 - (screen_height // 20)))
                    grade_text_rect = grade_text.get_rect(center=(screen_width // 2, screen_height // 2 + (screen_height // 20)))
                    
                    while current_time < end_time + timedelta(seconds=9):
                        display.fill((0, 0, 0))
                        display.blit(end_text, end_text_rect)
                        display.blit(grade_text, grade_text_rect)
                        
                        current_time = datetime.now() - start_time - elapsed_time
                        
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                return False, shaders
                        
                        if shader:
                            try:
                                bloomIntensity = random.uniform(0.3, 0.9)
                                shader.send("bloomIntensity", bloomIntensity)
                                shader.render_direct(pygame.Rect(0, 0, screen_width, screen_height))
                            except Exception as e:
                                print(e)
                                pygame.quit()
                        
                        pygame.display.flip()
                        clock.tick(60)
                    
                    # Restart after 5 sec
                    font = pygame.font.Font("retro_computer_personal_use.ttf", 36)
                    current_line = 0
                    user_input = ''
                    key_backspace_timer = 0
                    key_backspace_delay = 100
                    last_checked = None
                    last_check_half_correct = None
                    clock = pygame.time.Clock()
                    start_time = datetime.now()
                    last_check_time = None
                    check_delay = timedelta(seconds=1)
                    last_check_correct = False
                    correct_percentages = []
                    color = (255, 255, 255)
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.unload()
                    selected = False
                    progress_bar_size = initial_progress_bar_size
                    continue


                if last_check_time and datetime.now() - last_check_time <= check_delay:
                    if last_check_correct:
                        color = (0,0,0)  
                        display.blit(background_image_correct, (0, 0))
                    elif last_check_half_correct:
                        color = (0,0,0)
                        display.blit(background_image_half_correct, (0, 0))
                    else:
                        color = (0,0,0)  
                        display.blit(background_image_incorrect, (0, 0))
                else:
                    color = (255,255,255)  
                    display.blit(background_image, (0, 0))

                total_seconds = int(current_time.total_seconds())
                minutes = total_seconds // 60
                seconds = total_seconds % 60
                time_font = pygame.font.Font("retro_computer_personal_use.ttf", 15)
                time_text = time_font.render(f'{minutes:02}:{seconds:02}', True, (255, 255, 255))
                time_text_rect = time_text.get_rect(center=(screen_width * 0.697, screen_height * 0.06))
                display.blit(time_text, time_text_rect)
                audio_length_text = time_font.render(f'/ {end_time_formated}', True, (255, 255, 255))
                audio_length_text_rect = audio_length_text.get_rect(center=(screen_width * 0.74, screen_height * 0.06))
                correct_font = pygame.font.Font("retro_computer_personal_use.ttf", 15)
                average_correct = average_percentage(correct_percentages)
                correct_text = correct_font.render(f"Avg: {average_correct:.2f}%", True, (0, 255, 0))
                correct_text_rect = correct_text.get_rect(center=(screen_width * 0.27, screen_height * 0.06))
                display.blit(correct_text, correct_text_rect)
                display.blit(audio_length_text, audio_length_text_rect)

                if current_line < len(lyrics):
                    start_time_lyrics = parse_time(lyrics[current_line]['start'])
                    end_time_lyrics = parse_time(lyrics[current_line]['end'])

                    if start_time_lyrics <= current_time <= end_time_lyrics:
                        font = pygame.font.Font("retro_computer_personal_use.ttf", lyrics[current_line]['font_size'])
                        text = font.render(lyrics[current_line]['line'], True, color)
                        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
                        display.blit(text, text_rect)
                        if ((user_input).lower()).strip() != (((lyrics[current_line]['line'])).lower()).strip():
                            user_input_text = input_text_font.render(f">_ {user_input}", True, color)
                        else:
                            user_input_text = input_text_font.render(f">_ {user_input}", True, (0,255,0))
                        user_input_text_rect = user_input_text.get_rect(center=(screen_width // 2, screen_height*0.63))
                        display.blit(user_input_text, user_input_text_rect)
                        total_time_lyrics = (end_time_lyrics - start_time_lyrics).total_seconds()

                        total_frames = total_time_lyrics * int(clock.get_fps())

                        progress_bar_scaler = initial_progress_bar_size / total_frames  
                        if progress_bar_size > 0:
                            progress_bar_size -= progress_bar_scaler
                        else:
                            progress_bar_size = 0

                        progress_bar_x = (screen_width - progress_bar_size) // 2
                        progress_bar = pygame.Rect(progress_bar_x, screen_height // 2 + screen_height // 4, progress_bar_size, progress_bar_height)
                        pygame.draw.rect(display, progress_bar_color, progress_bar)
                        
                    elif current_time >= end_time_lyrics:
                        percentage = matching_percentage(user_input.lower().strip(), lyrics[current_line]['line'].lower().strip())
                        correct_percentages.append(percentage)
                        progress_bar_size = screen_width // 2
                        if percentage == 100:
                            display.blit(correct_text, correct_text_rect)
                            display.blit(background_image_correct, (0, 0))
                            text = font.render(lyrics[current_line]['line'], True, color)
                            display.blit(text, text_rect)
                            display.blit(time_text, time_text_rect)
                            display.blit(audio_length_text, audio_length_text_rect)
                            last_check_half_correct = False
                            last_check_correct = True
                        elif 100 > percentage > 50:
                            display.blit(correct_text, correct_text_rect)
                            display.blit(background_image_half_correct, (0, 0))
                            text = font.render(lyrics[current_line]['line'], True, color)
                            display.blit(text, text_rect)
                            display.blit(time_text, time_text_rect)
                            display.blit(audio_length_text, audio_length_text_rect)
                            last_check_correct = False
                            last_check_half_correct = True
                        else:
                            display.blit(correct_text, correct_text_rect)
                            text = font.render(lyrics[current_line]['line'], True, color)
                            display.blit(background_image_incorrect, (0, 0))
                            display.blit(text, text_rect)
                            display.blit(time_text, time_text_rect)
                            display.blit(audio_length_text, audio_length_text_rect)
                            last_check_half_correct = False
                            last_check_correct = False
                        if last_checked != current_line:
                            last_checked = current_line
                            last_check_time = datetime.now()
                            user_input = ''
                            current_line += 1
                            display.blit(correct_text, correct_text_rect)
                    else:
                        user_input = ''
                        user_input_text = wait_font.render("WAIT", True, color)
                        user_input_text_rect = user_input_text.get_rect(center=(screen_width // 2, screen_height*0.63))
                        display.blit(user_input_text, user_input_text_rect)
                        display.blit(correct_text, correct_text_rect)
                
                if shader:
                    try:
                        bloomIntensity = random.uniform(0.3, 0.9)
                        shader.send("bloomIntensity", bloomIntensity)
                        shader.render_direct(pygame.Rect(0, 0, screen_width, screen_height))
                    except Exception as e:
                        print(e)
                        pygame.quit()
                
                pygame.display.flip()
                clock.tick(60)
    
    if shader:
        try:
            shader.render_direct(pygame.Rect(0, 0, screen_width, screen_height))
        except Exception as e:
            print(e)
            pygame.quit()

    pygame.display.flip()

    pygame.quit()
    return True, shaders

while running:    
    running, shaders = main(shaders)



