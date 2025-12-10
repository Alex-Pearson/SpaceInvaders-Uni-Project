import pygame

pygame.init()

# dictating th size of the screen, standard hd screen size
WIDTH, HEIGHT = 1024, 576 #the resolution has been lowered to make the space smaller to make the game harder
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


# the invaders has been changed to an array now, this is so we can add more than one invader at a time 
invaders = []

rows = 1       # how many horizontal rows
cols = 10      # how many invaders per row
spacing_x = 80 # horizontal spacing
start_x = 50
start_y = 10

for row in range(rows):
    for col in range(cols):
        x = start_x + col * spacing_x
        y = start_y + row * 70
        invaders.append(pygame.Rect(x, y, 60, 60))


invader_step_time = 700      # move every 0.7 seconds
last_invader_move = 0
invader_direction = 1         # 1 = right, -1 = left
invader_step_size = 40        # distance per horizontal jump
invader_drop = 25             # vertical drop when hitting an edge

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
        for inv in invaders[:]:
            if bullet.colliderect(inv):
                invaders.remove(inv)
                bullets.remove(bullet)
                break


    if invaders and current_time - last_invader_move >= invader_step_time:

        # Move entire group horizontally
        for inv in invaders:
            inv.x += invader_direction * invader_step_size

        # Edge detection based on left-most or right-most invader
        left_edge = min(inv.left for inv in invaders)
        right_edge = max(inv.right for inv in invaders)

        if right_edge >= WIDTH or left_edge <= 0:
            invader_direction *= -1  # reverse direction
            for inv in invaders:
                inv.y += invader_drop  # move all down

        last_invader_move = current_time



    screen.fill((0, 0, 0)) # this is needed other when the defender is moved the screen will stay green

    screen.blit(player_img, player_rect)

    for bullet in bullets:
        pygame.draw.rect(screen, (0, 255, 0), bullet)

    for inv in invaders:
        pygame.draw.rect(screen, (255, 0, 0), inv)


    pygame.display.update()
    clock.tick(60) #lmits to 60fps for consistancy across multiple systems

pygame.quit()