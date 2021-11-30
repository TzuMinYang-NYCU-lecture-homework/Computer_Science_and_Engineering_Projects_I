axis = []
net = []
labels = []
is_running = False
speed = 0
angle = 90*2*Math.PI/360 
height = 35 
preloadAudio('Startup.wav')
preloadAudio('chord.wav')
preloadAudio('gj.wav')
preloadAudio('Go.wav')
playAudio('Startup.wav')

def axisInit():
    global axis, labels
    a = -137
    b = 0
    z = -76.25
    c = 274
    d = 100
    axis.append(arrow(
        pos=vec(a, b+2, z), 
        axis=vec(c+30,0,0), 
        shaftwidth= 1, 
        color = color.white)
    )
    axis.append(arrow(
        pos=vec(a, b, z), 
        axis=vec(0,d+10,0), 
        shaftwidth= 1, 
        color = color.white)
    )
    for t in range(0,20):
        axis.append(box(
            pos=vec(a + (t+1)*(c/20),b+d/2, z), 
            length=1, 
            height=d, 
            width=1)
        ) 
    for j in range(0,10):
        axis.append(box(
            pos=vec(a + c/2,b + (j+1)*(d/10), z), 
            length=c, 
            height=1, 
            width=1,
            color=color.gray(0.8)
        ))
    for y in range(0,6):
        num = str(b+y*(d/5))
        labels.append(label(
            pos=vec(a-2*c/40,b + y*(d/5),-76.25), 
            text = num, 
            height = 20, 
            border = 0, 
            font = 'monospace', 
            color = color.white, 
            box = False))

def net_init():
    global net
    a = -76.25 
    b = 0
    z = 0
    c = 152.5 
    d = 15.25
    for x in range(0,100):
        net.append(box(
            pos=vec(0, -a/2-30 ,-c/2+(x+1)*(c/100)),
            axis = vec(0, 0, 1),
            length=0.2, 
            height=15.2, 
            width=0.2,
            color=color.white
        )) 
    for y in range(0,15):
        net.append(box(
            pos=vec(0,b + (y+1)*(d/15), z),
            axis = vec(0, 0, 1), 
            length=c,   
            height=0.2, 
            width=0.2,
            color=color.white
        ))
    for m in range(0,6):
        net.append(box(
            pos=vec(-117+20*m, 1.5, 0),
            axis = vec(0, 0, 1), 
            length=c, 
            height=0.1, 
            width=0.5,
            color=color.yellow
        ))
    for f in range(0,6):
        net.append(box(
            pos=vec(17+20*f, 1.5, 0),
            axis = vec(0, 0, 1), 
            length=c, 
            height=0.1, 
            width=0.5,
            color=color.yellow
        ))

def table_tennis_init():
    global scene, table, ball, paddle, ball_pos_box, init_value_box, grip, marker
    scene = display(
        background = vec(0.6, 0.3, 0.2),
        forward = vec(1.2,-0.5,-1),
        width = 1200, 
        height = 1000,
        center = vec( -10, -30, -10)
    )
    table = box(
        length = 274, 
        width = 152.5, 
        height = 2.5, 
        pos = vec(0, 0, 0),
        color = vec(0.24, 0.35, 0.67)
    )
    table_lag1 = box(
        length = 5, 
        width = 5, 
        height = 76, 
        pos = vec(-137+5, -38-1.25, -76+5), 
        color = color.black
    )
    table_lag2 = box(
        length = 5, 
        width = 5, 
        height = 76, 
        pos = vec(137-5, -38-1.25, -76+5), 
        color = color.black
    )
    table_lag3 = box(
        length = 5, 
        width = 5, 
        height = 76, 
        pos = vec(-137+5, -38-1.25, 76-5), 
        color = color.black
    )
    table_lag4 = box(
        length = 5, 
        width = 5, 
        height = 76, 
        pos = vec(137-5, -38-1.25, 76-5), 
        color = color.black
    )
    center_line = box(
        pos = vec(0, 1,-5), 
        axis = vec(1,0,0), 
        width = 0.05,
        length = 274,
        color = color.white
    ) 

    paddle = cylinder(
        length = 1, 
        height = 20,
        radius = 13, 
        pos = vec(-117, 20, 10), 
        color = color.red,
        axis = vec( -1* sin(angle), 1 * cos(angle), 0)
    )
    grip = cylinder(
        length = 18,
        radius = 2,
        pos = vec(-117, 20, -16), 
        color = vec(0.6, 0.3, 0.2),
        axis = vec(0, 0, 1),
        texture=dict(file="/da/vp/img/wood.jpg")
    )
    ball_pos_box = label(
        pos=vec(400, 80, -50),
        text= 'Position:\nX:' + '\nY:' + '\nZ:', 
        height=30, 
        border=10, 
        font='monospace', 
        color = color.white
    )
    init_value_box = label(
        pos=vec(470, 200, -50),
        text= 'Initial values:\n' + 'Angle:' + '\nHeight:'+ '\nSpeed:', 
        height=30, 
        border=10, 
        font='monospace', 
        color = color.white
    ) 
    marker = box(
        length = 20, 
        width = 152.5, 
        height = 2, 
        pos = vec(-127, 0.3, 0),
        color = color.yellow
    )
    marker.visible = False
    axisInit()
    net_init()
  
