import pygame


def extract_frames_from_spritesheet(spritesheet, draw_size):
    frames = []
    frame_size = spritesheet.get_height()
    frames_quantity = spritesheet.get_width() // frame_size
    for frame_nr in range(frames_quantity):
        frame = spritesheet.subsurface(pygame.Rect(frame_nr * frame_size, 0, frame_size, frame_size))
        frame = pygame.transform.scale(frame, (draw_size, draw_size))
        frames.append(frame)
    return frames
