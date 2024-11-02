import urequests
import json

class SolicitudHttp:
    def __init__(self, url_base):
        self.url_base = url_base
        self.url_agregar_datos = f"{url_base}/add_data"
        self.datos = {'led_status': False}

    def enviar_estado_led(self, estado_led):
        self.datos['led_status'] = estado_led
        encabezados = {'Content-Type': 'application/json'}
        try:
            respuesta = urequests.post(self.url_agregar_datos, data=json.dumps(self.datos), headers=encabezados)
            if respuesta.status_code in [200, 201]:
                estado = 'encendido' if estado_led else 'apagado'
                print(f'Estado del LED ({estado}) guardado exitosamente en la base de datos.')
                respuesta.close()
                return True
            else:
                print(f'Error al guardar el estado del LED en la base de datos. Código de respuesta: {respuesta.status_code}')
                respuesta.close()
                return False
        except Exception as e:
            print('Error al enviar la solicitud POST:', e)
            return False