# Implementation of classic arcade game Pong
import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 18
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
ball_vel = [0,0]

# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel
    ball_pos = [WIDTH/2, HEIGHT/2] 
    if right == 0:
       ball_vel[0] = random.randrange(2, 4)
       ball_vel[1] = random.randrange(-3, -1)
    else:
       ball_vel[0] = random.randrange(-4, -2)
       ball_vel[1] = random.randrange(-3, -1)
           
# define event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global score1, score2
    paddle1_pos = [150, 230]
    paddle2_pos = [150, 230]
    paddle1_vel = [0, 0]
    paddle2_vel = [0, 0] 
    score1 = 0
    score2 = 0
    ball_init(0)
    
def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos[0] += paddle1_vel[0]
    paddle1_pos[1] += paddle1_vel[1]
    paddle2_pos[0] += paddle2_vel[0]
    paddle2_pos[1] += paddle2_vel[1]
    if(paddle1_pos[1] > HEIGHT or paddle1_pos[0] < 0):
       paddle1_vel[0] = 0
       paddle1_vel[1] = 0
    if(paddle2_pos[1] > HEIGHT or paddle2_pos[0] < 0):
       paddle2_vel[0] = 0
       paddle2_vel[1] = 0   
    
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 1],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 1],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 1],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw paddles
    c.draw_line((HALF_PAD_WIDTH, paddle1_pos[0]),(HALF_PAD_WIDTH, paddle1_pos[1]), 8, "Blue")
    c.draw_line((WIDTH-HALF_PAD_WIDTH, paddle2_pos[0]),(WIDTH-HALF_PAD_WIDTH, paddle2_pos[1]), 8, "Blue")
    
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # collide and reflect off top and bottom screen
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
       ball_vel[1] = - ball_vel[1]
        
    # respawn if it touches left or right screen or bounce back if it touches paddle
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:        
       if ball_pos[1] + BALL_RADIUS < paddle1_pos[0] or ball_pos[1] - BALL_RADIUS > paddle1_pos[1] :
          score2 +=1      
          ball_init(0)
             
       else:
          ball_vel[0] = 1.1 * ball_vel[0]
          ball_vel[1] = 1.1 * ball_vel[1]  
          ball_vel[0] = - ball_vel[0]
   
    elif ball_pos[0] >= WIDTH - (BALL_RADIUS + PAD_WIDTH):
       if ball_pos[1] + BALL_RADIUS < paddle2_pos[0] or ball_pos[1] - BALL_RADIUS > paddle2_pos[1] :
          score1 +=1      
          ball_init(1)
             
       else:
          ball_vel[0] = 1.2 * ball_vel[0]
          ball_vel[1] = 1.2 * ball_vel[1]  
          ball_vel[0] = - ball_vel[0]        
                        
    # draw ball and scores    
    c.draw_circle(ball_pos, BALL_RADIUS, 2, "Green", "White")
    c.draw_text(str(score1), (220, 50), 32, "Green")
    c.draw_text(str(score2), (350, 50), 32, "Green")
    c.draw_text("Player1", (210, 18), 12, "Green")
    c.draw_text("Player2", (340, 18), 12, "Green")
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
       paddle1_vel[0] -= 5
       paddle1_vel[1] -= 5
    elif key == simplegui.KEY_MAP["s"]:
       paddle1_vel[0] += 5
       paddle1_vel[1] += 5
    if key == simplegui.KEY_MAP["up"]:
       paddle2_vel[0] -= 5
       paddle2_vel[1] -= 5
    elif key == simplegui.KEY_MAP["down"]:
       paddle2_vel[0] += 5
       paddle2_vel[1] += 5        
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
       paddle1_vel[0] = 0
       paddle1_vel[1] = 0
    elif key == simplegui.KEY_MAP["s"]:
       paddle1_vel[0] = 0
       paddle1_vel[1] = 0
    if key == simplegui.KEY_MAP["up"]:
       paddle2_vel[0] = 0
       paddle2_vel[1] = 0
    elif key == simplegui.KEY_MAP["down"]:
       paddle2_vel[0] = 0
       paddle2_vel[1] = 0        

# create frame
frame = simplegui.create_frame("Pong Game", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", init, 100)

# start frame
init()
frame.start()