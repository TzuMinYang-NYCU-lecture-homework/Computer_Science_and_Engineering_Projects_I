g = 9.8             			#���O�[�t�� 9.8 m/s^2
L = 4.9             			#�O����
size = 0.1          			#�y�b�| 0.1m
#th = 30 * pi / 180  		#�O�׫� 30��
dt = 0.001
freq = 1000

def scene_init():
    global ball, scene, th, board
    scene = display(width=900, height=900, background=vector(0.5,0.5,0))
    scene.center = vector(0,(L-2*size)/2,0)					#�]�w���������I
    scene.forward = vector(-0.125, 0.1, -1)							#�]�w����������V
    floor = box(length=10, height=0.001, width=1)                #�e�a�O
    floor.pos = vector(-L/2, -0.1, 0)
    floor.axis=vector(-L,0,0)
    ball = sphere(radius = size, color = color.black)
    board = box(length=L, height=0.001, width=1)				#�e�תO
    ball.visible = False
    th = 0

def setPos(data):
    global board, ball, th
    th = data*pi / 180  		#�O�׫�
    board.pos = vector(-L*cos(th)/2 - size*sin(th) , L*sin(th)/2-size*cos(th), 0)	#�תO������
    board.axis=vector(-L*cos(th), L*sin(th),0)					#�תO����V	
    
    if th!=0:
        ball.visible = True
        if data<=20:
            ball = sphere(radius = size, color = color.black)
        elif data<=40:
            ball = sphere(radius = size, color = color.blue)
        elif data<=60:
            ball = sphere(radius = size, color = color.yellow)
        elif data<=80:
            ball = sphere(radius = size, color = color.orange)
        elif data==90:
            ball = sphere(radius = size, color = color.red)
        ball.pos = vector(-L*cos(th), L*sin(th), 0)
        ball.v = vector(0.0, 0.0, 0.0)                       

def resetScene():
    global scene, ball
    scene.background = vector(0.5, 0.5, 0)
    ball.pos = vector(-L*cos(th), L*sin(th), 0) 
    ball.v = vector(0.0, 0.0, 0.0)

def Angle(data):
    if data != None:
        setPos(data[0])

def setup():
    scene_init()
    profile = {
        'dm_name':'Ball-Slide1',
        'odf_list':[Angle]	
    }
    dai(profile)

setup()


while True:
    rate(freq)
    
    if ball.pos.x < 0.0:
        a = vector(g * sin(th) * cos(th), - g * sin(th) * sin(th), 0)     #�[�t��
        ball.v = ball.v + a * dt
        ball.pos = ball.pos + ball.v * dt
    else :
        scene.background = vector(0,0,0)
        resetScene()
        ball.visible = False
        board.visible = False
