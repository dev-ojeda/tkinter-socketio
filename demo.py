import threading
import tkinter as tk
from socketio import Client
from icecream import ic

# Configurar el cliente Socket.IO
sio = Client()
running_cola = False


def manipula_eventos() -> None:
    # Conectar al servidor Flask en el namespace /chat
    @sio.event
    def connect():
        ic("Conectado al servidor")
        sio.emit("mi_evento", {"mensaje": "Hola, servidor!"})
        update_log("Conectado al servidor")

    # Evento de desconexión
    @sio.event
    def disconnect() -> None:
        ic("Desconectado del namespace")
        update_log("Desconectado del servidor")

    @sio.on("message_cliente", namespace="/chat")
    def on_client_message(data) -> None:
        ic(f"Mensaje recibido del Cliente: {data}")
        update_log(f"{data["username"]}: {data["msg"]}")

    @sio.on("respuesta")
    def on_respuesta(data) -> None:
        ic(f"Respuesta del servidor: {data}")
        update_log(f"Servidor: {data}")


def connect_to_server() -> None:
    # sio.connect("http://localhost:5000")
    sio.connect("http://localhost:5000", namespaces=["/chat"])
    # sio.wait()


def send_message(namespace) -> None:
    mensaje = entry_message.get()
    username = "DESKTOP"
    if mensaje:
        ic(namespace)
        chat_mesage = {"username": username, "msg": mensaje}
        # sio.connect("http://localhost:5000", namespaces=["/chat"])
        if namespace == "/":
            sio.emit("mi_evento", chat_mesage)
            update_log(f"DESKTOP: {mensaje}")
            entry_message.delete(0, tk.END)
        elif namespace == "/chat":
            sio.emit("mensaje", chat_mesage, namespace="/chat")
            update_log(f"DESKTOP: {mensaje}")
            entry_message.delete(0, tk.END)
        else:
            ic("error")


def update_log(message) -> None:
    text_log.insert(tk.END, message + "\n")
    text_log.see(tk.END)


# Inicia la conexión en un hilo separado
def start_consuming(running) -> None:
    global running_cola
    if not running:
        running_cola = True
        thread = threading.Thread(target=manipula_eventos)
        thread.daemon = True
        thread.start()
    else:
        stop_consuming()


def stop_consuming() -> None:
    """Detiene el consumo."""
    global running_cola
    running_cola = False


# Crear la interfaz Tkinter
root = tk.Tk()
root.title("Chat con Flask-SocketIO")

frame = tk.Frame(root)
frame.pack(pady=10)

text_log = tk.Text(frame, height=15, width=50, state="normal")
text_log.pack()

entry_message = tk.Entry(frame, width=40)
entry_message.pack(side=tk.LEFT, padx=5)

btn_send = tk.Button(
    frame, text="Enviar", command=lambda: send_message(sio.connection_namespaces[0])
)
btn_send.pack(side=tk.LEFT)
# Conectar al servidor al iniciar la aplicación
start_consuming(running_cola)
connect_to_server()

root.protocol("WM_DELETE_WINDOW", lambda: (sio.disconnect(), root.destroy()))
root.mainloop()
