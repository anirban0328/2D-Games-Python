# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
width = 800
height = 600
score = 0
lives = 3
time = 0
collisions = 0
started = False
rock_group = set([])
missile_group = set([])
explosion_group = set([])

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)

def keydown(key):
        if key == simplegui.KEY_MAP["up"]:
            my_ship.set_thrust(True)            
        if key == simplegui.KEY_MAP["right"]:
            my_ship.increase_angle()
        if key == simplegui.KEY_MAP["left"]:
            my_ship.increase_angle_anti()
        if key == simplegui.KEY_MAP["space"]:
            my_ship.shoot()            
            
def keyup(key):
        if key == simplegui.KEY_MAP["up"]:
            my_ship.set_thrust(False)
        if key == simplegui.KEY_MAP["right"]:
            my_ship.decrease_angle()
        if key == simplegui.KEY_MAP["left"]:
            my_ship.decrease_angle()
    
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    timer.start()
    global started,score,lives
    center = [width / 2, height / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        score = 0
        lives = 3
        started = True
        soundtrack.rewind()
        soundtrack.play()
        
def process_sprite_group(group_set,canvas):
    for group in list(group_set):
        group.draw(canvas)
        group.update()
        if group.update() == False:
            group_set.remove(group) 
                
def group_collide(group_set,other_sprite):
    global collisions
    for group in list(group_set):
         if group.collide(other_sprite):
            group_set.remove(group)
            collisions += 1
            group_pos = group.get_position()
            explosion_group.add(Sprite(group_pos, [0,0], 0, 0, explosion_image, explosion_info, explosion_sound))
            return collisions
        
def group_group_collide(group_1, group_2):
     global score  
     for group in group_1:
         if group_collide(group_2,group):
             group_1.remove(group) 
             score +=10  
                
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
    def draw(self,canvas):
        if self.thrust:
           canvas.draw_image(self.image, [130,45], self.image_size, self.pos, self.image_size, self.angle)
        else:
           canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
    def update(self):        
        #position update
        self.angle += self.angle_vel
        self.pos[0] =(self.pos[0] + self.vel[0]) % width
        self.pos[1] =(self.pos[1] + self.vel[1]) % height
        
        #friction update
        self.vel[0] *= 0.99
        self.vel[1] *= 0.99
        
        #accleration update
        if self.thrust:
         self.vel[0] += 0.1 * angle_to_vector(self.angle)[0]
         self.vel[1] += 0.1 * angle_to_vector(self.angle)[1]    
        
    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
    
    def increase_angle(self):
        self.angle_vel = 0.05
     
    def increase_angle_anti(self): 
        self.angle_vel = -(0.05)
        
    def decrease_angle(self):
        self.angle_vel = 0 
     
    def shoot(self):
        global a_missile
        x = self.pos[0]+ self.radius * angle_to_vector(self.angle)[0]
        y = self.pos[1]+ self.radius * angle_to_vector(self.angle)[1]
        vel1 = self.vel[0] + 3 * angle_to_vector(self.angle)[0]
        vel2 = self.vel[1] + 3 * angle_to_vector(self.angle)[1]
        missile_group.add(Sprite([x , y], [vel1,vel2], 0, 0, missile_image, missile_info, missile_sound))
                
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
            
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius   
            
    def draw(self, canvas):
         if self.animated:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0]*self.age, self.image_center[1]], self.image_size,
                          self.pos, self.image_size, self.angle)
         else:                
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.age +=0.5
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % width
        self.pos[1] = (self.pos[1] + self.vel[1]) % height
        if(self.age < self.lifespan):            
            return True
        else:
            return False
        
    def collide(self, other_sprite):
        if dist(self.pos,other_sprite.get_position()) < self.radius + other_sprite.get_radius():
            return True
        else:
            return False
           
def draw(canvas):
    global time 
    
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [width/2, height/2], [width, height])
    canvas.draw_image(debris_image, [center[0]-wtime, center[1]], [size[0]-2*wtime, size[1]], 
                                [width/2+1.25*wtime, height/2], [width-2.5*wtime, height])

    # update ship
    my_ship.update()
    
    # draw ship and sprites
    my_ship.draw(canvas)    
    process_sprite_group(rock_group,canvas)
    process_sprite_group(missile_group,canvas)
    process_sprite_group(explosion_group,canvas)
    group_group_collide(rock_group, missile_group)
    
    # rock collide with ship
    if group_collide(rock_group, my_ship):
        global lives,started,score,lives
        lives -=1
        if lives == 0: 
            started = False
            for rock in rock_group:
                rock_group.pop(rock)
            timer.stop()    
        
    # draw lives and score
    canvas.draw_text("Lives", (40, 40), 22, "white")
    canvas.draw_text(str(lives), (40, 70), 22, "white")
    canvas.draw_text("Score", (700, 40), 22, "white")
    canvas.draw_text(str(score), (700, 70), 22, "white")
            
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [width/2, height/2], 
                          splash_info.get_size())
            
# timer handler that spawns a rock    
def rock_spawner():
    rock_pos = [0,0]
    if len(rock_group) < 13:
      rock_pos[0] = ( my_ship.pos[0] + random.randrange( my_ship.radius*2 , width - my_ship.radius*2) ) % width
      rock_pos[1] = ( my_ship.pos[1] + random.randrange( my_ship.radius*2 , height - my_ship.radius*2) ) % height  
      rock_vel = [random.randrange(-10, 10)/10, random.randrange(-10, 10)/10]
      angle = random.random() * .2 - .1  
      rock_group.add(Sprite(rock_pos, rock_vel, 0, angle, asteroid_image, asteroid_info))
    
# initialize frame
frame = simplegui.create_frame("Asteroids", width, height)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

# initialize ship
my_ship = Ship([width / 2, height / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
frame.set_draw_handler(draw)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
frame.start()
