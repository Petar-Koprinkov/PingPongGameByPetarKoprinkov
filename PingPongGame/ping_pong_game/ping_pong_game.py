import sys
import random
import pygame


# Input player names and choose the level of the game
player1_name = input("Enter name for Player 1: ")
player2_name = input("Enter name for Player 2: ")
level = input("Choose level for the game: \n-Easy \n-Medium \n-Hard \n")

level_to_speed = {
    "Easy": 5,
    "Medium": 7,
    "Hard": 9
}

# Set the default speed to 7
ball_speed = level_to_speed.get(level, 7)

pygame.init()

WIDTH, HEIGHT = 900, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

paddle_width, paddle_height = 15, 120
left_paddle_x, right_paddle_x = 10, WIDTH - 25
left_paddle_y, right_paddle_y = HEIGHT // 2 - paddle_height // 2, HEIGHT // 2 - paddle_height // 2
paddle_speed = 7
score_left, score_right = 0, 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong by Petar Koprinkov")

# Randomize the initial direction of the ball
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_speed_x, ball_speed_y = random.choice([-ball_speed, ball_speed]), random.choice([-ball_speed, ball_speed])

# Font for displaying the score
font = pygame.font.Font(None, 36)
countdown_font = pygame.font.Font(None, 72)


def display_countdown(number):
    screen.fill(BLACK)
    text = countdown_font.render(str(number), True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(1000)


# Countdown before game start
for i in range(5, 0, -1):
    display_countdown(i)
display_countdown("Go!")
pygame.time.delay(100)


def reset_ball():
    return WIDTH // 2, HEIGHT // 2, random.choice([-ball_speed, ball_speed]), random.choice([-ball_speed, ball_speed])


# Game loop

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Buttons

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle_y > 0:
        left_paddle_y -= paddle_speed
    if keys[pygame.K_s] and left_paddle_y < HEIGHT - paddle_height:
        left_paddle_y += paddle_speed
    if keys[pygame.K_UP] and right_paddle_y > 0:
        right_paddle_y -= paddle_speed
    if keys[pygame.K_DOWN] and right_paddle_y < HEIGHT - paddle_height:
        right_paddle_y += paddle_speed

    ball_x += ball_speed_x
    ball_y += ball_speed_y

    if (
            left_paddle_x < ball_x < left_paddle_x + paddle_width
            and left_paddle_y < ball_y < left_paddle_y + paddle_height
    ) or (
            right_paddle_x < ball_x < right_paddle_x + paddle_width
            and right_paddle_y < ball_y < right_paddle_y + paddle_height
    ):
        ball_speed_x = - ball_speed_x

    if ball_y <= 0 or ball_y >= HEIGHT:
        ball_speed_y = -ball_speed_y

    if ball_x <= 0:
        score_right += 1
        if score_right >= 10:
            winner_text = font.render(f"{player2_name} Wins! :)", True, WHITE)
            screen.blit(winner_text,
                        (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.delay(3000)  # Display winner message for 3 seconds
            pygame.quit()
            sys.exit()
        ball_x, ball_y, ball_speed_x, ball_speed_y = reset_ball()

    if ball_x >= WIDTH:
        score_left += 1
        if score_left >= 10:
            winner_text = font.render(f"{player1_name} Wins! :)", True, WHITE)
            screen.blit(winner_text,
                        (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.delay(3000)  # Display winner message for 3 seconds
            pygame.quit()
            sys.exit()
        ball_x, ball_y, ball_speed_x, ball_speed_y = reset_ball()

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (left_paddle_x, left_paddle_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, WHITE, (right_paddle_x, right_paddle_y, paddle_width, paddle_height))
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), radius=10)
    score_display = font.render(f"{player1_name}: {score_left} - {player2_name}: {score_right}", True, WHITE)
    screen.blit(score_display, (WIDTH // 2 - score_display.get_width() // 2, 10))

    pygame.display.flip()
    pygame.time.Clock().tick(60)
