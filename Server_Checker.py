import requests
import os


class ConexionApi: 
    def __init__(self, key, api):
        self.__ip = key
        self.__api = api
        self.__url_api = f'{self.__api}{self.__ip}'
        self.__respuesta = requests.get(self.__url_api) # Se conecta a la API
        if self.__respuesta.status_code == 200:
            print(f'Conexión Establecida con la API: ({self.__respuesta.status_code})')
        else:
            print(f'Error al conectar con la API: ({self.__respuesta.status_code})')

    def __repr__(self) -> str:
        return f'Api = {self.__api}{{ip}}, Ip = {self.__ip}, Conexión = {self.__url_api}, Respuesta = {self.__respuesta}'

    @property
    def respuesta(self) -> requests:
        return self.__respuesta


class ServerDatos:
    def __init__(self, conexion_api):
        self.__respuesta = conexion_api.respuesta
        if self.__respuesta.status_code == 200: # Se ejecuta si tiene contenido
            self.__respuesta_json = self.__respuesta.json()

    def __repr__(self) -> str:
        return f'STATUS: {self.__respuesta_json["is_online"]}, UPDATE: {self.__respuesta_json["update_date"]}, LAST_ONLINE: {self.__respuesta_json["last_online"]}, PLAYERS: {self.__respuesta_json["players"]}'

    @property
    def serverStatus(self) -> bool:
        if self.__respuesta_json['is_online'] == '1':
            return True
        else:
            return False

    @property
    def serverUltimaActualizacion(self) -> str:
        return str(self.__respuesta_json['update_date'])

    @property
    def serverVersion(self) -> str:
        return str(self.__respuesta_json['version'])

    @property
    def serverUltimaVezOnline(self) -> str:
        return str(self.__respuesta_json['last_online'])

    @property
    def serverJugadores(self) -> int:
        return int(self.__respuesta_json['players'])

def refrescar(key, api):
    contenido_api = ConexionApi(key, api)
    server = ServerDatos(contenido_api)
    return server


