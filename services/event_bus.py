import json
import re
import tkinter as tk
from tkinter import ttk
import requests
import threading
import time

import socketio


class EventEmitter:
    def __init__(self):
        # Diccionario para almacenar eventos y sus manejadores
        self._event_handlers = {}

    def on(self, event_name, handler):
        """Registra un manejador para un evento específico."""
        if event_name not in self._event_handlers:
            self._event_handlers[event_name] = []
        self._event_handlers[event_name].append(handler)

    def off(self, event_name, handler=None):
        """Desregistra un manejador para un evento específico."""
        if event_name in self._event_handlers:
            if handler:
                self._event_handlers[event_name].remove(handler)
                if not self._event_handlers[event_name]:
                    del self._event_handlers[event_name]
            else:
                del self._event_handlers[event_name]

    def emit(self, event_name, *args, **kwargs):
        """Llama a todos los manejadores registrados para un evento específico."""
        if event_name in self._event_handlers:
            for handler in self._event_handlers[event_name]:
                handler(*args, **kwargs)

    def once(self, event_name, handler):
        """Registra un manejador que se ejecutará solo una vez."""

        def wrapper(*args, **kwargs):
            handler(*args, **kwargs)
            self.off(event_name, wrapper)

        self.on(event_name, wrapper)


# Servicio que crea empleados
class EmpleadoService:
    def __init__(self, event_bus, event_name, name_funcion):
        self.event_bus = event_bus
        self.event_name = event_name
        self.name_funcion = name_funcion
        self.event_bus.on(self.event_name, self.name_funcion)

    def eliminar_empleado(self, empleados):
        print(f"Empleado eliminado: {empleados}")
        # Emitir el evento EliminarEmpleado
        self.event_bus.emit("EliminarEmpleado", empleados)


# URL del endpoint para consumir mensajes
# QUEUE_API_URL = "http://127.0.0.1:5000/delete/entry"


