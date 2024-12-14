import socketio
from icecream import ic

# Crear una instancia del cliente Socket.IO
sio = socketio.Client()


# Evento de conexión
@sio.event
def connect():
    ic("Conectado al servidor")
    sio.emit("mi_evento", {"mensaje": "Hola, servidor!"})


# Evento de desconexión
@sio.event
def disconnect():
    ic("Desconectado del servidor")


# Evento personalizado
@sio.on("respuesta")
def on_respuesta(data):
    ic(f"Respuesta del servidor: {data['data']}")


# Conectarse al servidor
sio.connect("http://localhost:5000")
sio.wait()
