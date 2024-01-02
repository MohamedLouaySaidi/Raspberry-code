import time
import board
import adafruit_dht
import pyrebase
import random
from datetime import datetime
import RPi.GPIO as GPIO
import BlynkLib
import blynklib
from BlynkTimer import BlynkTimer
import picamera
from datetime import datetime
from time import sleep
import os
import videostream
import sys


config={
    "apiKey":"",
    "authDomain":"",
    "databaseURL" :"",
    "storageBucket":""
     }
firebase= pyrebase.initialize_app(config)
db=firebase.database()
storage = firebase.storage()
# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D17)
dhtDevice = adafruit_dht.DHT11(board.D17, use_pulseio=False)
#GPIO.setmode(GPIO.BOARD)
PIR_PIN=4
GPIO.setup(PIR_PIN,GPIO.IN)
SOUND_PIN=27
GPIO.setup(SOUND_PIN, GPIO.IN)


BLYNK_AUTH_TOKEN = ""
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)
timer = BlynkTimer()

@blynk.on("connected")
def blynk_connected():
    print("Hi, You have Connected to New Blynk2.0")
    print(".......................................................")
    print("................... By SME Dehradun ...................")
    time.sleep(2);




while True:
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )
        if temperature_c > 40 :
            blynk.log_event("high_temperature")
        data={
            "Temperature" : temperature_c,
            "Humidity" : humidity
            }
        db.child("Status").push(data)
        db.update(data)
        blynk.virtual_write(0, humidity,)
        blynk.virtual_write(1, temperature_c)
        print("Values sent to New Blynk Server!")
        
        print("sent to database")
        if GPIO.input(PIR_PIN):
            print("motion detected")
            now = datetime.now()
            dt=now.strftime("%d %m %Y %H:%M:%S")
            motion={
            "motion" :"motion detected",
            "time" : dt
            }
            db.child("historique motion").push(motion)
            db.update(motion)
            blynk.virtual_write(3, 1)
        else:
            blynk.virtual_write(3, 0)
            
        if GPIO.input(SOUND_PIN) :
            blynk.log_event("baby_crying")
            print('baby might be crying')
            camera = picamera.PiCamera()
            camera.resolution = (1024, 768)
            camera.rotation = 180
            now = datetime.now()
            dt=now.strftime("%d %m %Y %H:%M:%S")
            name= dt+"babycry.jpg"
            camera.capture(name)
            print(name+"saved")
            storage.child(name).put(name)
            print("Image sent")
            os.remove(name)
            print("File Removed")
            camera.close() 
            #db.reference('capture').get()
            #capture={
            #"capture" :0
            #}
            #db.update(capture)
        @blynk.on("V2")
        def v2_write_handler(value):
            if int(value[0])== 1 :
                camera = picamera.PiCamera()
                camera.resolution = (1024, 768)
                camera.rotation = 180
                now = datetime.now()
                dt=now.strftime("%d %m %Y %H:%M:%S")
                name= dt+".jpg"
                camera.capture(name)
                print(name+"saved")
                storage.child(name).put(name)
                print("Image sent")
                os.remove(name)
                print("File Removed")
                camera.close()
                blynk.log_event("capture_image")

        @blynk.on("V5")
        def v5_write_handler(value_vid):
            try:
                if int(value_vid[0])== 1 :
                    #subprocess.Popen([sys.executable, "/home/sylou/blynk-library-python/videostream.py"])
                    videostream.start_streaming()
                elif int(value_vid[0])== 0 :
                    print("Close")
                    #subprocess.Popen([sys.executable, "/home/sylou/blynk-library-python/videostream.py"]).terminate()
            except KeyboardInterrupt:
                print("Continue")
                videostream.end_streaming()
            
            
        blynk.run()
        timer.run()
        
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
    
    time.sleep(2.0)
