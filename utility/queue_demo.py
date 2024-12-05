import tkinter as tk
from tkinter import ttk
from queue import Queue
from threading import Thread
import time


def producer(queue, log_widget_producer):
    """Produce tareas y las agrega a la cola."""
    for i in range(10):  # Crear 10 tareas
        task = f"Tarea {i + 1}"
        queue.put(task)
        log_widget_producer.insert(
            tk.END, f"Produciendo: {task}\n"
        )  # Actualizar la GUI
        log_widget_producer.see(tk.END)  # Scroll automático
        time.sleep(1)  # Simula el tiempo entre generación de tareas


def consumer(queue, log_widget_consumer):
    """Consume tareas de la cola y las procesa."""
    while True:
        task = queue.get()  # Obtener una tarea de la cola
        if task is None:  # Finalizar si se recibe None
            break
        print(f"Consumiendo: {task}")
        log_widget_consumer.insert(tk.END, f"Procesando {task}\n")  # Actualizar la GUI
        log_widget_consumer.see(tk.END)  # Scroll automático
        time.sleep(2)  # Simula tiempo de procesamiento
        log_widget_consumer.insert(tk.END, f"Finalizado {task}\n")
        log_widget_consumer.see(tk.END)
        queue.task_done()


def start_production(queue, log_widget_producer):
    """Inicia el productor en un hilo separado."""
    Thread(target=producer, args=(queue, log_widget_producer), daemon=True).start()


def start_consumption(queue, log_widget_consumer):
    """Inicia el consumidor en un hilo separado."""
    Thread(target=consumer, args=(queue, log_widget_consumer), daemon=True).start()


def main():
    # Configuración de la ventana principal
    root = tk.Tk()
    root.title("Producer-Consumer en Tkinter")
    root.geometry("400x300")

    # Cola compartida entre productor y consumidor
    task_queue = Queue()

    # Widgets de la GUI
    log_widget_producer = tk.Text(root, height=15, width=50)
    log_widget_producer.pack(pady=10, padx=10)

    # Widgets de la GUI
    log_widget_consumer = tk.Text(root, height=15, width=50)
    log_widget_consumer.pack(pady=10, padx=10)

    start_producer_btn = ttk.Button(
        root,
        text="Iniciar Productor",
        command=lambda: start_production(task_queue, log_widget_producer),
    )
    start_producer_btn.pack(pady=5)

    start_consumer_btn = ttk.Button(
        root,
        text="Iniciar Consumidor",
        command=lambda: start_consumption(task_queue, log_widget_consumer),
    )
    start_consumer_btn.pack(pady=5)

    # Ejecutar el loop principal de Tkinter
    root.mainloop()


if __name__ == "__main__":
    main()
