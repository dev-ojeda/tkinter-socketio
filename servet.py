import socketio
import eventlet
from icecream import ic

# Crear una instancia de Socket.IO (modo asíncrono por defecto)
sio = socketio.Server(cors_allowed_origins="*")  # Permitir todas las conexiones

# Crear una aplicación WSGI
app = socketio.WSGIApp(sio)


# Evento de conexión
@sio.event
def connect(sid, environ):
    ic(f"Cliente conectado: {sid}")
    sio.emit(
        "message", {"data": "¡Bienvenido al servidor!"}, to=sid
    )  # Enviar mensaje al cliente conectado


# Evento de desconexión
@sio.event
def disconnect(sid):
    ic(f"Cliente desconectado: {sid}")


# Evento personalizado
@sio.on("mi_evento")
def handle_mi_evento(sid, data):
    ic(f"Mensaje recibido de {sid}: {data}")
    # Responder al cliente
    sio.emit("respuesta", {"data": f"Recibido tu mensaje: {data['mensaje']}"}, to=sid)


def main():
    ic("Servidor Socket.IO ejecutándose en http://localhost:5000")
    eventlet.wsgi.server(eventlet.listen(("localhost", 5000)), app)


# Ejecutar el servidor
if __name__ == "__main__":
    main()
