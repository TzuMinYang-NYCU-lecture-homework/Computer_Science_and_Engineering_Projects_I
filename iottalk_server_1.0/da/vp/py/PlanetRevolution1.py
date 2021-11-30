#physic parameter
G = 6.673E-11
mass = {'earth': 5.97E24, 'mars':6.42E23, 'sun':1.99E30}   
d_at_perihelion = {'earth': 1.495E11, 'mars':2.279E11}      
v_at_perihelion = {'earth': 2.9783E4, 'mars':2.4077E4}     

#init
speed = 0

#progress parameter
freq = 6*24
# dt = 1.0/freq
dt = 60*60

def scene_init():
    global scene,planets,sun,earth,mars
    scene = display(width=1000, height=1000, background=vector(0,0,0))
    sun = sphere(pos=vector(0,0,0), 
                radius = 2.1E10, 
                color = color.yellow, 
                emissive=True, 
                shininess=0.8,
                texture = dict(file = textures.rock,bumpmap = bumpmaps.stucco))
    scene.lights = [local_light(pos=vector(0,0,0), color=color.white)]

    earth = sphere(pos = vector(d_at_perihelion['earth'],0,0),
                    radius = 9.5E9,
                    texture = dict(file = textures.earth,bumpmap = bumpmaps.stucco), 
                    make_trail = True, retain = 365 *24)
    earth.rotate(angle = pi/2, axis=vector(1, 0, 0))
    earth.m, earth.v = mass['earth'], vector(0, v_at_perihelion['earth'], 0)
    mars = sphere(pos = vector(d_at_perihelion['mars'],0,0), 
                    radius = 4.9E9,
                    texture = dict(file = textures.wood_old, bumpmap = bumpmaps.stucco), 
                    make_trail = True, 
                    retain = 700 * 24)
    mars.m, mars.v = mass['mars'], vector(0, v_at_perihelion['mars'], 0)
    sun.m = mass['sun']
    planets = [earth, mars]
    #L = label(pos = planet.pos,text = 'Speed', xoffset=20, yoffset=50, space=30, height=16, border=4, font='sans')

def a(s):
    return - norm(s.pos) * G * sun.m / mag2(s.pos) 
	

def addMass(ma):
    if ma < 16.5:
        sun.m = sun.m - 0.001 * ma * mass.sun
    else:
        sun.m = sun.m + 0.001 * ma * mass.sun
    # console.log('sun.m:',sun.m)
    # console.log('ma:',sun.m)

#label1 = label(pos=vec(0,5E9,0), text='Sun mass= ' + sun.m, xoffset=20, yoffset=50, space=30, height=16, border=4, font='sans')


# def handler(data):
#     rate(6*24,progress)
#     motion()
#     if data!= None:
#         addMass(data)

# def progress():
#     csmPull(df,handler)
# need to change progress into Speed() to let it move.
# the step is aproxmatily dai -> profile's func -> some update or draw function.
# a testing funciton for dai register
def Speed(data):
    global speed
    if data != None:
        speed = data[0]
        # addMass(speed)
    console.log('speed!:',speed)
    console.log('sun.m:',sun.m)
    console.log('ma:',sun.m)
def setup():
    # df = 'Speed'
    scene_init()
    profile ={
        'dm_name':'PlanetRevolution1',
        'odf_list':[Speed]
    }
    dai(profile)

setup()

# csmRegister(profile)
# rate(6*24,progress)

while True:
    # console.log("draw")
    rate(freq)
    #motion
    addMass(speed)
    for planet in planets:
        planet.v = planet.v + a(planet) * dt * 20
        planet.pos = planet.pos + planet.v * dt * 20
console.log("testwhile")