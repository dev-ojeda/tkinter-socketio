import json
import sqlite3


class Database:
    def __init__(self, db_name):
        """Inicializa la conexión a la base de datos"""
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Conecta a la base de datos especificada en db_name"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print(f"Conectado a la base de datos {self.db_name}")
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def execute_query(self, query, params=()):
        """Ejecuta una consulta de escritura en la base de datos"""
        try:
            self.cursor.execute(query, params)
            self.cursor.connection.commit()
            print("Consulta ejecutada correctamente")
        except sqlite3.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            self.cursor.close()
            self.close()

    def execute_query_many(self, query, params=()):
        """Ejecuta una consulta de escritura en la base de datos"""
        try:
            self.cursor.executemany(query, params)
            self.cursor.connection.commit()
            print("Consulta ejecutada correctamente")
        except sqlite3.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            self.cursor.close()
            self.close()

    def fetch_query(self, query, params=()):
        """Ejecuta una consulta de lectura y retorna los resultados"""
        try:
            data = self.cursor.execute(query, params).fetchall()
            return data
        except sqlite3.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []
        finally:
            self.cursor.close()
            self.close()

    def fetch_query_json(self, query, params=()) -> bool:
        """Ejecuta una consulta de lectura y retorna los resultados"""
        # Archivo JSON de salida
        output_file = "resultados.json"
        try:
            self.cursor.execute(query, params)
            # Obtener los nombres de las columnas
            columnas = [descripcion[0] for descripcion in self.cursor.description]
            # Obtener los resultados de la consulta
            resultados = self.cursor.fetchall()
            # Convertir los resultados a una lista de diccionarios
            datos = [dict(zip(columnas, fila)) for fila in resultados]
            # Guardar los datos en un archivo JSON
            with open(output_file, "w", encoding="utf-8") as archivo_json:
                json.dump(datos, archivo_json, indent=4, ensure_ascii=False)
            print(f"Datos exportados exitosamente a {output_file}")
            return True
        except sqlite3.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return False
        finally:
            self.cursor.close()
            self.close()

    def fetch_query_to_dict(self, query, params=()) -> list[dict]:
        """Ejecuta una consulta de lectura y retorna los resultados"""
        try:
            self.cursor.execute(query, params)
            # Obtener los nombres de las columnas
            columnas = [descripcion[0] for descripcion in self.cursor.description]
            # Obtener los resultados de la consulta
            # Convertir los resultados a una lista de diccionarios
            datos = [dict(zip(columnas, fila)) for fila in self.cursor.fetchall()]

            return datos
        except sqlite3.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []
        finally:
            self.cursor.close()

    def close(self):
        """Cierra la conexión a la base de datos"""
        if self.connection:
            self.connection.close()
            print("Conexión a la base de datos cerrada")
