import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 400
screen_height = 700

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

score = 0
last_score_update_time = time.time()

# Player
player_img = pygame.image.load('player.png')
player_img = pygame.transform.scale(player_img, (64, 64))
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() - 100)
player_rect = pygame.Rect(player_pos.x, player_pos.y, player_img.get_width()/2, player_img.get_height()/2)
player_speed = 0.5  # Adjust as needed
cooldown = 5
last_enemy_time = -cooldown
p_distance = 50

# Enemy
enemy_img = pygame.image.load('enemy.png')
enemy_img = pygame.transform.scale(enemy_img, (128, 128))
enemy_rect = pygame.Rect(player_pos.x, player_pos.y, player_img.get_width(), player_img.get_height())
enemy_speed = 0.5  # Adjust as needed
cooldown = 5
enemies = []
last_dash_time = -cooldown
distance = 0.5
enemy_spawn = [2, 1.5, 1.0, 0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1]
enemy_spawn_index = 0


# Bullet
bullet_img = pygame.image.load('03.png')
bullet_img = pygame.transform.scale(bullet_img, (64, 64))
bullet_pos = pygame.Vector2(player_pos.x+2, player_pos.y-30)
speed = 2
bullets = []

# Enemy Bullet
enemy_bullet_img = pygame.image.load('08.png')  
enemy_bullet_img = pygame.transform.scale(enemy_bullet_img, (32, 32))  
enemy_bullets = []
last_enemy_shoot_time = 0
bullet_spawn =[1.0, 0.9,0.8,0.7,0.6,0.5,0.4,0.3]
enemy_bullet_spawn_index = 0


# Heart
heart_img = pygame.image.load('heart.png')
heart_img = pygame.transform.scale(heart_img, (32, 32))
hearts = [pygame.Vector2(0, 0), pygame.Vector2(10, 0), pygame.Vector2(20, 0)]

# Aestroids
rock_img = pygame.image.load('rock.png')
rock_img = pygame.transform.scale(rock_img, (64 , 64))    
rock_speed = 0.5
last_rock_time = 1
rocks = []
rock_spawn=[1.0, 0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1]
rock_spawn_index = 0


# Font
pygame.font.init()
font = pygame.font.Font(None, 36)  # Use default font, size 36

# Function to display text
def display_text(text, x, y):
    text_surface = font.render(text, True, (255, 255, 255))  # Render the text in white
    screen.blit(text_surface, (x, y))

# Player Movement
def player_movement():
    screen.blit(player_img, (player_pos.x, player_pos.y))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos.x += player_speed
    if keys[pygame.K_UP]:
        player_pos.y -= player_speed
    if keys[pygame.K_DOWN]:
        player_pos.y += player_speed

# Boundary
def border():
    if player_pos.x < 0:
        player_pos.x = 0
    elif player_pos.x > screen_width - 64:
        player_pos.x = screen_width - 64
    
    if player_pos.y < 0:
        player_pos.y = 0
    elif player_pos.y > screen_height - 64:
        player_pos.y = screen_height - 64

# Teleport
def teleport():
    ctime = int(time.time())

    if ctime % 5 == 0:
        display_text("DASH", 0, 650)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_pos.x -= p_distance
    
        if keys[pygame.K_d]:
            player_pos.x += p_distance

# Score system
def scoreboard():
    global score, last_score_update_time

    # Check if 1 second has passed since the last score update
    current_time = time.time()
    if current_time - last_score_update_time >= 1.0:
        score += 1  # Increment the score
        last_score_update_time = current_time  # Update last_score_update_time
    
    # Display the updated score
    display_text(f'score: {score}', 250, 0)

def increase_difficulty():
    global rock_spawn_index, enemy_spawn_index, enemy_bullet_spawn_index

    # Adjust spawn intervals based on current difficulty level
    if score >= 0:
        rock_spawn_index = 1 
        enemy_spawn_index = 1
        enemy_bullet_spawn_index= 1
    elif score >= 10:
        rock_spawn_index = 2
        enemy_spawn_index = 2
        enemy_bullet_spawn_index= 2
    elif score >= 20:
        rock_spawn_index = 3 
        enemy_spawn_index = 3
        enemy_bullet_spawn_index= 3
    elif score >= 25:
        rock_spawn_index = 4
        enemy_spawn_index = 4
        enemy_bullet_spawn_index= 4
    elif score >= 30:
        rock_spawn_index = 5 
        enemy_spawn_index = 5
        enemy_bullet_spawn_index= 5
    elif score >= 35:
        rock_spawn_index = 6 
        enemy_spawn_index = 6
        enemy_bullet_spawn_index= 6
    elif score >= 40:
        rock_spawn_index = 7 
        enemy_spawn_index = 7

# Shooting
def shooting():
    global last_shoot_time
    current_time = time.time()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and current_time - last_shoot_time >= 0.2:  # Check if 1 second has passed 
        bullet_pos = pygame.Vector2(player_pos.x + 2, player_pos.y - 30)  # Adjust bullet initial position
        bullet_rect = pygame.Rect(bullet_pos.x, bullet_pos.y, bullet_img.get_width(), bullet_img.get_height())
        bullets.append((bullet_pos, bullet_rect))
        last_shoot_time = current_time
        

    # Move bullets and delete if off screen
    for bullet in bullets[:]:  # Use a slice to iterate over a copy of the list
        bullet[0].y -= speed
        bullet[1].topleft = (bullet[0].x, bullet[0].y)  # Update bullet rect position
        screen.blit(bullet_img, (bullet[0].x, bullet[0].y))
        if bullet[0].y < 0:  # Check if bullet is off the screen
            bullets.remove(bullet)

