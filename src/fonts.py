import pygame

from src.paths import PATH_FONT_ALICE_IN_WONDERLAND

if not pygame.get_init():
    pygame.init()

FONT_MONOSPACE_COURIER_16 = pygame.font.SysFont('Courier', 16)

FONT_ARIAL_16 = pygame.font.SysFont('Arial', 16)
FONT_ARIAL_18 = pygame.font.SysFont('Arial', 18)
FONT_ARIAL_26 = pygame.font.SysFont('Arial', 26)
FONT_ARIAL_32 = pygame.font.SysFont('Arial', 32)

FONT_ALICE_IN_WONDERLAND_16 = pygame.font.Font(PATH_FONT_ALICE_IN_WONDERLAND, 16)
FONT_ALICE_IN_WONDERLAND_18 = pygame.font.Font(PATH_FONT_ALICE_IN_WONDERLAND, 18)
FONT_ALICE_IN_WONDERLAND_32 = pygame.font.Font(PATH_FONT_ALICE_IN_WONDERLAND, 32)
FONT_ALICE_IN_WONDERLAND_36 = pygame.font.Font(PATH_FONT_ALICE_IN_WONDERLAND, 36)
FONT_ALICE_IN_WONDERLAND_40 = pygame.font.Font(PATH_FONT_ALICE_IN_WONDERLAND, 40)
FONT_ALICE_IN_WONDERLAND_48 = pygame.font.Font(PATH_FONT_ALICE_IN_WONDERLAND, 48)
