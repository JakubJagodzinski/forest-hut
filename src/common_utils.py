import json
import math
import os
import sys

import pygame


def get_fps_rate(delta_time) -> int:
    if delta_time > 0:
        return int(1.0 / delta_time)
    else:
        return 0


def load_json(file_path: str) -> dict | list:
    with open(file_path, 'rt', encoding='utf-8') as f:
        return json.load(f)


def load_json_from_directory(directory_path: str) -> dict | list:
    data = []
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            with open(os.path.join(directory_path, filename), 'rt', encoding='utf-8') as f:
                data.extend(json.load(f))
    return data


def load_txt(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def quit_game():
    pygame.quit()
    sys.exit()


def normalise_movement_vector(movement_vector) -> [float, float]:
    x, y = movement_vector
    movement_vector_length = float(math.sqrt(x * x + y * y))
    if movement_vector_length > 0:
        movement_vector[0] = x / movement_vector_length
        movement_vector[1] = y / movement_vector_length
    return movement_vector


def normalize_value(value, min_val, max_val, new_min=0, new_max=1):
    return (value - min_val) * ((new_max - new_min) / (max_val - min_val)) + new_min


def manhattan_distance(start_position, target_position):
    return abs(start_position[0] - target_position[0]) + abs(start_position[1] - target_position[1])


def euclidean_distance(start_position, target_position):
    return math.sqrt((start_position[0] - target_position[0]) ** 2 + (start_position[1] - target_position[1]) ** 2)


def adjust_color(color, factor):
    r, g, b = color
    r = min(255, max(0, int(r * factor)))
    g = min(255, max(0, int(g * factor)))
    b = min(255, max(0, int(b * factor)))
    return r, g, b


def remove_filename_extension(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]
