import tkinter as tk
from tkinter import messagebox


# Clase para manejar la sesión de usuario
class Session:
    def __init__(self):
        self.user = None

    def login(self, username):
        """Inicia la sesión con el nombre de usuario dado"""
        self.user = username

    def logout(self):
        """Cierra la sesión del usuario"""
        self.user = None

    def is_logged_in(self):
        """Verifica si hay un usuario en sesión"""
        return self.user is not None


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Inicio de Sesión")
        self.geometry("300x200")
        # self.withdraw()  # Ocultar la ventana principal hasta iniciar sesión
        # Crear las dos ventanas (frames)
        # Crear la instancia de sesión

        self.ventana_login = VentanaLogin(self)
        self.ventana_principal = VentanaPrincipal(self)

        # Mostrar la ventana de login al inicio
        self.mostrar_ventana(self.ventana_login)

    def mostrar_ventana(self, ventana):
        """Función para mostrar una ventana y ocultar las demás."""
        for widget in self.winfo_children():
            widget.pack_forget()
        ventana.pack()


class VentanaLogin(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.session = Session()
        # Campos de entrada para usuario y contraseña
        tk.Label(self, text="Usuario").grid(row=0, column=0, padx=5, pady=5)
        self.entry_username = tk.Entry(self)
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Contraseña").grid(row=1, column=0, padx=5, pady=5)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        # Botón de inicio de sesión
        self.login_button = tk.Button(self, text="Iniciar Sesión", command=self.login)
        self.login_button.grid(row=3, column=1, padx=5)

    # Función de inicio de sesión

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        validar = self.session.is_logged_in()
        if validar:
            messagebox.showinfo("Inicio de sesión", f"Usuario Logeado, {username}!")
        elif username == "usuario" and password == "1234":
            self.session.login(username)
            messagebox.showinfo("Inicio de sesión", f"Bienvenido, {username}!")
            self.master.mostrar_ventana(self.master.ventana_principal)
        else:
            messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos")


class VentanaPrincipal(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.session = Session()
        self.boton_logout = tk.Button(
            self,
            text="Cerrar sesión",
            command=self.logout,
        )
        self.boton_logout.grid(row=0, column=2, padx=5)

    # Función de cierre de sesión
    def logout(self):
        self.session.logout()
        self.master.mostrar_ventana(self.master.ventana_login)


if __name__ == "__main__":
    app = Application()
    # Iniciar el bucle principal
    app.mainloop()
