import utime
from controladorLed import ControladorLed
from controladorSensor import ControladorSensor
from controladorOled import ControladorOled
from wifiManager import WiFiManager
from connector import SolicitudHttp

UMBRAL_POCA_LUZ = 2000

def main():
    print("Programa de control de luz iniciado")

    SSID = "Wokwi-GUEST"
    PASSWORD = ""
    url_servidor = 'https://serverwokwi.onrender.com'

    wifi_manager = WiFiManager(SSID, PASSWORD)
    led_delasota = ControladorLed(11)
    sensor_de_nivel_luz_schiaretti = ControladorSensor(14)
    pantalla_oled = ControladorOled(5, 4)
    cliente = SolicitudHttp(url_servidor)
    estado_led = False 
    
    # Intentar conectar al WiFi
    wifi_manager.conectar()
    
    if wifi_manager.esta_conectado():
        print("Conexión WiFi exitosa")
        pantalla_oled.limpiar_pantalla()
        pantalla_oled.escribir_texto('WiFi conectado', 0, 0)
    else:
        print("No se pudo conectar al WiFi")
        pantalla_oled.limpiar_pantalla()
        pantalla_oled.escribir_texto('WiFi no conectado', 0, 0)
    
    while True:
        try:
            utime.sleep(0.5)
            valor_sensor = sensor_de_nivel_luz_schiaretti.mostrar_valor_actual()
            
            if valor_sensor < UMBRAL_POCA_LUZ and not estado_led:
                pantalla_oled.limpiar_pantalla()
                pantalla_oled.escribir_texto('hay poca luz', 0, 0)
                pantalla_oled.escribir_texto('se encendera', 0, 10)
                pantalla_oled.escribir_texto('el led y se', 0, 20)
                pantalla_oled.escribir_texto('guardara en bdd', 0, 30)

                estado_led = True
                if cliente.enviar_estado_led(estado_led):
                    pantalla_oled.limpiar_pantalla()
                    pantalla_oled.escribir_texto('Estado LED', 0, 0)
                    pantalla_oled.escribir_texto('encendido', 0, 10)
                    pantalla_oled.escribir_texto('guardado', 0, 20)
                    pantalla_oled.escribir_texto('exitosamente', 0, 30)
                
                led_delasota.encender_led()

            elif valor_sensor >= UMBRAL_POCA_LUZ and estado_led:
                pantalla_oled.limpiar_pantalla()
                pantalla_oled.escribir_texto('hay suficiente luz', 0, 0)
                pantalla_oled.escribir_texto('se encendera', 0, 10)
                pantalla_oled.escribir_texto('el led y se', 0, 20)
                pantalla_oled.escribir_texto('guardara en bdd', 0, 30)
                print('Ya hay suficiente luz, se apagará el led!')


                estado_led = False
                if cliente.enviar_estado_led(estado_led):
                    pantalla_oled.limpiar_pantalla()
                    pantalla_oled.escribir_texto('Estado LED', 0, 0)
                    pantalla_oled.escribir_texto('apagado', 0, 10)
                    pantalla_oled.escribir_texto('guardado', 0, 20)
                    pantalla_oled.escribir_texto('exitosamente', 0, 30)
                
                led_delasota.apagar_led()

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()