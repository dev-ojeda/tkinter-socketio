import threading
import time


# Función que ejecutará el thread
def tarea_concurrente(id_hilo, lock):
    for i in range(5):
        with lock:  # Bloquea el acceso para proteger la sección crítica
            print(f"Hilo {id_hilo} está ejecutando la iteración {i}")
        time.sleep(1)  # Simula un proceso que toma tiempo


# Crear un Lock para sincronización
lock = threading.Lock()

# Crear y lanzar múltiples threads
hilos = []
for id_hilo in range(3):  # 3 threads simultáneos
    hilo = threading.Thread(target=tarea_concurrente, args=(id_hilo, lock))
    hilos.append(hilo)
    hilo.start()

# Esperar a que todos los threads terminen
for hilo in hilos:
    hilo.join()

print("Todos los hilos han terminado.")
