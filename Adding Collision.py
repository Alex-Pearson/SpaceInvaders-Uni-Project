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

# We store bullets in an array so we can have have more than one bullet at a time, i've added a delay because it would shoot too fast
bullets = []
bullet_speed = -20
last_shot_time = 0
shot_delay = 500

# this while loop keeps the game running, the for loop collects any updates like key presses
# this is a test placeholder asset for the invader 
invader = pygame.Rect(300, 100, 60, 60)


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

    # Shooting bullets with space bar (max 2 bullets, 1s delay)
    current_time = pygame.time.get_ticks()
    if keys[pygame.K_SPACE]:
        if len(bullets) < 2 and current_time - last_shot_time > shot_delay:
            bullet_rect = pygame.Rect(player_rect.centerx - 5, player_rect.top, 5, 20)
            bullets.append(bullet_rect)
            last_shot_time = current_time  # reset cooldown timer

    # Update bullets
    for bullet in bullets[:]:
        bullet.y += bullet_speed
        if bullet.bottom < 0:
            bullets.remove(bullet)

        # Collision detection: bullet vs invader
        if invader and bullet.colliderect(invader):
            bullets.remove(bullet)
            invader = None  # thisdestroy invader

   
    screen.fill((0, 0, 0)) # this is needed other when the defender is moved the screen will stay green
    screen.blit(player_img, player_rect)

    for bullet in bullets:
        pygame.draw.rect(screen, (0, 255, 0), bullet)

    if invader:
        pygame.draw.rect(screen, (255, 0, 0), invader)  # i've just used a red box temporaly will be a real asset later

    pygame.display.update()
    clock.tick(60) #lmits to 60fps for consistancy across multiple systems


pygame.quit()
