import pygame
import requests
import time

pygame.init()
s_width = 1600
s_height = 900
screen = pygame.display.set_mode((s_width, s_height))
clock = pygame.time.Clock()

big = pygame.font.SysFont("Manjari", 80)
small = pygame.font.SysFont("Manjari", 30)
blanks_text = ""
type_text = ["hi", "doin", "ur", "mom"]
blanks_storage = []
i = 0

r = 0
g = 0
b = 0
g_timer = 1
b_timer = 2
r_up = True
g_up = True
b_up = True

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
    screen.fill(pygame.Color(r, g, b))

    if i < 4:
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


while generating:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            generating = False

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
    screen.fill(pygame.Color(r, g, b))

    pygame.display.flip()
    clock.tick(60)
