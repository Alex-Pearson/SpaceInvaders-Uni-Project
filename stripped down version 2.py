import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1024, 704 #the resolution has been lowered to make the space smaller to make the game harder
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders Requirement for second objective")

clock = pygame.time.Clock()

# Loads the defender image sets it size and sets it speed
player_img = pygame.image.load("Defender.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (80, 80))
player_rect = player_img.get_rect()
player_rect.midbottom = (WIDTH // 2, HEIGHT - 10)
player_speed = 5

score=0 
#This code is for the players lives
player_lives = 3
player_respawn_time = 2000   # 2 seconds of invincibility after hit
player_last_hit = 0
player_alive = True
player_flash_interval = 150   # milliseconds between flashes

bullets = []
bullet_speed = -20
last_shot_time = 0
shot_delay = 500

#We have created a seperate bullet for the invaders, as we don't want them shooting themselves      
enemy_bullets = []
enemy_bullet_speed = 7
enemy_shoot_probability = 0.001   # 0.1% chance per frame

invader_img_row1 = pygame.image.load("Invader 1.png").convert_alpha() #this code i've changed to load pngs instead of the placeholder red blocks
invader_img_row1 = pygame.transform.scale(invader_img_row1, (60, 60))

invader_img_row2 = pygame.image.load("Invader 2.png").convert_alpha()
invader_img_row2 = pygame.transform.scale(invader_img_row2, (60, 60))

invader_img_row3 = pygame.image.load("Invader 3.png").convert_alpha()
invader_img_row3 = pygame.transform.scale(invader_img_row3, (60, 60))

# the invaders has been changed to an array now, this is so we can add more than one invader at a time 
invaders = []

rows = 3       # we are chaning to 3 rows
cols = 10      # how many invaders per row
spacing_x = 80 # horizontal spacing
spacing_y = 80
start_x = 50
start_y = 10

row_images = [invader_img_row1, invader_img_row2, invader_img_row3] # new array for the images

for row in range(rows):
    for col in range(cols):
        x = start_x + col * spacing_x
        y = start_y + row * spacing_y

        rect = pygame.Rect(x, y, 60, 60)
        image = row_images[row]  # pick image based on row

        invaders.append({"rect": rect, "image": image})



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

        # this is for the collusion for
        for inv in invaders[:]:
            if bullet.colliderect(inv["rect"]):
                invaders.remove(inv)
                bullets.remove(bullet)
                score += 10   
                break

    screen.fill((0, 0, 0)) # this is needed other when the defender is moved the screen will stay green

    #this will make the player flash when inv
    if not player_alive:
        time_since_hit = pygame.time.get_ticks() - player_last_hit
        # toggle visibility every flash interval
        if (time_since_hit // player_flash_interval) % 2 == 0:
            screen.blit(player_img, player_rect)  # visible this frame
    else:
        # normal drawing when alive
        screen.blit(player_img, player_rect)


    for bullet in bullets:
        pygame.draw.rect(screen, (0, 255, 0), bullet)

    for inv in invaders:
        screen.blit(inv["image"], inv["rect"])

    for eb in enemy_bullets:
        pygame.draw.rect(screen, (255, 255, 255), eb)
    
    if not player_alive:
        if pygame.time.get_ticks() - player_last_hit > player_respawn_time:
            player_alive = True

    # Enemy shooting: only the top row
    if invaders:
        # Find top row (lowest y value)
        min_y = min(inv["rect"].y for inv in invaders)
        top_row = [inv for inv in invaders if inv["rect"].y == min_y]

        # Random shooting chance from top row invaders
        for inv in top_row:
            if random.random() < enemy_shoot_probability:
                bullet = pygame.Rect(inv["rect"].centerx - 3, inv["rect"].bottom, 6, 15)
                enemy_bullets.append(bullet)

        # Move enemy bullets
    for eb in enemy_bullets[:]:
        eb.y += enemy_bullet_speed

        # Bullet leaves screen
        if eb.top > HEIGHT:
            enemy_bullets.remove(eb)
            continue
    # Enemy bullet collusion will take a life away from the player when hit
        if eb.colliderect(player_rect) and player_alive:
            enemy_bullets.remove(eb)

            player_lives -= 1
            player_alive = False
            player_last_hit = pygame.time.get_ticks()

            player_rect.midbottom = (WIDTH // 2, HEIGHT - 10)

            if player_lives <= 0:
                print("GAME OVER")
                running = False    

    font = pygame.font.SysFont(None, 40)
    lives_text = font.render(f"Lives: {player_lives}", True, (0, 255, 0))
    screen.blit(lives_text, (10, 10))

    score_text = font.render(f"Score: {score}", True, (0, 255, 0))
    screen.blit(score_text, (10, 50))

    pygame.display.update()
    clock.tick(60) #lmits to 60fps for consistancy across multiple systems, helps the game to run cosistantly 

pygame.quit()