def lives():
    for heart_pos in hearts:
        screen.blit(heart_img, heart_pos)
    
    if not hearts:
        pygame.quit()

def rock():
    global last_rock_time
    current_time = time.time()
    
    if current_time - last_rock_time >= rock_spawn[rock_spawn_index]:  # Check if 1 second has passed 0.2
        rock_pos = pygame.Vector2(random.randint(5, 395), -50) # Adjust rock initial position
        rock_rect = pygame.Rect(rock_pos.x, rock_pos.y, rock_img.get_width(), rock_img.get_height())
        rocks.append((rock_pos,rock_rect))
        last_rock_time = current_time

    # Move rocks and delete if off screen
    for rock in rocks[:]:  # Use a slice to iterate over a copy of the list
        rock[0].y += rock_speed
        rock[1].topleft = (rock[0].x, rock[0].y)  # Update rock rect position
        screen.blit(rock_img, (rock[0].x, rock[0].y))
        if rock[0].y > screen_height:  # Check if rock is off the screen
            rocks.remove(rock)

def enemy():
    global last_enemy_time
    current_time = time.time()
    
    if current_time - last_enemy_time >= enemy_spawn[enemy_spawn_index]:  # Check if 1 second has passed 1
        enemy_pos = pygame.Vector2(random.randint(5, 395), -50) # Adjust enemy initial position
        enemy_rect = pygame.Rect(enemy_pos.x, enemy_pos.y, enemy_img.get_width(), enemy_img.get_height())
        enemies.append((enemy_pos,enemy_rect))
        last_enemy_time = current_time

    # Move enemy and delete if off screen
    for enemy in enemies[:]:  # Use a slice to iterate over a copy of the list
        enemy[0].y += enemy_speed
        enemy[1].topleft = (enemy[0].x, enemy[0].y)  # Update enemy rect position
        screen.blit(enemy_img, (enemy[0].x, enemy[0].y))
        if enemy[0].y > screen_height:  # Check if rock is off the screen
            enemies.remove(enemy)

    global last_bullet_time
    current_time = time.time()

def enemy_shooting():
    global last_enemy_shoot_time
    current_time = time.time()
    
    # Enemy shooting cooldown
    if current_time - last_enemy_shoot_time >= bullet_spawn[enemy_bullet_spawn_index]:  # Enemy shoots every 1 second 0.5
        for enemy in enemies:  # Each enemy can shoot a bullet
            enemy_bullet_pos = pygame.Vector2(enemy[0].x + enemy_img.get_width() // 2, enemy[0].y + enemy_img.get_height())
            enemy_bullet_rect = pygame.Rect(enemy_bullet_pos.x, enemy_bullet_pos.y, enemy_bullet_img.get_width(), enemy_bullet_img.get_height())
            enemy_bullets.append((enemy_bullet_pos, enemy_bullet_rect))
        last_enemy_shoot_time = current_time
    
    
    # Move enemy bullets and delete if off screen
    for bullet in enemy_bullets[:]:  # Use a slice to iterate over a copy of the list
        bullet[0].y += speed  # Enemy bullets move downwards
        bullet[1].topleft = (bullet[0].x, bullet[0].y)  # Update bullet rect position
        screen.blit(enemy_bullet_img, (bullet[0].x -15, bullet[0].y))
        if bullet[0].y > screen_height:  # Check if bullet is off the screen
            enemy_bullets.remove(bullet)


# Rock collision
def rock_collision():
    for bullet in bullets[:]:  # Use a slice to iterate over a copy of the list
        for rock in rocks[:]:  # Use a slice to iterate over a copy of the list
            if bullet[1].colliderect(rock[1]):
                bullets.remove(bullet)  # Remove the bullet that collided with the rock
                rocks.remove(rock)

# Enemy collision
def enemy_collision():
    for bullet in bullets[:]:  
        for enemy in enemies[:]:  
            if bullet[1].colliderect(enemy[1]):
                bullets.remove(bullet)  
                enemies.remove(enemy)

def player_collision():
    for rock in rocks[:]:
        if rock[1].collidepoint(player_pos.x,player_pos.y):
            rocks.remove(rock)
            if hearts:
                hearts.pop()

    for enemy in enemies[:]:
        if enemy[1].collidepoint(player_pos.x,player_pos.y):
            enemies.remove(enemy)
            if hearts:
                hearts.pop()

    for bullet in enemy_bullets[:]:
        if bullet[1].collidepoint(player_pos.x,player_pos.y):
            enemy_bullets.remove(bullet)
            if hearts:
                hearts.pop()





# Game Loop
running = True
last_shoot_time = 0  # Initialize last shoot time

      
while running:
    screen.fill((0, 0, 0))  # Fill the screen with black color

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    player_movement()
    border()
    teleport()
    shooting()
    lives()
    rock()
    rock_collision()
    enemy() 
    enemy_collision()
    enemy_shooting()   
    player_collision()  
    scoreboard()
    increase_difficulty()


    pygame.display.update()  # Update the display

# Quit Pygame
pygame.quit()
