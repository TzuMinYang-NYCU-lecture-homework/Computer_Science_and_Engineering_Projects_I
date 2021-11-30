
#  1. 變數設定
size = 0.2                # 球的半徑 0.2 m
g = vector(0,-9.8,0)     # 重力加速度

dt = 0.05
freq = 1000
scl = 0

#  2. 畫面設定 
def scene_init():
    global c1, c2
    scene = display(width = 960, height = 600, center = vector(15,0,0), background=(0.5,0.6,0.5))
    c1 = curve(color = color.yellow)
    c2 = curve(color = color.red)
    floor = box(pos=vector(15,-0.05,0), length = 70, height = 1, width=70)

#  3. 初始條件
def balljump(data):
    global c1, c2, ball, t, scl
    c1.visible = False
    c2.visible = False
    c1 = curve(color = color.yellow)
    c2 = curve(color = color.red)
    t = 0
    scl = data

def Scale(data):
    if data != None:
        balljump(data[0])

def setup():
    scene_init()
    profile = {
        'dm_name':'3DMotion2',
        'odf_list':[Scale]
    }
    dai(profile)
setup()

t = 0

while True:
    rate(freq)

    if t < 100:
        x = (2+cos(16*t))*cos(t)
        y = (2+cos(16*t))*sin(t)
        z = sin(16*t)
        c1.append(pos = [vector(2*x,t*0.5+0.5,2*y)], radius = 0.01*scl)
        c2.append(pos = [vector(x*scl*0.1+20,t*scl*0.03+0.5,y*scl*0.1)], radius = 0.1)
    t = t + dt
            
