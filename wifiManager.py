import network
import utime

class WiFiManager:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)
        
    def conectar(self):
        self.wlan.active(True)
        try:
            if not self.wlan.isconnected():
                self.wlan.connect(self.ssid, self.password)
                for _ in range(10):
                    if self.wlan.isconnected():
                        break
                    utime.sleep(1)
            if not self.wlan.isconnected():
                raise Exception('Tiempo de conexión agotado')
        except Exception as e:
            print('Error en la conexión WiFi:', str(e))
    
    def esta_conectado(self):
        return self.wlan.isconnected()
