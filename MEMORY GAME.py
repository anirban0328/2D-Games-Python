# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def expo():
    global exposed
    exposed = []
    for a in range(16):
     exposed.append("FALSE")

def init():
    expo()
    global state
    global i
    global z
    global h
    global count
    global flag
    flag = 0
    count = 0
    l.set_text("Moves = " + str(count))
    state = 0
    h = []
    i = range(8)
    j = range(8)
    random.shuffle(i)
    random.shuffle(j)
    i.extend(j)
    random.shuffle(i)
        
# define event handlers
def mouseclick(p):
    global state
    global exposed
    global z
    global count
    n = 0
    while n < 16:          
      pos = 50 * n
      pos1 = 50 * (n+1)
      if( pos < p[0] < pos1):  
           if exposed[n] == "TRUE":
                return
           else: 
             exposed[n] = "TRUE"
             z = n
      n+=1       
    if state == 0:
        count +=1
        l.set_text("Moves = " + str(count))
        state = 1
    elif state == 1:
        l.set_text("Moves = " + str(count))
        state = 2
    else:
        count +=1
        l.set_text("Moves = " + str(count))
        state = 1
        
        
# cards are logically 50x100 pixels in size    
def draw(canvas):
       global state
       global y 
       global z
       global i
       global h
       global flag
       global abc
       global xyz 
       m = 1        
       for a in i:   
         pos = 50 * m
         canvas.draw_line((pos, 60), (pos+2, 60), 130, "Blue")        
         m += 1                 
       if state == 1:
              if flag == 1:  
                exposed[abc] = "FALSE"
                exposed[xyz] = "FALSE"                 
              flag = 0
              y = z   
              pos = 50 * z  
              canvas.draw_text(str(i[z]), (pos+15, 60), 40, "Red")               
              for c in h:              
                 canvas.draw_text(str(i[c]), ((c* 50) +15, 60), 40, "Teal")                
                  
       if state == 2:
              flag = 1          
              abc = y
              xyz = z         
              pos = 50 * y
              pos1 = 50 * z                       
              canvas.draw_text(str(i[z]), (pos1+15, 60), 40, "Red")      
              canvas.draw_text(str(i[y]), (pos+15, 60), 40, "Red")
                        
              if (i[y] == i[z]):
                  h.append(y)
                  h.append(z)
                  exposed[z] = "TRUE"
                  exposed[y] = "TRUE"                            
              for c in h:              
                   canvas.draw_text(str(i[c]), ((c* 50) +15, 60), 40, "Teal")            
                                                                    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)
l=frame.add_label("Moves = 0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()