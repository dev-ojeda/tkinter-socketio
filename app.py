import sys
import tkinter as tk
from interfaces.main import FrameSigin, DashboardApp
from interfaces.menu_bar import MenuBarApp


class Application(tk.Tk):
    """
        Clase para iniciar la aplicacion
    Args:
        tk (Tk): Main de la aplicacion
    """

    def __init__(self) -> None:
        """
        Constructor para inicializar la clase
        """
        super().__init__()
        self.title("LOGIN")
        self.geometry("450x250")
        self.attributes("-fullscreen", False)
        # self.resizable(False, False)

        # Cambiar color del botón (solo si tu tema lo permite)
        self.update_idletasks()  # Necesario para asegurarse de que los estilos se actualicen
        self.frame_sigin = FrameSigin(self)
        # Instancia de EventEmitter (broker de eventos)
        self.menu = MenuBarApp(self)
        self.frame_dashboard = DashboardApp(self)
        # Mostrar la ventana de login al inicio
        self.mostrar_ventana(self.frame_sigin)

    def mostrar_ventana(self, ventana) -> None:
        """
        Función para mostrar una ventana y ocultar las demás.
        Args:
            ventana (Frame): Recibe el frame
        """
        for widget in self.winfo_children():
            widget.pack_forget()
        ventana.pack(expand=True, fill="both")


if __name__ == "__main__":
    app = Application()
    app.protocol("WM_DELETE_WINDOW", lambda: (app.quit(), app.destroy(), sys.exit(0)))
    app.mainloop()

