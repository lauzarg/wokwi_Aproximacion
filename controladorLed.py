from machine import Pin

class ControladorLed:
    def __init__(self, pin):
        self.__pin = pin
        self.led = Pin(self.__pin, Pin.OUT)
    
    def encender_led(self): 
        self.led.value(1)
        
    def apagar_led(self):
        self.led.value(0)