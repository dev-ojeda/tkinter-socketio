import tkinter as tk
from interfaces.main import FrameSigin, DashboardApp
from interfaces.menu_bar import MenuBarApp


class Application(tk.Tk):
    def __init__(self):
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
        """Función para mostrar una ventana y ocultar las demás."""
        for widget in self.winfo_children():
            widget.pack_forget()
        ventana.pack(expand=True, fill="both")


if __name__ == "__main__":
    app = Application()
    app.mainloop()
