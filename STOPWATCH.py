# "Stopwatch: The Game"
import simplegui

# global variables
timer=0
time=0
message="0:00.0"
message1="0/0"
attempts=0
success=0
started=0

# helper function that converts integer counting tenths of seconds into formatted string A:BC.D
def timer_handler(): 
    global time
    time +=1
    format(time)

def format(t):
    global message
    a=t%10
    b=t/10
    c=int(b/60)
    d=int(b%60)
    
    if d<10:
        d="0"+str(d)
        message =str(c)+":"+d+"."+str(a)
    else:
        message =str(c)+":"+str(d)+"."+str(a)
    
# event handlers for buttons "Start", "Stop", "Reset"
def start():
     timer.start()
     global started
     started = 1
        
def stop():
    timer.stop()
    global attempts
    global success
    global started
    global message1
    
    if started==1:    
        if time%5==0:
            success+=1        
        started=0
        attempts+=1
    message1 = str(success)+"/"+str(attempts)    
            
def reset():
    global time
    global started
    global attempts
    global success
    global message1
    started=0
    attempts=0
    success=0
    timer.stop()
    time=0
    format(time)
    message1 = str(success)+"/"+str(attempts)    
    
# draw handler
def draw(canvas):
    canvas.draw_text(message,[150,150], 50, "Red")
    canvas.draw_text(message1,[400,50], 40, "Green")
        
# create frame
frame = simplegui.create_frame("Stopwatch", 500, 300)

# register event handlers
frame.add_button("START", start)
frame.add_button("STOP", stop)
frame.add_button("RESET", reset)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, timer_handler)

# start timer and frame
frame.start()