def time_delay(): 
    global is_running
    is_running = False 
    playAudio('Go.wav')
      
  
def table_tennis_motion(data):
    global is_running, ball_pos_box, ball_touch, height, angle, speed
    speed = data[0]
    angle = data[1]
    height = data[2]
    ball = sphere(pos = vec(-115, height, 10), radius = 2, color = color.orange)
    ball.velocity = vector(speed * sin(angle), -221, 0)
    g = 980 
    dt = 0.001
    air_drag_coe = 2.5
    a = vector(0, -g, 0) 
    ball_touch = 0
    frame_count = 0
    paddle.pos.x = -117
    grip.pos.x =  -117
    def jump(): 
        global is_running, frame_count, ball_touch, ball, speed, net, marker       
        ball.pos = ball.pos + ball.velocity * dt 
        if ball.pos.y < 3 and ball.velocity.y <= 0:
            ball.velocity.y = - ball.velocity.y
            ball_touch += 1
            playAudio('chord.wav')
        else:
            if ball_touch >= 2:
                ball.velocity = ball.velocity + a * dt 
            else:
                ball.velocity = ball.velocity + a * dt - air_drag_coe * ball.velocity * dt
        for i in range(0, 7):
            if (ball.pos.x <= (-117+i*20) and ball.pos.x > (-137+i*20)) and ball.pos.y < 3.5 :
                marker.pos = vec(-127+i*20, 0.3, 0)
                marker.visible = True

        if (ball.pos.x <= 0 and ball.pos.x > -17) and ball.pos.y < 3 :
            marker.pos = vec(-8.5, 0.3, 0)
            marker.length = 17
            marker.visible = True
        if (ball.pos.x <= 17 and ball.pos.x > 0) and ball.pos.y < 3:
            marker.pos = vec(8.5, 0.3, 0)
            marker.length = 17
            marker.visible = True
        for k in range(0, 7):
            if (ball.pos.x <= (37+k*20) and ball.pos.x > (17+k*20)) and ball.pos.y < 3.5 :
                marker.pos = vec(27+k*20, 0.3, 0)
                marker.visible = True

        if ball.pos.x >= 137 or ball_touch >= 10 or ball.pos.x < -137 or (ball.pos.x > -3 and ball.pos.x < 3 and ball.pos.y < 10.25 and ball.pos.z < 100):            
            ball.visible = False  
            speed = 0
            setTimeout(time_delay,2000)
            marker.visible = False
            marker.length = 20
            return
        else:
            rate(1000, jump)
        if frame_count % 10 == 0:
            ball_pos_box.text = 'Position:\nX:' + str(round(ball.pos.x,1)) + '\nY:' + str(round(ball.pos.y,1)) + '\nZ:' + str(ball.pos.z,1)
        frame_count += 1
    jump()

def Speed(data):
    global is_running, speed, angle, height
    if not is_running and data != None:
        speed = data[0]
        console.log("speed:"+ speed)
        is_running = True
        table_tennis_motion([speed, angle , height])
        update()

def Angle(data):	
    global angle
    if data != None and data[0] >= 0 and data[0] <= 180:
        angle = data[0]* Math.PI/180
        update()

def Height(data):
    global height
    if data != None and data[0] > 0:
        height = data[0]
        update()

def setup():
    table_tennis_init()
    profile = {
        "dm_name": "TableTennis",
        "odf_list": [Speed, Angle, Height]
    }
    dai(profile)

def update():
    global init_value_box, height, angle, speed
    init_value_box.text = 'Initial values:\n' + 'Angle:' + str(round(angle*180/Math.PI,1)) + '\nHeight:' + str(round(height,1)) + '\nSpeed:' + str(round(speed,1))
    paddle.pos.y = height
    paddle.axis = vec( -1* sin(angle), 1 * cos(angle), 0)
    grip.pos.y =  height
    grip.length = 20

setup()




