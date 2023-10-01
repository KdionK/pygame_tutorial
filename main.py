import pygame
import pygame.display
import os
pygame.font.init()
pygame.mixer.init()

#window size
WIDTH, HEIGHT = 900, 500

#window size application
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

#declaration of the color inside a tuple
WHITE = (255, 255, 255)
RED = (255, 0 ,0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH/2 - 10/2, 0, 10, HEIGHT)
HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

FPS = 60
VELOCITY = 5
BULLET_VELOCITY = 10
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Assets","space.png")), (WIDTH, HEIGHT))

def draw_screen(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health):
    #rempli l'écran de blanc
    WIN.blit(SPACE, (0, 0))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    pygame.draw.rect(WIN, (0,0,0), BORDER)

    red_health_text = HEALTH_FONT.render("Health : " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health : " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, ( WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    #update le display
    pygame.display.update()

def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT /2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def yellow_movement(keys_pressed, yellow):

    if keys_pressed[pygame.K_a] and yellow.x >= 0:
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width < BORDER.x - 10:
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y >= 0:
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y + yellow.height < HEIGHT:
        yellow.y += VELOCITY

def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x > BORDER.x + BORDER.width:
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + red.width <= WIDTH + 15:
        red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y >= 0:
        red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + red.height < HEIGHT:
        red.y += VELOCITY


def handle_bullet(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    yellow_health = 10
    red_health = 10

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(60)
        #vérifie toutes les events qui se sont passés dans la dernière frame
        for event in pygame.event.get():
            #Si un de ces event était de type QUIT
            if event.type == pygame.QUIT:
                #termine la While Loop
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(yellow_bullets) < 3:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2.5, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < 3:
                    bullet = pygame.Rect(red.x + red.width, red.y + red.height // 2 - 2.5, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""

        if red_health <= 0:
            winner_text = "Yellow Wins !"
        elif yellow_health <= 0:
            winner_text = "Red Wins !"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed, yellow)
        red_movement(keys_pressed, red)

        handle_bullet(yellow_bullets, red_bullets, yellow, red)

        draw_screen(yellow, red,yellow_bullets,red_bullets, yellow_health, red_health)
    #si je suis à l'extérieur de la While Loop, ferme le jeu
    main()


#Si le nom du fichier qui a été exécuté == main => appelle la fonction main()
#if the name of the file that was executed == main => call the main function


if __name__ == "__main__":
    main()