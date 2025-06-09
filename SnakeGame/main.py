import pygame
import sys
import math
from snake import game, reset_snake
from food import food_coordinate
import score
import sound

width = 960
height = 672
step = 24
WHITE = (255, 255, 255)
button_hover = (110, 110, 60)
BLACK = (0, 0, 0)
DIGITS = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

clock = pygame.time.Clock()
x, y = width // 2, height // 2
init_height = 100

pygame.init()
pygame.font.init()
emoji_font = pygame.font.SysFont('Segoe UI Emoji', step - 2)
score_font = pygame.font.SysFont('Segoe UI Emoji', 50)
score_board_font = pygame.font.SysFont('Segoe UI', 50)
text_font = pygame.font.SysFont('Segoe UI', 30)
over_font = pygame.font.SysFont('Segoe UI', 80)
game_over_text = over_font.render('Game Over!', True, BLACK)
reset_text = text_font.render('Play Again', True, WHITE)
close_text = text_font.render('Close', True, WHITE)
cl_text = pygame.font.SysFont('Segoe UI', 20).render('Choose Difficulty', True, WHITE)
hard_text = text_font.render('Hard', True, WHITE)
medium_text = text_font.render('Medium', True, WHITE)
easy_text = text_font.render('Easy', True, WHITE)
score_board_text = pygame.font.SysFont('Segoe UI', 40).render('Score:', True, (110, 210, 210))
high_score_board_text = pygame.font.SysFont('Segoe UI', 40).render('Highest Score:', True, (110, 210, 210))
choose_level_text = pygame.font.SysFont('Segoe UI', 40).render('Choose Difficulty', True, BLACK)


screen = pygame.display.set_mode((width, init_height + height))
pygame.display.set_caption("Snake Game")
end_game = False
food_x, food_y, food_emoji = food_coordinate(width, height , step)
tails = []
game_over_window_width = 800
game_over_window_height = 300
game_over_window_x = width // 2 - game_over_window_width // 2
game_over_window_y = (height + init_height) // 2 - game_over_window_height // 2
game_over_window = pygame.Rect(game_over_window_x, game_over_window_y, game_over_window_width, game_over_window_height)
button_width = 0.25 * game_over_window_width
button_height = 0.2 * game_over_window_height
reset_button = pygame.Rect(game_over_window_x + 0.2 * game_over_window_width - button_width / 2, game_over_window_y + 0.7 * game_over_window_height, button_width, button_height)
close_button = pygame.Rect(game_over_window_x + 0.5 * game_over_window_width - button_width / 2, game_over_window_y + 0.7 * game_over_window_height, button_width, button_height)
choose_level_button = pygame.Rect(game_over_window_x + 0.8 * game_over_window_width - button_width / 2, game_over_window_y + 0.7 * game_over_window_height, button_width, button_height)
high_score = score.get_high_score()
score_added = False
high_score_update = False

choose_level_screen = True
level_chosen = False
should_update_music = False
choose_level_width = 300
choose_level_height = 400
choose_level_x = width // 2 - choose_level_width // 2
choose_level_y = (height + init_height) // 2 - choose_level_height // 2
choose_level_window = pygame.Rect(choose_level_x, choose_level_y, choose_level_width, choose_level_height)
hard_button = pygame.Rect(choose_level_x + 0.5 * choose_level_width - button_width / 2, choose_level_y + 0.3 * choose_level_height, button_width, button_height)
medium_button = pygame.Rect(choose_level_x + 0.5 * choose_level_width - button_width / 2, choose_level_y + 0.5 * choose_level_height, button_width, button_height)
easy_button = pygame.Rect(choose_level_x + 0.5 * choose_level_width - button_width / 2, choose_level_y + 0.7 * choose_level_height, button_width, button_height)

fps = 60

