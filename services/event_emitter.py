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


# Uso del EventEmitter
emitter = EventEmitter()


# Manejadores de eventos
def on_data_received(data):
    print(f"Data recibida: {data}")


def on_data_processed(data):
    print(f"Data procesada: {data}")


# Registro de eventos
emitter.on("data_received", on_data_received)
emitter.on("data_processed", on_data_processed)

print(emitter._event_handlers)

# Emitir eventos
emitter.emit("data_received", {"id": 1, "value": "Hola, mundo"})
emitter.emit("data_processed", {"id": 1, "status": "Éxito"})

print(emitter._event_handlers)

# Usar el manejador 'once'
emitter.once(
    "one_time_event", lambda x: print(f"Este evento solo se ejecuta una vez: {x}")
)

print(emitter._event_handlers)

emitter.emit("one_time_event", "Primera ejecución")
emitter.emit("one_time_event", "Segunda ejecución (no debería ejecutarse)")
