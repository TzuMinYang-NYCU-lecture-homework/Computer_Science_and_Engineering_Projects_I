
g = 9.8
size = 0.25
freq = 1000
dt = 0.002
drag_coef = 0.42
drag_power = 1.0

def scene_init():
    global ball
    scene = display(title='bouncing projectile',center = vector(0,5,0),width = 1200 ,height = 800, background = vector(0.5,0.5,0))
    floor = box(length = 100,height = 0.01 , weight = 4 , color = color.blue)
    ball = sphere(radius = size , color = color.red ,make_trail = false)
    ball.velocity = vector(0.0,0.0,0.0)
    ball.visible = False

def fall(i):
    global ball, spd
    spd = i
    ball.velocity = vector(spd,0.0,0.0)
    ball.pos = vector(-50.0,10.0,0.0)
    ball.visible = True;

def Command(data):
    if data != None:
        fall(data[0])

def setup():
    scene_init()
    profile = {
        'dm_name':'AirResistance2',
        'odf_list':[Command]
    }
    dai(profile)

setup()

while True:
    rate(freq)

    d = drag_coef * (ball.velocity^drag_power)
    if ball.pos.x < 50.0:
        if ball.velocity.y < 0 :
            ball.velocity.y += (d * dt * 3.6)
        else:
            ball.velocity.y -= (d * dt * 3.6)
        if ball.velocity.x > 0:
            ball.velocity.x -= (d * dt * 0.47)
        ball.pos = ball.pos + ball.velocity * dt

        if ball.pos.y < size and ball.velocity.y < 0:
            ball.velocity.y = - ball.velocity.y
        else:
            ball.velocity.y = ball.velocity.y - (g * dt)

