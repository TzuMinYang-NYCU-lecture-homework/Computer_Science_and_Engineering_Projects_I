g=vector(0,-9.8,0)
freq = 1000
size = 0.2
yellow = vector(1, 1 ,0)
blue = vector(0, 0, 1)
red = vector(1, 0, 0)
green = vector(0, 1, 0)
orange = vector(1, 0.5, 0)
pink = vector(1, 0.5, 0.75)

def scene_init():
    global ty
    #scene = display(title='0216247_final_project', width=800, height=600, background=vector(0.5,0.6,0.5), center=vector(15,0,0))
    scene = display(width=800, height=600, background=vector(0.5,0.6,0.5), center=vector(15,0,0))
    gd1 = gdisplay(x=800, y=0, title='time VS Y',xtitle='t(s)',ytitle='y(m)',ymax=5,xmax=30)
    ty=gcurve(gdisplay=gd1,color=yellow )
    floor=box(pos=vector(15,-0.05,0),lenght=30,height=0.1,width=5)

def balljump(spd):
    global ball, dt, t
    t = 0
    if spd <=10:
       ball=sphere(radius=size,color=blue,make_trail=True)
       ball.pos=vector(0,size,0)
       ball.velocity=vector(2,spd,0)
       dt=0.001
    else if spd<=20:
       ball=sphere(radius=size,color=yellow,make_trail=True)
       ball.pos=vector(0,size,0)
       ball.velocity=vector(2,spd,0)
       dt=0.003
    else if spd <= 30:
       ball=sphere(radius=size,color=red,make_trail=True)
       ball.pos=vector(0,size,0)
       ball.velocity=vector(2,spd,0)
       dt=0.005
    else if spd <= 40:
       ball=sphere(radius=size,color=orange,make_trail=True)
       ball.pos=vector(0,size,0)
       ball.velocity=vector(2,spd,0)
       dt=0.007
    else if spd <= 45:
       ball=sphere(radius=size,color=green,make_trail=True)
       ball.pos=vector(0,size,0)
       ball.velocity=vector(2,spd,0)
       dt=0.009
    else if spd <= 60:
       ball=sphere(radius=size,color=pink,make_trail=True)
       ball.pos=vector(0,size,0)
       ball.velocity=vector(2,spd,0)
       dt=0.011
    else if spd == 0:
       ball.visible=False
       ball.make_trail=False


def Speed(data):
    if data!=None:
        #reset_flag = True
        balljump(data[0])

def setup():
    scene_init()
    profile={
        'dm_name':'3DMotion1',
        'odf_list':[Speed],
        }
    dai(profile)
setup()


t = 0

while True:
    rate(freq)
    #if t< 5:
    #    rate(1000,jump)
    ty.plot(pos=(t,ball.pos.x))
    t+=dt
    if ball.pos.y<=size :
        ball.velocity.y=abs(ball.velocity.y)
    ball.pos=ball.pos + ball.velocity * dt
    ball.velocity=ball.velocity + g * dt
