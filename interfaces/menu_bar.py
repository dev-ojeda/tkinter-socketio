import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class MenuBarApp(ttk.Frame):
    """docstring for ClassName."""

    def __init__(self, master):
        super(MenuBarApp, self).__init__(master)
        self.master = master
        self.menu_bar = tk.Menu(self)
        # Crear el menú "Archivo"
        self.menu_archivo = tk.Menu(self.menu_bar, tearoff=0, name="menu_archivo")
        self.menu_archivo.add_command(label="Nuevo", command=self.nuevo_archivo)
        self.menu_archivo.add_command(label="Abrir", command=self.abrir_archivo)
        self.menu_archivo.add_command(label="Guardar", command=self.guardar_archivo)
        self.menu_archivo.add_separator()
        self.menu_archivo.add_command(label="Salir", command=self.salir)
        self.menu_bar.add_cascade(label="Archivo", menu=self.menu_archivo)

        # Crear el menú "Editar"
        self.menu_editar = tk.Menu(self.menu_bar, tearoff=0, name="menu_editar")
        self.menu_editar.add_command(label="Deshacer")
        self.menu_editar.add_command(label="Rehacer")
        self.menu_editar.add_separator()
        self.menu_editar.add_command(label="Copiar")
        self.menu_editar.add_command(label="Pegar")
        self.menu_bar.add_cascade(label="Editar", menu=self.menu_editar)

        # Crear el menú "Ver"
        self.menu_ver = tk.Menu(self.menu_bar, tearoff=0, name="menu_editar")
        # self.menu_ver.add_command(label="Listar", command=self.listar_empleados)
        self.menu_ver.add_command(label="Cerrar", command=self.salir_empleados)
        self.menu_bar.add_cascade(label="Ver", menu=self.menu_ver)

    # Funciones para los comandos de los menús
    def nuevo_archivo(self):
        messagebox.showinfo("Nuevo Archivo", "Se ha creado un nuevo archivo.")

    # def listar_empleados(self):
    #     self.frame_treeview.frame_filtro.pack(pady=10, padx=30, expand=True)
    #     self.frame_treeview.frame_tree.pack(pady=10, padx=30, fill="both", expand=True)
    #     self.frame_treeview.frame_pagination.pack(pady=10, padx=30, expand=True)
    #     self.frame_treeview.pack()

    def salir_empleados(self):

        for value in self.menu_bar.winfo_children():
            print(value)
        # for value in self.frame_treeview.winfo_manager:
        #     pass
        # self.frame_treeview.frame_filtro.destroy()
        # self.frame_treeview.frame_tree.destroy()
        # self.frame_treeview.frame_pagination.destroy()
        # self.frame_treeview.destroy()

    def abrir_archivo(self):
        messagebox.showinfo("Abrir Archivo", "Se ha abierto un archivo.")

    def guardar_archivo(self):
        messagebox.showinfo("Guardar Archivo", "Se ha guardado el archivo.")

    def salir(self):
        self.master.quit()
        self.master.destroy()
        sys.exit()

    def logout(self):
        """Cierra sesión y regresa a la ventana de login."""
        # self.master.title("LOGIN")
        # self.master.geometry("400x200")
        self.master.quit()
        self.master.destroy()
        sys.exit()
