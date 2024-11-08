import json
import pygame
import time
from datetime import timedelta

def adjust_font_size(text, screen_width, screen_height):
    max_width = screen_width//5
    max_height = screen_height//4
    pygame.font.init()
    font_size = screen_height//9
    font = pygame.font.Font(None, font_size)
    text_size = font.size(text)
    
    while text_size[0] > max_width or text_size[1] > max_height:
        font_size -= 1
        font = pygame.font.Font(None, font_size)
        text_size = font.size(text)

    return font_size

def convert_time_to_seconds(time_str):
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds

def convert_seconds_to_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"

def modify_json_lyrics(filename, speed, screen_width, screen_height):
    start = time.time()
    with open(filename, 'r', encoding="utf-8") as file:
        data = json.load(file)

    for lyric in data['lyrics']:
        font_size = adjust_font_size(lyric['line'], screen_width, screen_height)
        lyric['font_size'] = font_size

        start_time_seconds = convert_time_to_seconds(lyric['start']) / speed
        end_time_seconds = convert_time_to_seconds(lyric['end']) / speed
        lyric['start'] = convert_seconds_to_time(int(start_time_seconds))
        lyric['end'] = convert_seconds_to_time(int(end_time_seconds))

    if speed != 1:
        new_filename = filename.replace('lyrics.json', f'lyrics_{speed}.json')
    else:
        new_filename = filename

    with open(new_filename, 'w', encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    end = time.time()
    return timedelta(seconds=end - start)
