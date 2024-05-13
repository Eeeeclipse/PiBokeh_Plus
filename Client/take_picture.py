from picamera2 import Picamera2, Preview
from pynput import keyboard

    
def take_picture():
    camera = Picamera2()
    camera_config = camera.create_preview_configuration({'size':(630, 420)})
    camera.configure(camera_config)
    camera.start_preview(Preview.QTGL)
    camera.start()
    
    with keyboard.Events() as events:
        event = events.get()
        if event is not None:
            img = camera.capture_array()[:,:,:3]
            camera.stop_preview()
    return img