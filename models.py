# from tkinter import ttk
from tkinter import *
# import sqlite3


class MainWindow:

    def __init__(self, root: Tk) -> None:
        self.window = root

        # Main settings
        self.window.title("Gestor de Productos")
        self.window.minsize(width=420, height=630)
        self.window.resizable(True, True)
        self.window.wm_iconbitmap("assets/product-manager-icon.ico")

        # Style settings
        self.window.configure(
            background="#272b30",
            padx=20,
            pady=20
        )

        # Main frame
        frame = LabelFrame(self.window, text="Añadir Nuevo Producto")
        frame.grid(row=0, column=0, columnspan=3)

        self.window.mainloop()
