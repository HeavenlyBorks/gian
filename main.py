import pygame
import requests
import time
import shutil
import math

pygame.init()
s_width = 1600
s_height = 900
screen = pygame.display.set_mode((s_width, s_height))
clock = pygame.time.Clock()

big = pygame.font.SysFont("Manjari", 80)
small = pygame.font.SysFont("Manjari", 30)
blanks_text = ""
type_text = [
    "greeting",
    "adjective to describe a person",
    "noun",
    "noun, plural",
    "verb that two people can do, ending in -ing",
    "verb that two people can do, ending in -ing",
    "adjective to describe an activity",
    "verb",
    "name of some famous group",
    "noun, plural",
    "random fun fact",
    "verb",
    "body part",
    "verb",
    "project two people can work on, plural",
    "sign off phrase",
    "noun",
    "adjective",
]
blanks_storage = []
i = 0

replaceable_text = "{}, {} Giancarlo Beritella. How’s the {}? How are the {}? I feel like it’s been ages since we {} at CMCB. I really enjoy {} with you, I feel like it is always very {}. We could {} about anything from {} to {} to how {}. Sometimes I just want to {} your {} and {} at what’s going on in there. We should work on more {} together. {}.\n- Christian, with some help from his ARTV 101 class\nP.S. I've never met anyone with the same {} as you. I think that's pretty {}."
final_text = ""

r = 0
g = 0
b = 0
g_timer = 1
b_timer = 2
r_up = True
g_up = True
b_up = True


def rgb():
    global r, g, b, g_timer, b_timer, r_up, g_up, b_up
    if r_up and r == 255:
        r_up = False
    if not r_up and r == 0:
        r_up = True
    if g_up and g == 255:
        g_up = False
    if not g_up and g == 0:
        g_up = True
    if b_up and b == 255:
        b_up = False
    if not b_up and b == 0:
        b_up = True
    if r_up:
        r += 1
    else:
        r -= 1
    if g_timer:
        g_timer -= 1
    else:
        if g_up:
            g += 1
        else:
            g -= 1
        g_timer = 1
    if b_timer:
        b_timer -= 1
    else:
        if b_up:
            b += 1
        else:
            b -= 1
        b_timer = 2


backspace = False
backspace_start = None
backspace_rapid = None

running = True
generating = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # check backspace
            if event.key == pygame.K_BACKSPACE and blanks_text:
                blanks_text = blanks_text[:-1]
                backspace = True
                backspace_start = time.time()
            if event.key == pygame.K_RETURN and blanks_text:
                blanks_storage.append(blanks_text)
                blanks_text = ""
                i += 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE:
                backspace = False
                backspace_start = None
        if event.type == pygame.TEXTINPUT:
            blanks_text += event.text

    if backspace and time.time() - backspace_start > 0.5:
        if backspace_rapid and time.time() - backspace_rapid > 0.05:
            blanks_text = blanks_text[:-1]
            backspace_rapid = time.time()
        elif not backspace_rapid:
            backspace_rapid = time.time()

    rgb()
    screen.fill(pygame.Color(r, g, b))

    if i < len(type_text):
        blanks = pygame.font.Font.render(big, blanks_text, False, (255, 255, 255))
        blanks_r = blanks.get_rect()
        blanks_r.centerx = s_width // 2
        blanks_r.centery = s_height // 2
        word_type = pygame.font.Font.render(small, type_text[i], False, (255, 255, 255))
        type_r = word_type.get_rect()
        type_r.top = blanks_r.bottom + 10
        type_r.centerx = blanks_r.centerx
        screen.blit(blanks, blanks_r)
        screen.blit(word_type, type_r)
    else:
        running = False
        generating = True

    pygame.display.flip()
    clock.tick(60)

big = pygame.font.SysFont("Manjari", 50)
final_text = replaceable_text.format(*blanks_storage)
final_split = final_text.split("\n")
to_split = final_split[0].split(" ")
current_line = ""
current_line_preview = ""
lines = []
for word in to_split:
    current_line_preview += word + " "
    if big.size(current_line_preview)[0] < math.ceil(s_width * 0.8):
        current_line += word + " "
    else:
        lines.append(current_line)
        current_line = word + " "
        current_line_preview = word + " "
lines.append(current_line)
small_lines = [final_split[1]]
current_line = ""
current_line_preview = ""
for word in final_split[2].split(" "):
    current_line_preview += word + " "
    if small.size(current_line_preview)[0] < math.ceil(s_width * 0.9):
        current_line += word + " "
    else:
        small_lines.append(current_line)
        current_line = word + " "
        current_line_preview = word + " "
small_lines.append(current_line)
lines_height = 0
for line in lines:
    lines_height += big.size(line)[1] + 10
lines_start = math.floor((s_height / 2) - (lines_height / 2))

while generating:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            generating = False

    rgb()
    screen.fill(pygame.Color(r, g, b))

    curr_lines_height = lines_start

    for line in lines:
        line_render = big.render(line, False, (255, 255, 255))
        line_r = line_render.get_rect()
        line_r.top = curr_lines_height
        line_r.left = math.floor(s_width * 0.1)
        screen.blit(line_render, line_r)
        curr_lines_height += line_r.height + 10

    for line in small_lines:
        line_render = small.render(line, False, (255, 255, 255))
        line_r = line_render.get_rect()
        line_r.top = curr_lines_height
        line_r.right = math.ceil(s_width * 0.9)
        screen.blit(line_render, line_r)
        curr_lines_height += line_r.height + 5

    pygame.display.flip()
    clock.tick(60)
