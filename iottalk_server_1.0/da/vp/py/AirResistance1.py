g=9.8
size = 0.25
freq = 1000
dt=0.005

def scene_init():
    global spd, drag_coeff, showinfo, pointer, rebounce_coeff, ball
    scene = display(title='Bouncing_Ball', width=1600, height=800, background=vector(0.5,0.5,0.0), center=vector(0,5,0))
    floor = box(length=30, height=0.01, width=4, color=color.blue,pos=vector(0,0,0))

    spd = vector(2,0,0)
    BALL = sphere(pos=vector(-15,5.0,0.0),radius=size, color=color.red)
    ball = sphere(pos=vector(-15,5.0,0.0),radius=size, color=color.red)
    pointer = arrow(pos=vector(-15,5.0,0.0),axis=spd,shaftwidth=0.2,color=color.black)
    scene.range=18
    camera_x1=0.0
    camera_x2=0.0
    scene.forward=vector(camera_x1,camera_x2,-1)
    drag_coeff = 0.0
    rebounce_coeff = 1.0
    info = "Velocity = ("+str(spd.x)+","+str(spd.y)+")\ndrag coeff = "+str(drag_coeff)+"\nrebouncing coeff = "+str(rebounce_coeff)+"\ndata = "+str(data)
    showinfo=label(pos=vector(0,12,0), text=info,background=vector(0.2,0.2,0.2),height = 10)

def balllaunch(i):
  global spd, drag_coeff, rebounce_coeff, check, ball, showinfo, pointer, data
  data = int(i)
  if data==0:
    ball.pos = vector(-15,5.0,0.0)
    spd = vector(2,0,0)
    drag_coeff = 0.0
    rebounce_coeff = 1.0
  elif data==1:
    if rebounce_coeff>0.05:
      rebounce_coeff=rebounce_coeff-0.1
  elif data==2:
    spd.y=spd.y+1;
  elif data==3:
    if rebounce_coeff<1.00:
      rebounce_coeff=rebounce_coeff+0.1
  elif data==4:
    if(spd.x>0):
      spd.x=spd.x-1
  elif data==6:
    spd.x=spd.x+1
  elif data==7:
    if drag_coeff>0.2:
      drag_coeff=drag_coeff-0.2
  elif data==8:
    spd.y=spd.y-1
  elif data==9:
    drag_coeff=drag_coeff+0.2
  c_x = spd.x
  c_y = spd.y
  ball.velocity = vector(c_x,c_y,0)
  info = "Velocity = ("+str(spd.x)+","+str(spd.y)+")\ndrag coeff = "+str(drag_coeff)+"\nrebouncing coeff = "+str(rebounce_coeff)+"\ndata = "+str(data)
  showinfo.text=info
  pointer.axis = spd
  check = False

def Command(i):
  if i != None:
    balllaunch(i[0])

def setup():
  scene_init()
  profile = {
    'dm_name':'AirResistance1',
    'odf_list':[Command]
  }
  dai(profile)

setup()
#csmRegister(profile)
#rate(1,progress)
data = 0
check = False

while True:
  rate(freq)
    
  if ball.pos.x >= 15 and check == True:
    ball.visible=False
  else:
    ball.visible=True
  if data > 0 and data < 11:		
    ball.pos = ball.pos + ball.velocity * dt
    if ball.pos.y<size and ball.velocity.y>-0.1:
      check = True
      console.log("FUCK")
      ball.pos.y = 0
    if ball.pos.y<size and ball.velocity.y<0:
      ball.velocity.y = -1*rebounce_coeff*ball.velocity.y
    elif ball.velocity!=0:
      ball.velocity.y = ball.velocity.y - g * dt - drag_coeff * ball.velocity.y/10 * dt
      ball.velocity.x = ball.velocity.x - drag_coeff * ball.velocity.x/10 * dt
    if check == True:
      ball.visible = False