running = True
while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            score.add_score_to_db()

    if not end_game and not choose_level_screen:
        x, y, food_x, food_y, end_game, tails, food_emoji, move_now = game(width, height, step, x, y, food_x, food_y, tails, food_emoji)

    if should_update_music:
        sound.stop_music()
        sound.load_music(what_level)
        should_update_music = False

    screen.fill(BLACK)
    score_now = score.get_score()
    score_digits = [0, 0, 0, 0]
    text_c = score_board_text.get_rect(center=(60, 45))
    screen.blit(score_board_text, text_c)
    for i in range(len(score_digits)):
        score_digits[i] = score_now % 10
        score_now //= 10
    for i in range(len(score_digits)):
        digit_emoji = score_font.render(DIGITS[score_digits[len(score_digits) - i - 1]], True, (255, 255, 255))
        screen.blit(digit_emoji, (102 + i * 50, 20))

    pygame.draw.line(screen, WHITE, (width / 2, 0), (width / 2, init_height))

    text_c = high_score_board_text.get_rect(center=(width / 2 + 130, 45))
    screen.blit(high_score_board_text, text_c)
    temp_high_score = high_score
    high_score_digits = [0, 0, 0, 0]
    for i in range(len(high_score_digits)):
        high_score_digits[i] = temp_high_score % 10
        temp_high_score //= 10
    for i in range(len(high_score_digits)):
        digit_emoji = score_font.render(DIGITS[high_score_digits[len(high_score_digits) - i - 1]], True, (255, 255, 255))
        screen.blit(digit_emoji, (width / 2 + 240 + i * 50, 20))
    
    pygame.draw.line(screen, WHITE, (0, init_height), (width, init_height))
    # for i in range(step, width, step):
    #     pygame.draw.line(screen, WHITE, (i, init_height), (i, init_height + height))
    # for j in range(init_height, init_height + height, step):
    #     pygame.draw.line(screen, WHITE, (0, j), (width, j))
    pygame.draw.circle(screen, WHITE, (x + step / 2, y + init_height + step / 2), step / 2)
    head_x = x + step / 2
    head_y = y + init_height + step / 2
    for tail in tails:
        tail_x = tail.x_now + step / 2
        tail_y = tail.y_now + init_height + step / 2
        if math.hypot(head_x - tail_x, head_y - tail_y) < step * 0.5:
            end_game = True
        pygame.draw.circle(screen, tail.color, (tail.x_now + step / 2, tail.y_now + init_height + step / 2), step / 2)

    fod_emoji = emoji_font.render(food_emoji, True, (255, 255, 255))
    screen.blit(fod_emoji, (food_x - 2, food_y + init_height))

    if choose_level_screen:
        pygame.draw.rect(screen, (110, 210, 210), choose_level_window)
        text_c = choose_level_text.get_rect(center=(choose_level_x + choose_level_width / 2, choose_level_y + 0.15 * choose_level_height))
        screen.blit(choose_level_text, text_c)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        text_c = hard_text.get_rect(center=hard_button.center)
        if hard_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, button_hover, hard_button)
            if mouse_click[0]:
                what_level = 'hard'
                fps = 150
                choose_level_screen = False
                should_update_music = True
                end_game = False
        else:
            pygame.draw.rect(screen, BLACK, hard_button)
        screen.blit(hard_text, text_c)

        text_c = medium_text.get_rect(center=medium_button.center)
        if medium_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, button_hover, medium_button)
            if mouse_click[0]:
                what_level = 'medium'
                fps = 100
                choose_level_screen = False
                should_update_music = True
                end_game = False
        else:
            pygame.draw.rect(screen, BLACK, medium_button)
        screen.blit(medium_text, text_c)

        text_c = easy_text.get_rect(center=easy_button.center)
        if easy_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, button_hover, easy_button)
            if mouse_click[0]:
                what_level = 'easy'
                fps = 60
                choose_level_screen = False
                should_update_music = True
                end_game = False
        else:
            pygame.draw.rect(screen, BLACK, easy_button)
        screen.blit(easy_text, text_c)

    if end_game and not choose_level_screen:
        if not score_added:
            score.add_score_to_db()
            score_added = True
        if not high_score_update:
            high_score = score.get_high_score()
            high_score_update = True
        pygame.draw.rect(screen, (110, 210, 210), game_over_window)
        text_c = game_over_text.get_rect(center=(game_over_window_x + game_over_window_width / 2, game_over_window_y + 0.2 * game_over_window_height))
        screen.blit(game_over_text, text_c)
        score_text = score_board_font.render(f'Your Score: {score.get_score()}', True, BLACK)
        text_c = score_text.get_rect(center=(game_over_window_x + game_over_window_width / 2, game_over_window_y + 0.5 * game_over_window_height))
        screen.blit(score_text, text_c)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        text_c = reset_text.get_rect(center=reset_button.center)
        if reset_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, button_hover, reset_button)
            screen.blit(reset_text, text_c)
            if mouse_click[0]:
                end_game = False
                x, y = width // 2, height // 2
                tails = []
                reset_snake()
                score.set_score()
                food_x, food_y, fod_emoji = food_coordinate(width, height, step)
                score_added = False
                high_score_update = False
        else:
            pygame.draw.rect(screen, BLACK, reset_button)
            screen.blit(reset_text, text_c)

        text_c = close_text.get_rect(center=close_button.center)
        if close_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, button_hover, close_button)
            screen.blit(close_text, text_c)
            if mouse_click[0]:
                running = False
                score.set_score()
        else:
            pygame.draw.rect(screen, BLACK, close_button)
            screen.blit(close_text, text_c)

        text_c = cl_text.get_rect(center=choose_level_button.center)
        if choose_level_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, button_hover, choose_level_button)
            screen.blit(cl_text, text_c)
            if mouse_click[0]:
                choose_level_screen = True
                end_game = False
                x, y = width // 2, height // 2
                tails = []
                reset_snake()
                score.set_score()
                food_x, food_y, fod_emoji = food_coordinate(width, height, step)
                score_added = False
                high_score_update = False
        else:
            pygame.draw.rect(screen, BLACK, choose_level_button)
            screen.blit(cl_text, text_c)

    sound.update_music()
    pygame.display.flip()

score.close_db()
pygame.quit()
sys.exit()


