import machine
from ssd1306 import SSD1306_I2C

class ControladorOled:
    def __init__(self, __pin_scl, __pin_sda):
        self.__pin_scl = __pin_scl
        self.__pin_sda = __pin_sda
        self.__i2c = machine.SoftI2C(scl=machine.Pin(self.__pin_scl), sda=machine.Pin(self.__pin_sda))
        self.__display = SSD1306_I2C(128, 64, self.__i2c)

    def limpiar_pantalla(self):
        self.__display.fill(0)
        self.__display.show()

    def escribir_texto(self, texto, x, y):
        self.__display.text(texto, x, y)
        self.__display.show()