# Classe para o Consumer (Tkinter)
class ConsumerApp(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        # Agrupar claves por valor
        self.valores_claves = set()
        # Etiqueta
        self.label = tk.Label(
            self.master.frame_tree_empleados,
            text="Mensajes de la Cola",
            font=("Arial", 16),
        )
        self.label.grid(pady=10)

        # Caja de texto con scroll
        self.text_area = tk.Text(
            self.master.frame_tree_empleados, wrap="word", width=40, height=10
        )
        # Scrollbar vertical
        scrollbar_v = ttk.Scrollbar(
            self.master.frame_tree_empleados,
            orient="vertical",
            command=self.text_area.yview,
        )
        scrollbar_v.grid(row=5, column=1, sticky="ns")

        # Scrollbar horizontal
        # scrollbar_h = ttk.Scrollbar(
        #     self.master.frame_tree_empleados,
        #     orient="horizontal",
        #     command=self.text_area.xview,
        # )
        # scrollbar_h.grid(row=6, column=1, sticky="ew")

        self.text_area.configure(yscrollcommand=scrollbar_v.set)
        self.text_area.grid(row=5, column=0, sticky="nsew")

        # Botón para iniciar el consumo
        self.start_button = ttk.Button(
            self.master.frame_tree_empleados,
            text="Iniciar Consumo",
            image=self.master.ejecutar,
            compound="left",
            command=self.start_consuming,
        )
        self.start_button.grid(pady=5)

        # Botón para iniciar el consumo
        self.delete_button = ttk.Button(
            self.master.frame_tree_empleados,
            text="Eliminar Consumo",
            command=self.master.eliminar_empleado_consumido,
        )
        self.delete_button.grid(pady=5)

        # Botón para detener el consumo
        self.stop_button = ttk.Button(
            self.master.frame_tree_empleados,
            text="Detener Consumo",
            image=self.master.ejecutar,
            compound="left",
            command=self.stop_consuming,
        )
        self.stop_button.grid(pady=5)

        # Estado del hilo de consumo
        self.running_cola = False

    def fetch_message(self):
        # QUEUE_API_URL = "http://127.0.0.1:5000/delete/entry"
        """Obtiene un mensaje de la cola usando la API."""
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        try:
            response = requests.get(
                "http://127.0.0.1:5000/delete/entry", headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    return data.get("message")
                else:
                    return "La cola está vacía."
            else:
                return f"Error en la API: {response.status_code}"
        except Exception as e:
            return f"Error al conectar: {e}"

    def consume_messages(self):
        """Consume mensajes de la cola periódicamente."""
        # Expresión regular para encontrar nombres con comillas simples
        while self.running_cola:
            self.message = self.fetch_message()
            # Reemplazar comillas simples por dobles solo en claves y valores no anidados
            json_data = re.sub(r"(?<!\\)'", '"', self.message)
            # formateado_all = json.dumps(formateado, indent=2)
            # self.almacenar_mensajes(json_data)
            self.text_area.insert(tk.END, json_data + "\n")
            self.text_area.see(tk.END)  # Desplaza al final
            time.sleep(2)  # Intervalo de consumo

    def almacenar_mensajes(self, data):
        texto = 'D"'
        indice = 23
        nuevo_caracter = "'"
        nueva_cadena = ""
        try:
            if re.search(texto, data):
                print(f"'{texto}' encontrado.")
                nueva_cadena = data[:indice] + nuevo_caracter + data[indice + 1 :]
                print(nueva_cadena)
            else:
                print(f"'{texto}' no encontrado.")
                nueva_cadena = data
        except ValueError:
            print(f"'{texto}' no encontrado.")

        json_objeto = json.loads(nueva_cadena)
        [
            self.valores_claves.add((clave, value))
            for clave, value in dict(json_objeto).items()
            if str(clave) == "id"
        ]

    def start_consuming(self):
        """Inicia el consumo en un hilo separado."""
        print(self.running_cola)
        if not self.running_cola:
            self.running_cola = True
            self.thread = threading.Thread(target=self.consume_messages)
            self.thread.daemon = True
            self.thread.start()

    def stop_consuming(self):
        """Detiene el consumo."""
        self.running_cola = False
        self.clear_area()

    def clear_area(self):
        self.text_area.delete("1.0", tk.END)


class SocketIOApp(ttk.Frame):
    """docstring for ClassName."""

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.sio = socketio.Client()
        self.add_chat = tk.Toplevel(self.master.menu_frame)
        self.add_chat.title("Chat")
        self.add_chat.geometry("500x400")
        self.chat_log = tk.Text(self.add_chat, state="normal", height=15, width=50)
        self.chat_log.pack(pady=10)
        self.message_entry = tk.Entry(self.add_chat, width=40)
        self.message_entry.pack(side=tk.LEFT, padx=10)

        self.send_button = tk.Button(
            self.add_chat, text="Enviar", command=self.send_message
        )
        self.send_button.pack(side=tk.RIGHT, padx=10)
        self.send_conectar = tk.Button(
            self.add_chat, text="Conectar", command=self.start_socketio
        )
        self.send_conectar.pack(fill="x", side="left", padx=10)
        self.consumir_evento()
        self.running = False

    def connect_to_server(self):
        try:
            self.sio.connect("http://127.0.0.1:5000")
            self.sio.wait()
            self.sio.emit("custom_pull", {"nombre": "SERVIDOR"})
            print("Conectado al servidor SocketIO.")
        except Exception as e:
            self.chat_log.insert(tk.END, f"Error al conectar: {e}\n")
            print(f"Error al conectar: {e}")

    def consumir_evento(self):
        # Evento de recepción de mensajes
        @self.sio.on("server_message")
        def on_server_message(data):
            message = data.get("message")
            username = data.get("username")
            self.chat_log.insert(tk.END, f"{username}: {message}\n")

    # Función para enviar mensajes al servidor
    def send_message(self):
        message = self.message_entry.get()
        username = "SERVIDOR"
        if message:
            self.sio.emit(
                "cliente_message",
                {"username": username, "message": message},
            )
            self.chat_log.insert(tk.END, f"SERVIDOR: {message}\n")
            self.message_entry.delete(0, tk.END)

    # Inicia la conexión en un hilo separado
    def start_socketio(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.connect_to_server)
            self.thread.daemon = True
            self.thread.start()

    def stop_consuming(self):
        """Detiene el consumo."""
        self.running = False
