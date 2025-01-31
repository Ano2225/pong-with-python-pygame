import pygame, sys, random

def add_numbers(a, b):
    return a + b

def ball_animation():
     global ball_speed_x, ball_speed_y, score_sound, paddle_hit_sound
     ball.x += ball_speed_x
     ball.y += ball_speed_y
     
     #handle collisions
     if ball.top <= 0 or ball.bottom >= screen_height:
         ball_speed_y *= -1
     if ball.left <= 0 or ball.right >= screen_width:
        ball_restart()
         
     if ball.colliderect(player) or ball.colliderect(opponent):
         ball_speed_x *= -1
         paddle_hit_sound.play()

def player_animation():
     player.y += player_speed
     if player.top <= 0:
         player.top = 0
     if player.bottom >= screen_height:
         player.bottom = screen_height

def opponent_ai():
    if opponent.top < ball.y:
         opponent.top += opponent_speed
    if opponent.bottom > ball.y:
         opponent.bottom -= opponent_speed
    if opponent.top <= 0:
         opponent.top = 0
    if opponent.bottom >= screen_height:
         opponent.bottom = screen_height 

def ball_restart():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, game_over
    
    
    #Determine who scored 
    if ball.left <= 0:
        player_score += 1
        score_sound.play()
    elif ball.right >= screen_width:
        opponent_score += 1
        score_low.play()
    
    if player_score >= MAX_SCORE or opponent_score >= MAX_SCORE:
        game_over = True
    
    ball.center = (screen_width/2, screen_height/2)
    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))
 
             
#General setup
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

#setting up the main window
screen_width = 1280
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Game Rectangle
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15,30,30)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70,10,140)
opponent = pygame.Rect(10, screen_height/2 - 70,10,140)

#Game over variables
replay_button = pygame.Rect(screen_width/2 - 100, screen_height/2 + 50, 200, 50)
quit_button = pygame.Rect(screen_width/2 - 100, screen_height/2 + 120, 200, 50)

#colors
bg_color = pygame.Color('grey12')
light_grey = (200,200,200)
accent_color = (100, 150, 250)
green = (0,128, 0)

#speed variables
ball_speed_y = 7
ball_speed_x = 7
player_speed = 0
opponent_speed = 7

#score variable
player_score = 0
opponent_score = 0
MAX_SCORE = 5
game_over = False
waiting = True

font = pygame.font.Font(None, 42)

#countdown variable
countdown_duration = 3
countdown_font = pygame.font.Font(None, 100)
start_time = pygame.time.get_ticks()

#add song
paddle_hit_sound = pygame.mixer.Sound('sound/paddle_hiit.mp3')
score_sound = pygame.mixer.Sound('sound/score_sound.mp3')
score_low = pygame.mixer.Sound('sound/score_lower.mp3')
countdown_sound = pygame.mixer.Sound('sound/countdown.mp3')

while True:
     #Handling input
     for event in pygame.event.get():
         if event.type == pygame.QUIT:
             pygame.quit()
             sys.exit()
         if event.type == pygame.KEYDOWN:
             if event.key == pygame.K_DOWN:
                 player_speed += 7
             if event.key == pygame.K_UP:
                 player_speed -= 7
         if event.type == pygame.KEYUP:
             if event.key == pygame.K_DOWN:
                 player_speed -= 7
             if event.key == pygame.K_UP:
                 player_speed += 7
     
     current_time = pygame.time.get_ticks()
     remaining_time = max(countdown_duration - (current_time - start_time) // 1000, 0)  
     
     if remaining_time > 0:
         #countdown screen
         screen.fill(bg_color)
         countdown_text = countdown_font.render(str(remaining_time), True, (255,0,0)) 
         countdown_rect = countdown_text.get_rect(center=(screen_width/2,screen_height/2))          
         screen.blit(countdown_text, countdown_rect)
         countdown_sound.play()

         pygame.display.flip()
         continue
                 
     if not game_over:
        ball_animation()
        player_animation()
        opponent_ai()
        
        #Visuals
        screen.fill(bg_color)
        pygame.draw.rect(screen, light_grey, player)
        pygame.draw.rect(screen, light_grey, opponent)
        pygame.draw.ellipse(screen, (200, 200,255), ball)
        pygame.draw.ellipse(screen, accent_color, ball, width=2)
        pygame.draw.aaline(screen, light_grey, (screen_width/2,0), (screen_width/2,screen_height))
     
        score_text = font.render('Score', True, light_grey)
        score_text_rect = score_text.get_rect(center=(screen_width/2, 20))
        
        score_surface = font.render(f'{opponent_score}  {player_score}',True, light_grey)
        score_rect = score_surface.get_rect(center=(screen_width/2, 50))
        screen.blit(score_surface, score_rect)
        screen.blit(score_text, score_text_rect)
        
        #updating the window
        pygame.display.flip()
        clock.tick(60)
     
     if game_over: 
        #Game over screen
        screen.fill(bg_color)
        winner_text = font.render('Congratulations , you have won 🎉 !' if player_score >= MAX_SCORE else 'Computer Wins 😔', True, green)
        winner_rect = winner_text.get_rect(center=(screen_width/2, screen_height/2))
        screen.blit(winner_text, winner_rect)
        
        #Draw buttons
        pygame.draw.rect(screen, accent_color, replay_button, border_radius=10)
        pygame.draw.rect(screen, (50, 50, 100), replay_button, border_radius=10, width=2) 

        pygame.draw.rect(screen, light_grey, quit_button, border_radius=10)
        
        #Button text
        replay_text = font.render('Replay', True, bg_color)
        quit_text = font.render('Quit', True, bg_color)
        
        replay_text_rect = replay_text.get_rect(center=replay_button.center)
        quit_text_rect = quit_text.get_rect(center=quit_button.center)
        
        screen.blit(replay_text, replay_text_rect)
        screen.blit(quit_text, quit_text_rect)
        
        pygame.display.flip()
        
        #handle button clicks
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if replay_button.collidepoint(mouse_pos):
                    #reset game state
                    player_score = 0
                    opponent_score = 0
                    game_over = False
                    ball.center = (screen_width/2, screen_height/2)
                    start_time = pygame.time.get_ticks()
                elif quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()   
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
   
    
         
     