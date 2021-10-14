import RPi.GPIO as GPIO
import datetime
import time

init = False

GPIO.setmode(GPIO.BOARD) # Broadcom pin-numbering scheme

def get_last_watered():
    try:
        f = open("utolsoOntozes.txt", "r")
        return f.readline()
    except:
        return "NEVER!"
      
def get_status(pin = 8):
    GPIO.setup(pin, GPIO.IN) 
    return GPIO.input(pin)

def init_output(pin):
    GPIO.setup(pin, GPIO.OUT)   # Pin beállítása kimenetként
    GPIO.output(pin, GPIO.LOW)  # Pin értéke hamis
    GPIO.output(pin, GPIO.HIGH) # Pin értéke igaz
    
def auto_water(delay = 5, pump_pin = 7, water_sensor_pin = 8):
    consecutive_water_count = 0
    init_output(pump_pin)
    print("Here we go! Press CTRL+C to exit")
    try:
        while 1 and consecutive_water_count < 10:
            time.sleep(delay)
            wet = get_status(pin = water_sensor_pin) == 0
            # Szenzor lekérdezése után, ha nem nedves, szivattyú bekapcsolása
            if not wet:
                if consecutive_water_count < 5:
                    pump_on(pump_pin, 1)
                consecutive_water_count += 1
            else:
                consecutive_water_count = 0
    # Kilépés Ctrl+C-re, GPI felszabadítással
    except KeyboardInterrupt: 
        GPIO.cleanup() 

def pump_on(pump_pin = 7, delay = 1):
    init_output(pump_pin)
    f = open("utolsoOntozes.txt", "w")
    f.write("Utoljára öntözve {}".format(datetime.datetime.now())) # Aktuális öntözés bekönyvelése
    f.close()
    GPIO.output(pump_pin, GPIO.LOW)
    time.sleep(1)
    GPIO.output(pump_pin, GPIO.HIGH)
