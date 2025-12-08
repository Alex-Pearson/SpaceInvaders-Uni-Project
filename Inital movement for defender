import pygame

pygame.init()

# dictating th size of the screen, standard hd screen size
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

#creating a clock for keeping track of time
clock = pygame.time.Clock()

# Loads the defender image sets it size and sets it speed
player_img = pygame.image.load("Defender.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (80, 80))
player_rect = player_img.get_rect()
player_rect.midbottom = (WIDTH // 2, HEIGHT - 10)
player_speed = 5

#this while loop keeps the game running, the for loop collects any updates like key presses
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += player_speed

    
    screen.fill((0, 0, 0)) # this is needed other when the defender is moved the screen will stay green
    screen.blit(player_img, player_rect)  
    pygame.display.update()
    clock.tick(60) #lmits to 60fps for consistancy across multiple systems

pygame.quit()
