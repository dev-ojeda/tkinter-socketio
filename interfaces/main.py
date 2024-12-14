from datetime import date, datetime
import os
import queue
import re
import sys
import tkinter as tk
from tkinter import PhotoImage, messagebox
from tkinter import ttk
from model.empleado import Empleado
from model.enum_rol import Roles
from model.usuario import Usuario
from ttkwidgets import CheckboxTreeview
from tkcalendar import Calendar
from services.event_bus import ConsumerApp, SocketIOApp
from ttkwidgets.utilities import get_assets_directory


class FrameSigin(ttk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.style = ttk.Style()
        # Cambiar el tema (clam, default, alt, etc.)
        self.style.theme_use("clam")
        self.style.configure("TLabel", font=("Helvetica", 12), padding=5)
        self.style.configure("TEntry", font=("Helvetica", 12), padding=5)
        self.style.configure(
            "TButton",
            font=("Helvetica", 12, "bold"),
            background="#4CAF50",
            foreground="white",
        )
        self.style.map(
            "TButton",
            # Cuando el botón está activo (hover)
            background=[("active", "lightblue")],
            foreground=[("active", "darkblue")],
        )  # Cambiar el

        self.frame_login = ttk.Frame(self, padding="20 20", relief="groove")

        # Etiqueta y campo de usuario
        ttk.Label(self.frame_login, text="Usuario:").grid(
            row=0, column=0, sticky="e", pady=10
        )
        self.entry_usuario = ttk.Entry(self.frame_login, width=30)
        self.entry_usuario.insert(0, "admin")
        self.entry_usuario.grid(row=0, column=1, pady=10)

        ttk.Label(self.frame_login, text="Contraseña:").grid(
            row=1, column=0, sticky="e", pady=10
        )
        self.entry_contraseña = ttk.Entry(self.frame_login, show="*", width=30)
        self.entry_contraseña.insert(0, "1234")
        self.entry_contraseña.grid(row=1, column=1, padx=5, pady=5)

        self.boton_login = ttk.Button(
            self.frame_login,
            text="Iniciar sesión",
            style="TButton",
            command=self.verificar_login,
        )
        self.boton_login.grid(
            row=2,
            column=0,
            pady=20,
            columnspan=2,
        )
        self.frame_login.pack(ipadx=5, ipady=5, expand=True)

    # Función para verificar el login y cambiar de ventana
    def verificar_login(self) -> None:
        self.user = Usuario()
        self.user._usuario = self.entry_usuario.get()
        self.user._contraseña = self.entry_contraseña.get()
        if self.user.verificar_login():
            messagebox.showinfo("Inicio de sesión", "Inicio de sesión exitoso")
            self.master.title("PRINCIPAL")
            self.master.geometry("850x650")
            self.master.config(bg="#86c5b7")
            # self.master.config(menu=self.master.menu.menu_bar)
            # self.master.tree_view.frame_logout.pack(pady=5)
            # self.master.tree_view.frame_datos.pack(
            #     padx=20, pady=20, fill="both", expand=True
            # )
            # self.master.tree_view.frame_botones.pack(pady=10)
            # self.master.frame_treeview.frame_filtro.pack(pady=10, padx=30, expand=True)
            # self.master.frame_treeview.frame_pagination.pack(
            #     pady=10, padx=30, expand=True
            # )
            # self.master.frame_treeview.panel_principal_vertical.pack(
            #     pady=15, padx=15, fill="both", expand=True
            # )
            # self.master.frame_treeview.panel_principal_horizontal.pack(
            #     pady=20, padx=20, fill="both", expand=True
            # )
            self.master.frame_dashboard.paned_window.pack(
                pady=10, padx=30, fill="both", expand=True
            )
            self.master.mostrar_ventana(self.master.frame_dashboard)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")


class FrameSigout(ttk.Frame):
    """docstring for FrameApp."""

    def __init__(self, master) -> None:
        super().__init__(master)
        self.master = master
        self.frame_logout = ttk.Frame(self, name="frame_logout")
        self.boton_logout = tk.Button(
            self.frame_logout,
            text="Cerrar sesión",
            command=self.logout,
        )
        self.boton_logout.grid(row=0, column=2, padx=5)

        messagebox.showinfo("Nuevo Archivo", "Se ha creado un nuevo archivo.")

    def abrir_archivo(self) -> None:
        messagebox.showinfo("Abrir Archivo", "Se ha abierto un archivo.")

    def guardar_archivo(self) -> None:
        messagebox.showinfo("Guardar Archivo", "Se ha guardado el archivo.")

    def salir(self) -> None:
        self.master.quit()
        self.master.destroy()
        sys.exit()

    def logout(self) -> None:
        """Cierra sesión y regresa a la ventana de login."""
        self.master.quit()
        self.master.destroy()
        sys.exit()
        # self.master.mostrar_ventana(self.master.frame_login)


class DashboardApp(ttk.Frame):
    """docstring for TreeviewApp."""

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.lista = []
        self.datos_pagina = []
        self.items_seleccionados = []
        self.estado = 0
        self.message_queue = queue.Queue()
        self.filas_por_pagina = 10  # Tamaño de cada página
        self.pagina_actual = 0
        self.cargar_estilos()
        self.cargar_images()
        # Contenedor principal
        self.main_frame = ttk.Frame(self, relief="groove")
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.pack_propagate(False)
        self.paned_window = ttk.Panedwindow(self.main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(padx=20, pady=20, expand=True, fill="both")

        # Menú lateral
        self.menu_frame = ttk.Frame(
            self.main_frame, width=150, relief="groove", style="FD.TFrame"
        )
        self.menu_frame.pack_propagate(False)
        self.menu_frame.pack(side="left", fill="y")

        # Área de contenido
        self.content_frame = ttk.Frame(
            self.main_frame, relief="groove", style="FD.TFrame"
        )
        self.content_frame.pack_propagate(False)
        self.content_frame.pack(side="right", fill="both", expand=True)
        self.paned_window.add(self.menu_frame)
        self.paned_window.add(self.content_frame)

        # Opciones del menú
        self.buttons = {
            "Inicio": self.mostrar_inicio,
            "Configuración": self.mostrar_configuracion,
            "Formulario": self.ingresar_empleado,
            "Listado": self.validar_data,
            "Chat": self.abrir_chat,
        }

        # Crear los botones del menú
        for text, command in self.buttons.items():
            btn = ttk.Button(
                self.menu_frame, text=text, command=command, style="Custom.TButton"
            )
            btn.pack(fill="x", padx=10, pady=5)

        # Frame actual
        self.current_frame = None

        # Mostrar la pantalla de inicio al iniciar
        self.mostrar_inicio()

    def cambiar_frame(self, nuevo_frame) -> None:
        """Cambiar el frame actual por un nuevo frame."""
        if self.current_frame:
            self.current_frame.destroy()  # Eliminar el frame actual
        self.current_frame = nuevo_frame
        self.current_frame.pack(fill="both", expand=True)

    def cargar_estilos(self) -> None:
        """Carga los estilos para los controles."""
        self.style_label_entry_button = ttk.Style()
        self.style_label_entry_button.theme_use("clam")
        self.style_label_entry_button.configure(
            "Custom.TLabel",
            font=("Helvetica", 14, "italic"),
            foreground="darkblue",
            background="lightgray",
            padding=5,
        )
        self.style_label_entry_button.configure(
            "Custom.TEntry",
            font=("Verdana", 12),
            foreground="black",
            fieldbackground="lightyellow",
            padding=5,
        )
        self.style_label_entry_button.configure(
            "Custom.TButton",
            font=("Helvetica", 12, "bold"),
            background="#4CAF50",
            foreground="white",
        )
        self.style_label_entry_button.map(
            "Custom.TButton",
            # Cuando el botón está activo (hover)
            background=[("active", "lightblue")],
            foreground=[("active", "darkblue")],
        )  # Cambiar el
        self.style_frame_datos = ttk.Style()
        self.style_frame_datos.theme_use("clam")
        self.style_frame_datos.configure(
            "Custom.Treeview",
            font=("Helvetica", 12),
            background="lightgray",
            rowheight=25,
            fieldbackground="lightgray",
            borderwidth=5,
        )  # Altura de cada fila
        self.style_frame_datos.configure(
            "Custom.Treeview.Heading",
            font=("Helvetica", 14, "bold"),
            background="#628879",
            foreground="lightblue",
        )
        self.style_frame_datos.configure(
            "Custom.TCombobox",
            fieldbackground="#f0f8ff",  # Color de fondo del área de entrada
            background="#4682b4",  # Color del fondo desplegable
            foreground="black",  # Color del texto
            selectbackground="#87cefa",  # Color de fondo al seleccionar una opción
            selectforeground="white",  # Color del texto seleccionado
            borderwidth=4,
            # Tipo de borde (puede ser flat, solid, raised, etc.)
            relief="raised",
            font=("Arial", 12),  # Fuente y tamaño del texto
        )
        self.style_frame_datos.map(
            "Custom.Treeview",
            background=[("selected", "#347083")],
            foreground=[("selected", "black")],
        )

    def cargar_images(self) -> None:
        IM_EXECUTE = os.path.join(get_assets_directory(), "execute.png")
        self.ejecutar = PhotoImage(file=IM_EXECUTE)

    def crear_eventos(self) -> None:
        # Crear el Treeview
        self.consumer = ConsumerApp(self)

    def mostrar_inicio(self) -> None:
        """Mostrar el frame de inicio."""
        frame = ttk.Frame(self.content_frame)
        label = ttk.Label(frame, text="Bienvenido al Inicio", style="Custom.TLabel")
        label.pack(pady=20)
        self.cambiar_frame(frame)

    def abrir_chat(self) -> None:
        self.ventana_chat = SocketIOApp(self)

    def ingresar_empleado(self) -> None:
        """Mostrar el frame de ingreso de empleados."""
        # Crear un Frame para el lado derecho que contendrá un Notebook
        frame = ttk.Frame(self.content_frame)
        notebook = ttk.Notebook(frame)
        notebook.pack(fill="both")
        tab_form_datos = ttk.Frame(
            notebook, width=300, height=300, relief="groove", style="FD.TFrame"
        )
        ttk.Label(tab_form_datos, text="Nombre:", style="Custom.TLabel").grid(
            row=0, column=0, pady=5, padx=5
        )
        entry_nombre = ttk.Entry(tab_form_datos, style="Custom.TEntry")
        entry_nombre.grid(row=0, column=1, pady=5, padx=5, sticky="w")

        ttk.Label(tab_form_datos, text="Rol:", style="Custom.TLabel").grid(
            row=1, column=0, pady=5, padx=5
        )
        # Crear un Combobox con el estilo personalizado
        self.opciones = {0: "Seleccione", 1: "SRE", 2: "DEV", 3: "ING"}
        cmb_puesto = ttk.Combobox(
            tab_form_datos,
            state="normal",
            values=[v for v in self.opciones.values()],
            style="Custom.TCombobox",
        )
        cmb_puesto.set(str(self.opciones[0]))
        cmb_puesto.grid(row=1, column=1, pady=6, padx=6, sticky="w")
        # Email
        ttk.Label(tab_form_datos, text="Email:", style="Custom.TLabel").grid(
            row=2, column=0, pady=5, padx=5
        )
        self.entry_email = ttk.Entry(tab_form_datos, style="Custom.TEntry")
        self.entry_email.grid(row=2, column=1, pady=5, padx=5, sticky="w")

        ttk.Label(tab_form_datos, text="Salario:", style="Custom.TLabel").grid(
            row=3, column=0, pady=5, padx=5
        )
        entry_salario = ttk.Entry(tab_form_datos, style="Custom.TEntry")
        entry_salario.grid(row=3, column=1, pady=5, padx=5, sticky="w")

        # Calendar
        ttk.Label(tab_form_datos, text="Fecha:", style="Custom.TLabel").grid(
            row=4, column=0, pady=5, padx=5
        )

        fecha_ingreso = Calendar(
            tab_form_datos,
            locale="en_US",
            day=datetime.now().day,
            month=datetime.now().month,
            year=datetime.now().year,
            cursor="hand1",
            disabledforeground="red",
            selectmode="day",
            date_pattern="yyyy-mm-dd",
            selectforeground="green",
        )
        fecha_ingreso.grid(row=4, column=1, pady=5, padx=5, sticky="w")
        # Botones de control
        btn_agregar = ttk.Button(tab_form_datos, text="Agregar", style="Custom.TButton")
        btn_agregar.grid(row=5, column=1, pady=10, padx=10, sticky="w")
        # self.btn_editar = tk.Button(self.frame_botones, text="Editar", command=editar_empleado)
        # self.btn_editar.grid(row=0, column=1, padx=5)
        tab_form_datos.pack(padx=20, pady=20, expand=True, fill="both")
        notebook.add(tab_form_datos, text="Ingreso Empleados")
        self.cambiar_frame(frame)

    def agregar_empleado(self) -> None:
        """Funcion para agregar empleados"""
        self.empleado = Empleado()
        self.empleado._nombre = self.entry_nombre.get()
        rol = self.cmb_puesto.get()
        if rol == Roles.SRE.name:
            rol = Roles.SRE.value
        elif rol == Roles.DEV.name:
            rol = Roles.DEV.value
        elif rol == Roles.ING.name:
            rol = Roles.ING.value
        else:
            rol = 0
        self.empleado._rol_id = rol
        self.empleado._email = self.entry_email.get()
        self.empleado._salario = self.entry_salario.get()
        fec_ini = datetime.strptime(self.fecha_ingreso.get_date(), "%Y-%m-%d")
        fec_ini_all = datetime(
            fec_ini.year,
            fec_ini.month,
            fec_ini.day,
            datetime.now().hour,
            datetime.now().minute,
            datetime.now().second,
        )
        self.empleado._fecha_ingreso = fec_ini_all
        if self.validar_email():
            self.empleado.agregar_empleado()
            self.entry_nombre.delete(0, tk.END)
            self.cmb_puesto.set(str(self.opciones[0]))
            self.entry_email.delete(0, tk.END)
            self.entry_salario.delete(0, tk.END)
            self.fecha_ingreso.selection_set(str(date.today()))
            self.lista_empleados()
        else:
            return

    def eliminar_empleado_consumido(self) -> None:
        valores_consumidos = self.consumer.valores_claves
        empleado = Empleado()
        empleado._data = list(())
        cantidad = len(valores_consumidos)
        empleado._cantidad = cantidad
        for clave, value in tuple(sorted(valores_consumidos)):
            empleado._data.append((int(value),))
        empleado.eliminar_empleado()
        self.estado = 0
        self.lista_empleados()

    def eliminar_empleado(self) -> None:
        empleado = Empleado()
        empleado._data = list(())
        item = [(a, self.treeview.item(a, "values")[0]) for a in self.current_selection]
        cantidad = len(item)
        empleado._cantidad = cantidad
        if cantidad == 1:
            empleado._id = int(item[0][1])
            self.treeview.delete(item[0][0])
        else:
            for k, v in item:
                empleado._data.append((int(v),))
                self.treeview.delete(k)
        empleado.eliminar_empleado()
        self.estado = 0
        self.lista_empleados()

    def mostrar_listado_empleados(self) -> None:
        frame = ttk.Frame(self.content_frame)
        notebook = ttk.Notebook(frame)
        notebook.pack(fill="both")

        # Agregar treeview empleados
        self.tab_treeview_empleado = ttk.Frame(
            notebook, style="FD.TFrame", width=300, height=800, relief="sunken"
        )
        self.create_filtro()
        # Frame para Paginacion
        self.frame_pagination = ttk.Frame(
            self.tab_treeview_empleado,
            style="FD.TFrame",
            relief="sunken",
            width=200,
            height=200,
        )
        self.frame_pagination.pack(padx=10, pady=10, fill="both")
        # Frame para Treeview
        self.frame_tree = ttk.Frame(
            self.tab_treeview_empleado,
            style="FD.TFrame",
            relief="sunken",
            width=500,
            height=600,
        )
        self.frame_tree.pack(padx=20, pady=20, expand=True, fill="both")
        self.frame_tree_empleados = ttk.Frame(
            self.frame_tree,
            style="FD.TFrame",
            relief="sunken",
            width=200,
            height=300,
        )

        ##### TREEVIEW ########
        self.treeview = CheckboxTreeview(self.frame_tree_empleados)
        self.treeview.configure(
            selectmode="none", show="tree headings", style="Custom.Treeview"
        )
        self.treeview["columns"] = (
            "ID",
            "Nombre",
            "Rol",
            "Email",
            "Salario",
            "Fecha Inicio",
            "Hora Inicio",
        )
        self.treeview.column("#0", anchor=tk.CENTER, width=60, stretch=tk.NO)
        self.treeview.column(
            "ID", anchor=tk.CENTER, width=60, stretch=tk.NO
        )  # Ocultar la primera columna
        self.treeview.column("Nombre", anchor=tk.CENTER, width=120, stretch=tk.YES)
        self.treeview.column("Rol", anchor=tk.CENTER, width=50, stretch=tk.NO)
        self.treeview.column("Email", anchor=tk.CENTER, width=200, stretch=tk.YES)
        self.treeview.column("Salario", anchor=tk.CENTER, width=80, stretch=tk.YES)
        self.treeview.column(
            "Fecha Inicio", anchor=tk.CENTER, width=150, stretch=tk.YES
        )
        self.treeview.column("Hora Inicio", anchor=tk.CENTER, width=80, stretch=tk.YES)
        self.treeview.heading(
            "#0",
            text="ALL",
        )
        self.treeview.heading(
            "#1", text="ID", command=lambda: self.sort_column("#1", False)
        )
        self.treeview.heading(
            "#2", text="Nombre", command=lambda: self.sort_column("#2", False)
        )
        self.treeview.heading(
            "#3", text="Rol", command=lambda: self.sort_column("#3", False)
        )
        self.treeview.heading(
            "#4", text="Email", command=lambda: self.sort_column("#4", False)
        )
        self.treeview.heading(
            "#5",
            text="Salario",
            command=lambda: self.sort_column("#5", False),
        )
        self.treeview.heading(
            "#6",
            text="Fecha Inicio",
            command=lambda: self.sort_column("#6", False),
        )
        self.treeview.heading(
            "#7",
            text="Hora Inicio",
            command=lambda: self.sort_column("#7", False),
        )
        self.treeview.grid(row=3, column=0, padx=10, pady=10)
        self.crear_eventos()
        # self.btn_exportar = ttk.Button(
        #     self.frame_tree_empleados,
        #     text="Exportar",
        #     style="Custom.TButton",
        #     command=self.exportar_json_empleados,
        # )
        # self.btn_exportar.grid(row=5, column=0, padx=5)
        self.frame_tree_empleados.pack(padx=10, pady=10, side="left", fill="both")

        self.btn_anterior = ttk.Button(
            self.frame_pagination,
            text="Anterior",
            style="Custom.TButton",
            command=self.pagina_anterior,
        )
        self.btn_anterior.grid(row=5, column=0, padx=5, pady=5)

        self.label_pagina = ttk.Label(
            self.frame_pagination, style="Custom.TLabel", text="ALGO"
        )
        self.label_pagina.grid(row=5, column=1, padx=5, pady=5, sticky="e")

        self.btn_siguiente = ttk.Button(
            self.frame_pagination,
            text="Siguiente",
            style="Custom.TButton",
            command=self.pagina_siguiente,
        )
        self.btn_siguiente.grid(row=5, column=2, padx=5, pady=5)

        self.treeview.previous_selection = set()
        self.treeview.bind("<<TreeviewSelect>>", self.on_treeview_select)
        self.treeview.bind("<Button-1>", self.toogleCheck)
        self.separator_v = ttk.Separator(self.frame_tree, orient="vertical")
        self.separator_v.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        self.mostrar_formulario_empleados()
        ######  FIN    #######

        notebook.add(self.tab_treeview_empleado, text="Listado")
        self.cambiar_frame(frame)

    def mostrar_formulario_empleados(self) -> None:
        # Frame Datos
        self.frame_form_datos = ttk.Frame(
            self.frame_tree,
            style="FD.TFrame",
            width=200,
            height=600,
            relief="sunken",
        )
        self.frame_form_datos.pack(padx=15, pady=15, fill="both")

        ttk.Label(self.frame_form_datos, text="Nombre:", style="Custom.TLabel").grid(
            row=0, column=0, pady=5, padx=5
        )
        self.entry_nombre_tree = ttk.Entry(self.frame_form_datos, style="Custom.TEntry")
        self.entry_nombre_tree.grid(row=0, column=1, pady=5, padx=5, sticky="e")

        ttk.Label(self.frame_form_datos, text="Rol:", style="Custom.TLabel").grid(
            row=1, column=0, pady=5, padx=5
        )
        # Crear un Combobox con el estilo personalizado
        self.opciones = {0: "Seleccione", 1: "SRE", 2: "DEV", 3: "ING"}
        self.cmb_puesto_tree = ttk.Combobox(
            self.frame_form_datos,
            state="normal",
            values=[v for v in self.opciones.values()],
            style="Custom.TCombobox",
        )
        self.cmb_puesto_tree.grid(row=1, column=1, pady=6, padx=6, sticky="e")

        # Email
        ttk.Label(self.frame_form_datos, text="Email:", style="Custom.TLabel").grid(
            row=2, column=0, pady=5, padx=5
        )
        self.entry_email_tree = ttk.Entry(self.frame_form_datos, style="Custom.TEntry")
        self.entry_email_tree.grid(row=2, column=1, pady=5, padx=5, sticky="e")

        ttk.Label(self.frame_form_datos, text="Salario:", style="Custom.TLabel").grid(
            row=3, column=0, pady=5, padx=5
        )
        self.entry_salario_tree = ttk.Entry(
            self.frame_form_datos, style="Custom.TEntry"
        )
        self.entry_salario_tree.grid(row=3, column=1, pady=5, padx=5, sticky="e")

        ttk.Label(
            self.frame_form_datos, text="Fecha Ingreso:", style="Custom.TLabel"
        ).grid(row=4, column=0, pady=5, padx=5)

        self.fecha_ingreso_tree = Calendar(
            self.frame_form_datos,
            locale="en_US",
            day=datetime.now().day,
            month=datetime.now().month,
            year=datetime.now().year,
            cursor="hand1",
            disabledforeground="red",
            selectmode="day",
            date_pattern="yyyy-mm-dd",
            selectforeground="green",
        )
        self.fecha_ingreso_tree.grid(row=4, column=1, pady=5, padx=5, sticky="w")
        # # Botones de control
        # self.btn_agregar_tree = ttk.Button(
        #     self.frame_tree,
        #     text="Agregar",
        #     style="Custom.TButton",
        #     command=self.agregar_empleado,
        # )
        # self.btn_agregar_tree.grid(row=3, column=0, pady=5, padx=10)
        # self.btn_editar = tk.Button(self.frame_botones, text="Editar", command=editar_empleado)
        # self.btn_editar.grid(row=0, column=1, padx=5)
        self.btn_eliminar_tree = ttk.Button(
            self.frame_form_datos,
            text="Eliminar",
            style="Custom.TButton",
            state="disabled",
            command=self.eliminar_empleado,
        )
        self.btn_eliminar_tree.grid(row=5, column=1, pady=10, padx=10)

        # Separator vertical
        self.separator_h = ttk.Separator(self.frame_tree, orient="horizontal")
        self.separator_h.pack(side="top", fill=tk.X, padx=10)

        # Frame Datos
        self.btn_eliminar_items_seleccionados = ttk.Frame(
            self.frame_tree,
            style="FD.TFrame",
            width=150,
            height=400,
            relief="sunken",
        )
        self.btn_eliminar_items_seleccionados.pack(padx=10, pady=10, fill="both")

        self.btn_eliminar_items = ttk.Button(
            self.btn_eliminar_items_seleccionados,
            text="Eliminar Items Seleccionados",
            style="Custom.TButton",
            state="disabled",
            command=self.eliminar_empleado,
        )
        self.btn_eliminar_items.grid(row=3, column=1, pady=5, padx=5)

    def exportar_json_empleados(self) -> None:
        empleado = Empleado()
        if empleado.exportar_json_empleados():
            messagebox.showinfo("Exportar", "Datos exportados exitosamente")
        else:
            messagebox.showerror("Error al exportar", "Datos no exportados")

    def validar_data(self) -> None:
        if len(self.lista) == 0:
            self.mostrar_listado_empleados()
            self.lista_empleados()
        else:
            self.mostrar_listado_empleados()
            self.cargar_pagina()

    def validar_email(self) -> bool:
        email = self.entry_email.get()
        # Patrón de expresión regular para validar correos electrónicos
        patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if re.match(patron, email):
            # messagebox.showinfo("Validación Exitosa", f"El correo '{email}' es válido.")
            return True
        else:
            messagebox.showerror(
                "Error de Validación",
                f"'{
                    email}' no es un correo electrónico válido.",
            )
            return False

    def lista_empleados(self) -> None:
        self.lista.clear()
        # Configura el máximo valor de progreso
        # self.progressbar.start(100)
        empleado = Empleado()
        data = empleado.cargar_empleados()
        for row in data:
            # self.progressbar.step()
            self.lista.append(row)
            # self.treeview.insert("", tk.END, values=row)
            # self.update_idletasks()  # Refresca la ventana
            # time.sleep(0.05)  # Pausa para simular trabajo

        self.total_paginas = (
            len(self.lista) + self.filas_por_pagina - 1
        ) // self.filas_por_pagina
        self.cargar_pagina()
        # self.progressbar.stop()

    def cargar_pagina(self) -> None:
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # Calcular el inicio y fin de los datos para la página actual
        inicio = self.pagina_actual * self.filas_por_pagina
        fin = inicio + self.filas_por_pagina
        self.datos_pagina = self.lista[inicio:fin]
        # Insertar los datos de la página en el Treeview
        for fila in self.datos_pagina:
            id = fila[0]
            nombre = fila[1]
            rol = fila[2]
            email = fila[3]
            salario = fila[4]
            fecha_formateada = datetime.strptime(str(fila[5]), "%Y-%m-%d %H:%M:%S")
            fecha_ingreso = fecha_formateada.date()
            hora_inicio = fecha_formateada.time()
            item = self.treeview.insert(
                "",
                "end",
                text="",
                values=(id, nombre, rol, email, salario, fecha_ingreso, hora_inicio),
                tags="unchecked",
                image=self.treeview.im_unchecked,
            )
            self.treeview.item(
                item,
                tags="unchecked",
                image=self.treeview.im_unchecked,
            )
            # self.checkbox_states[self.item_id] = (
            #     False  # Todos los checkboxes comienzan desmarcados
            # )
        # Actualizar la etiqueta de la página
        self.label_pagina.config(
            text=f"Página {self.pagina_actual + 1} de {self.total_paginas}"
        )

        # Habilitar o deshabilitar los botones de navegación según la página actual
        self.btn_anterior.config(
            state="normal" if self.pagina_actual > 0 else "disabled"
        )
        self.btn_siguiente.config(
            state=(
                "normal" if self.pagina_actual < self.total_paginas - 1 else "disabled"
            )
        )

    def pagina_anterior(self) -> None:
        # global pagina_actual
        if self.pagina_actual > 0:
            self.pagina_actual -= 1
            self.cargar_pagina()

    def pagina_siguiente(self) -> None:
        # global pagina_actual
        if self.pagina_actual < self.total_paginas - 1:
            self.pagina_actual += 1
            self.cargar_pagina()

    def create_filtro(self) -> None:
        self.frame_filtro = ttk.Frame(
            self.tab_treeview_empleado,
            style="FD.TFrame",
            relief="sunken",
            width=200,
            height=200,
        )

        ttk.Label(self.frame_filtro, text="Filtro:", style="Custom.TLabel").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )
        self.filter_entry = ttk.Entry(self.frame_filtro, style="Custom.TEntry")
        self.filter_entry.bind("<KeyRelease>", self.filter_treeview)
        self.filter_entry.grid(row=0, column=1, padx=5, pady=5, sticky="e")
        # Frame para el filtro
        self.frame_filtro.pack(padx=10, pady=10, expand=True, fill="both")

    def mostrar_configuracion(self) -> None:
        """Mostrar el frame de configuración."""
        frame = ttk.Frame(self.content_frame)
        label = ttk.Label(frame, text="Configuración", font=("Arial", 16))
        label.pack(pady=20)

        # Controles adicionales
        ttk.Label(frame, text="Opción 1:").pack(pady=5)
        ttk.Entry(frame).pack(pady=5)

        ttk.Label(frame, text="Opción 2:").pack(pady=5)
        ttk.Entry(frame).pack(pady=5)

        self.cambiar_frame(frame)

    def mostrar_ayuda(self) -> None:
        """Mostrar el frame de ayuda."""
        frame = ttk.Frame(self.content_frame)
        label = ttk.Label(frame, text="Ayuda", font=("Arial", 16))
        label.pack(pady=20)
        ttk.Label(frame, text="Aquí puedes encontrar información útil.").pack(pady=10)
        self.cambiar_frame(frame)

    #### FUNCIONES TREEVIEW #####

    def toogleCheck(self, event) -> None:
        print(f"ESTADO: {self.estado}")
        x, y, widget = (event.x, event.y, event.widget)
        elem = widget.identify("element", x, y)
        elemento = self.treeview.identify_region(x, y)
        row_id = self.treeview.identify_row(y)
        col_id = self.treeview.identify_column(x)
        if "image" in elem or "text" in elem or row_id != "":
            self._check_uncheck_row(row_id)
        elif col_id == "#0":
            if self.estado == 0:
                self.estado = self.check_all()
            elif self.estado == 1:
                row_id = self.treeview.selection()
                if len(row_id) > 0:
                    self._check_uncheck_rows(row_id)
                else:
                    self.estado = self.uncheck_all()
            else:
                self.estado = 0
        elif elemento == "heading" and col_id != "#0":
            self.treeview.heading(
                col_id, command=lambda: self.sort_column(col_id, not False)
            )
        elif elem == "cell" and col_id != "#0":
            self.on_treeview_click(event)

    def esta_ordenada(self, tupla) -> bool:
        for i in range(len(tupla) - 1):
            if tupla[i] > tupla[i + 1]:
                return False
        return True

    def on_treeview_select(self, event) -> None:
        # Obtener la selección actual
        self.current_selection = set(self.treeview.selection())
        # Identificar si hay deselección comparando con la selección anterior
        deselected_items = self.treeview.previous_selection - self.current_selection
        if deselected_items:
            print("Elementos deseleccionados:", deselected_items)

        print(len(self.current_selection))
        if len(self.current_selection) > 1:
            self.btn_eliminar_items.config(state="normal")
            self.entry_nombre_tree.delete(0, tk.END)
            self.cmb_puesto_tree.set(str(self.opciones[0]))
            self.entry_email_tree.delete(0, tk.END)
            self.entry_salario_tree.delete(0, tk.END)
            self.fecha_ingreso_tree.selection_set(str(date.today()))
            self.btn_eliminar_tree.config(state="disabled")
        elif len(self.current_selection) == 1:
            item = [a for a in self.current_selection]
            print(item)
            valores = self.treeview.item(item, "values")
            self.entry_nombre_tree.insert(0, valores[1])
            self.cmb_puesto_tree.set(valores[2])
            self.entry_email_tree.insert(0, valores[3])
            self.entry_salario_tree.insert(0, valores[4])
            fec_ini = datetime.strptime(str(valores[5]), "%Y-%m-%d")
            self.fecha_ingreso_tree.selection_set(fec_ini)
            self.btn_eliminar_tree.config(state="normal")
        else:
            self.entry_nombre_tree.delete(0, tk.END)
            self.cmb_puesto_tree.set(str(self.opciones[0]))
            self.entry_email_tree.delete(0, tk.END)
            self.entry_salario_tree.delete(0, tk.END)
            self.fecha_ingreso_tree.selection_set(str(date.today()))
            self.btn_eliminar_tree.config(state="disabled")
            self.btn_eliminar_items.config(state="disabled")
        # Actualizar la selección anterior
        self.treeview.previous_selection = self.current_selection

    def sort_column(self, col, reverse) -> None:
        # Obtener los elementos y valores de la columna especificada
        items = [(self.treeview.set(k, col), k) for k in self.treeview.get_children("")]
        reverse = self.esta_ordenada(items)
        # Ordenar por tipo de dato (int o str)
        try:
            if col == "#1":
                items.sort(key=lambda t: int(t[0]), reverse=reverse)
            elif col == "#6":
                items.sort(
                    key=lambda t: datetime.strptime(t[0], "%Y-%m-%d"), reverse=reverse
                )
            elif col == "#7":
                items.sort(
                    key=lambda t: datetime.strptime(t[0], "%H:%M:%S"), reverse=reverse
                )
            else:
                items.sort(key=lambda t: t[0], reverse=reverse)
        except ValueError:
            items.sort(key=lambda t: t[0], reverse=reverse)

        # Reorganizar los elementos en el Treeview
        for index, (val, k) in enumerate(items):
            self.treeview.move(k, "", index)

        # Alternar entre ascendente y descendente en el siguiente clic
        # self.treeview.heading(col, command=lambda: self.sort_column(col, not reverse))

    def filter_treeview(self, event) -> None:
        filter_text = self.filter_entry.get().lower()
        # Limpiar Treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # Reinsertar elementos que coincidan con el filtro
        for id, nombre, rol, email, salario, fecha_ingreso in self.datos_pagina:
            if (
                filter_text in str(id)
                or filter_text in nombre.lower()
                or filter_text in rol.lower()
                or filter_text in email.lower()
                or filter_text in str(salario)
                or filter_text in str(fecha_ingreso)
            ):
                fecha_formateada = datetime.strptime(
                    str(fecha_ingreso), "%Y-%m-%d %H:%M:%S"
                )
                fecha_ingreso = fecha_formateada.date()
                hora_inicio = fecha_formateada.time()
                self.treeview.insert(
                    "",
                    tk.END,
                    values=(
                        id,
                        nombre,
                        rol,
                        email,
                        salario,
                        fecha_ingreso,
                        hora_inicio,
                    ),
                )

    def _check_uncheck_rows(self, row_id) -> None:
        for selected_item in row_id:
            tag = self.treeview.item(selected_item, "tags")[0]
            tags = list(self.treeview.item(selected_item, "tags"))
            tags.remove(tag)
            self.treeview.item(selected_item, tags=tags)
            if tag == "checked":
                self.treeview.item(
                    selected_item,
                    text="",
                    tags="unchecked",
                    image=self.treeview.im_unchecked,
                )
                self.treeview.selection_remove(self.treeview.selection())
            else:
                self.treeview.item(
                    selected_item,
                    text="",
                    tags="checked",
                    image=self.treeview.im_checked,
                )
                self.treeview.selection_add(selected_item)
        self.estado = 0

    def _check_uncheck_row(self, row_id) -> None:
        tag = self.treeview.item(row_id, "tags")[0]
        tags = list(self.treeview.item(row_id, "tags"))
        tags.remove(tag)
        self.treeview.item(row_id, tags=tags)
        if tag == "checked":
            self.treeview.item(
                row_id,
                text="",
                tags="unchecked",
                image=self.treeview.im_unchecked,
            )
            self.treeview.selection_remove(row_id)
        else:
            self.treeview.item(
                row_id,
                text="",
                tags="checked",
                image=self.treeview.im_checked,
            )
            self.treeview.selection_add(row_id)
        self.estado = 1

    def _check_uncheck_all(self, state, image) -> None:
        """Check or uncheck all items."""

        def aux(item):
            if item:
                self.change_state(item, state, image)
            children = self.treeview.get_children(item)
            self.treeview.selection_add(children)
            for c in children:
                aux(c)

        aux("")

    def uncheck_all(self) -> int:
        """Uncheck all items."""

        self._check_uncheck_all(state="unchecked", image="pyimage2")
        return 0

    def check_all(self) -> int:
        """Check all items."""

        self._check_uncheck_all(state="checked", image="pyimage1")

        return 1

    def change_state(self, item, state, image) -> None:
        """
        Replace the current state of the item.

        i.e. replace the current state tag but keeps the other tags.

        :param item: item id
        :type item: str
        :param state: "checked", "unchecked" or "tristate": new state of the item
        :type state: str
        """
        images = self.treeview.item(item, "image")
        tags = self.treeview.item(item, "tags")
        states = ("checked", "unchecked", "tristate")
        m_images = ("pyimage1", "pyimage2", "pyimage3")
        new_tags = [t for t in tags if t not in states]
        new_images = [i for i in images if i not in m_images]
        new_tags.append(state)
        new_images.append(image)
        self.treeview.item(item, tags=tuple(new_tags), image=tuple(new_images))
