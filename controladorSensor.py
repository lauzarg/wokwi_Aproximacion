from machine import Pin, ADC

class ControladorSensor:
    def __init__(self, __pinSensor):
        self.__pinSensor = __pinSensor
        self.__adc = ADC.ATTN_11DB
        self.__sensor = ADC(Pin(self.__pinSensor))

    def __configurar_ganancia(self):
        self.__sensor.atten(self.__adc)

    def mostrar_valor_actual(self):
        self.__configurar_ganancia()
        valor_actual = self.__sensor.read()
        return valor_actual


