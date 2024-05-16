# this program visualizes activities with pyglet

import activity_recognizer as activity
import pyglet
from DIPPID import SensorUDP



#connect phone
PORT = 5700
sensor = SensorUDP(PORT)

#sensor data
acc_x = acc_y = acc_z = 0
gyro_x = gyro_y = gyro_z = 0


window_width = 1280
window_height = 720
window = pyglet.window.Window(window_width, window_height)
pyglet.gl.glClearColor(1, 1, 1, 1) 

#load images
img_running = pyglet.image.load('img/running_1.png')
running = pyglet.sprite.Sprite(img_running)
running.scale = 0.5
img_rowing = pyglet.image.load('img/rowing_1.png')
rowing = pyglet.sprite.Sprite(img_rowing)
rowing.scale = 0.5
img_lifting = pyglet.image.load('img/lifting_1.png')
lifting = pyglet.sprite.Sprite(img_lifting)
lifting.scale = 0.5
img_jumpingjack = pyglet.image.load('img/jumpingjack_1.png')
jumpingjack = pyglet.sprite.Sprite(img_jumpingjack)
jumpingjack.scale = 0.5


#get live data
def handle_accelerometer(data): 
    global acc_x, acc_y, acc_z
    acc_x = data.get("x")
    acc_y = data.get("y")
    acc_z = data.get("z")

def handle_gyroscope(data):
    global gyro_x, gyro_y, gyro_z
    gyro_x = data.get("x")
    gyro_y = data.get("y")
    gyro_z = data.get("z")

def get_data():
    return[acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z]

#classifier erstellen
classifier = activity.model()

@window.event
def on_draw():
    window.clear()
    live_data = get_data()
    fitness_activity = activity.estimated(classifier, live_data)
    match fitness_activity:
        case 'running':
            running.draw()
        case 'rowing':
            rowing.draw()
        case 'lifting':
            lifting.draw()
        case 'jumpingjacks':
            jumpingjack.draw()

sensor.register_callback('gyroscope', handle_accelerometer)
sensor.register_callback('gyroscope', handle_gyroscope)

pyglet.app.run()




