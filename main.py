import pygame
import sys
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Pong')

player1_score = 0
player2_score = 0
WIN_THRESHOLD = 5

paddle_y = 250
ai_paddle_y = 250
paddle_speed = .5

ball_x = 400
ball_y = 300
ball_speed_x = 0.4 if random.random() < 0.5 else -0.4
ball_speed_y = 0.35 if random.random() < 0.5 else -0.35

def paddle (paddle_y, ai_paddle_y):
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0,paddle_y, 10, 100))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(790,ai_paddle_y, 10, 100))

def ball(ball_x, ball_y):
    pygame.draw.circle(screen, (255,255,255), (ball_x, ball_y), 10)

def scoreboard():
    font = pygame.font.Font(None, 36)
    player1_text = font.render(str(player1_score), 1, (255, 255, 255))
    player2_text = font.render(str(player2_score), 1, (255, 255, 255))
    screen.blit(player1_text, (50, 10))
    screen.blit(player2_text, (750, 10))

def move_paddle(paddle_y, paddle_speed):
    UPPER_BOUND = 0
    LOWER_BOUND = 500

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        if paddle_y > UPPER_BOUND:
            paddle_y -= paddle_speed
    if keys[pygame.K_s]:
        if paddle_y < LOWER_BOUND:
            paddle_y += paddle_speed

    return paddle_y

def ball_movement(ball_x, ball_y, ball_speed_x, ball_speed_y):

    global player1_score
    global player2_score
    RESET_BALL = (400, 300)

    if ball_x <= 0:
        player2_score += 1
        ball_x, ball_y = RESET_BALL
        ball_speed_x = -ball_speed_x
    elif ball_x >= 790:
        player1_score += 1
        ball_x, ball_y = RESET_BALL
        ball_speed_x = -ball_speed_x

    ball_x += ball_speed_x
    ball_y += ball_speed_y

    if ball_y <= 0 or ball_y >= 600:
        ball_speed_y = -ball_speed_y

    return ball_x, ball_y, ball_speed_x, ball_speed_y

def collision(ball_x, ball_y, ball_speed_x, ball_speed_y, paddle_y):
    PADDLE_HEIGHT = 100
    BALL_RADIUS = 10
    MAX_BOUNCE_ANGLE = 0.5

    if ball_x <= 10 + BALL_RADIUS and paddle_y <= ball_y <= paddle_y + PADDLE_HEIGHT:
        ball_speed_x = -ball_speed_x
        relative_y = (paddle_y + PADDLE_HEIGHT / 2) - ball_y
        normalized_y = relative_y / (PADDLE_HEIGHT / 2)
        ball_speed_y = -normalized_y * MAX_BOUNCE_ANGLE

    elif ball_x >= 790 - 10 - BALL_RADIUS and ai_paddle_y <= ball_y <= ai_paddle_y + PADDLE_HEIGHT:
        ball_speed_x = -ball_speed_x
        relative_y = (ai_paddle_y  + PADDLE_HEIGHT / 2) - ball_y
        normalized_y = relative_y / (PADDLE_HEIGHT / 2)
        ball_speed_y = -normalized_y * MAX_BOUNCE_ANGLE

    return ball_speed_x, ball_speed_y

def check_winner(player1_score, player2_score):

    if player1_score >= WIN_THRESHOLD:
        print('Player 1 Wins!')
        return False
    elif player2_score >= WIN_THRESHOLD:
        print('Player 2 Wins!')
        return False
    else:
        return True
    
def ai_paddle(ball_y, ai_paddle_y):
    UPPER_BOUND = 0
    LOWER_BOUND = 500
    if ball_speed_x > 0:
        if ball_y < ai_paddle_y:
            if ai_paddle_y > UPPER_BOUND:
                ai_paddle_y -= (paddle_speed + .1)
        if ball_y > ai_paddle_y:
            if ai_paddle_y < LOWER_BOUND:
                ai_paddle_y += (paddle_speed + .1)
    return ai_paddle_y

def main():

    global paddle_y
    global paddle_speed
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    global player1_score, player2_score
    global ai_paddle_y

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        paddle_y = move_paddle(paddle_y, paddle_speed)
        ai_paddle_y = ai_paddle(ball_y, ai_paddle_y)
        ball_x, ball_y, ball_speed_x, ball_speed_y = ball_movement(ball_x, ball_y, ball_speed_x, ball_speed_y)
        ball_speed_x, ball_speed_y = collision(ball_x, ball_y, ball_speed_x, ball_speed_y, paddle_y)

        screen.fill((0,0,0))
        paddle(paddle_y, ai_paddle_y)
        ball(ball_x, ball_y)
        scoreboard()

        if not check_winner(player1_score, player2_score):
            running = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()