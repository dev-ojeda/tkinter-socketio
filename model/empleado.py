import datetime
from tkinter import messagebox
from model.rol import Rol
from utility.conexion import Database


class Empleado(Rol):

    def __init__(self):
        self.connexion = Database("empleados.db")

    def empleado(
        self,
        rol_id,
        rol_nombre,
        id,
        nombre,
        email,
        salario,
        fecha_ingreso,
        data,
        cantidad,
    ):
        super().__init__(rol_id=rol_id, rol_nombre=rol_nombre)
        self.__id = int(id)
        self.__nombre = str(nombre)
        self.__rol_id = int(rol_id)
        self.__rol_nombre = str(rol_nombre)
        self.__email = str(email)
        self.__salario = float(salario)
        self.__fecha_ingreso = datetime(fecha_ingreso)
        self.__data = list(data)
        self.__cantidad = int(cantidad)

    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        self.__id = value

    @property
    def _nombre(self):
        return self.__nombre

    @_nombre.setter
    def _nombre(self, value):
        self.__nombre = value

    @property
    def _rol_id(self):
        return self.__rol_id

    @_rol_id.setter
    def _rol_id(self, value):
        self.__rol_id = value

    @property
    def _rol_nombre(self):
        return self.__rol_nombre

    @_rol_nombre.setter
    def _rol_nombre(self, value):
        self.__rol_nombre = value

    @property
    def _email(self):
        return self.__email

    @_email.setter
    def _email(self, value):
        self.__email = value

    @property
    def _salario(self):
        return self.__salario

    @_salario.setter
    def _salario(self, value):
        self.__salario = value

    @property
    def _fecha_ingreso(self):
        return self.__fecha_ingreso

    @_fecha_ingreso.setter
    def _fecha_ingreso(self, value):
        self.__fecha_ingreso = value

    @property
    def _data(self):
        return self.__data

    @_data.setter
    def _data(self, value):
        self.__data = value

    @property
    def _cantidad(self):
        return self.__cantidad

    @_cantidad.setter
    def _cantidad(self, value):
        self.__cantidad = value

    # Conectar y crear base de datos y tabla si no existen
    # def crear_tabla(self):
    #     tablas = """
    #     INSERT INTO empleado (nombre, rol_id, email, salario, fecha_registro) VALUES
    #     ('Nelson', 3, 'neo1@example.com', 44.0, '2024-11-25');
    #     """
    #     try:
    #         self.conn.execute_query(tablas)
    #         # self.cargar_empleados()
    #     except ValueError:
    #         messagebox.showerror("Error", "El salario debe ser un número.")

    def cargar_empleados(self) -> list:
        data = self.connexion.fetch_query(
            """
            SELECT 
            empleado.id as id, 
            empleado.nombre as nombre, 
            rol.rol_nombre as rol_nombre,
            empleado.email as email, 
            empleado.salario as salario,
            empleado.fecha_registro as fecha_registro 
            FROM 
            empleado as empleado,
            rol as rol
            WHERE rol.id = empleado.rol_id
        """
        )
        return data

    # Función para agregar un nuevo empleado
    def agregar_empleado(self):
        nombre = self.__nombre
        rol_id = self.__rol_id
        email = self.__email
        salario = self.__salario
        fecha_ingreso = self.__fecha_ingreso
        if nombre and rol_id and email and salario and fecha_ingreso:
            try:
                salario = float(salario)
                self.connexion.execute_query(
                    "INSERT INTO empleado (nombre, rol_id, email, salario, fecha_registro) VALUES (?, ?, ?, ?, ?)",
                    (nombre, rol_id, email, salario, fecha_ingreso),
                )
                # self.cargar_empleados()
            except ValueError:
                messagebox.showerror("Error", "El salario debe ser un número.")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    # Función para eliminar un empleado seleccionado
    def eliminar_empleado(self):

        try:
            if self.__cantidad == 1:
                id = self.__id
                self.connexion.execute_query("DELETE FROM empleado WHERE id = ?", (id,))
            elif self.__cantidad > 1:
                datos = self.__data
                self.connexion.execute_query_many(
                    "DELETE FROM empleado WHERE id = ?", datos
                )

        except IndexError:
            messagebox.showwarning(
                "Advertencia", "Selecciona un empleado para eliminar."
            )

    def exportar_json_empleados(self) -> bool:
        data = self.connexion.fetch_query_json(
            """
            SELECT *
            FROM 
            empleado as empleado,
            rol as rol
            WHERE rol.id = empleado.rol_id
        """
        )
        return data

    def cargar_empleados_to_dict(self) -> list[dict]:
        data = self.connexion.fetch_query_to_dict(
            """
            SELECT 
            empleado.id as id, 
            empleado.nombre as nombre, 
            rol.rol_nombre as rol_nombre,
            empleado.email as email, 
            empleado.salario as salario,
            empleado.fecha_registro as fecha_registro 
            FROM 
            empleado as empleado,
            rol as rol
            WHERE rol.id = empleado.rol_id
        """
        )
        return data
