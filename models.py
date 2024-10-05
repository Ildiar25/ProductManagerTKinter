from tkinter import ttk
from tkinter import *
from sqlite3 import Cursor
import sqlite3


class MainWindow:

    db = "database/products.db"

    def __init__(self, root: Tk) -> None:
        self.window = root

        # Main settings
        self.window.title("Gestor de Productos")
        self.window.minsize(width=420, height=630)
        self.window.resizable(False, False)
        self.window.wm_iconbitmap("assets/product-manager-icon.ico")

        # Grid config
        self.window.grid_columnconfigure(0, weight=1)

        # Background style settings
        self.window.configure(
            # background="#272b30",
            padx=20,
            pady=20
        )

        # Main frame
        frame = LabelFrame(self.window, text="Añadir Nuevo Producto", width=380)
        frame.grid()
        frame.configure(
            # background="#3F454E",
            borderwidth=1,
            font=("Calibri", 12)
        )

        # Name label
        self.name_label = Label(frame, text="Nombre: ")
        self.name_label.grid(row=1, column=0)

        # Name entry
        self.name = Entry(frame)
        self.name.focus()  # Autofocus on the field
        self.name.grid(row=1, column=1)

        # Price label
        self.price_label = Label(frame, text="Precio: ")
        self.price_label.grid(row=2, column=0)

        # Price entry
        self.price = Entry(frame)
        self.price.grid(row=2, column=1)

        # Add button
        self.add_button = ttk.Button(frame, text="Guardar", command=self.add_product)
        self.add_button.grid(row=3, columnspan=2, sticky=W + E)

        # Product Tables:
        style = ttk.Style()  # Creates the Style object

        # Treeview Style -- Sets the main table appearance and its font style
        style.configure("mystyle.Treeview", highlightthikness=0, bd=0, font=("Calibri", 11))

        # Heading Style -- Sets the heading text style
        style.configure("mystyle.Treeview.Heading", font=("Calibri", 13, "bold"))

        # Style Layout -- Deletes all borders
        style.layout("mystyle.Treeview", [("mystyle.Treeview.treearea", {"sticky": "nswe"})])

        # Table structure
        self.table = ttk.Treeview(height=20, columns=[0, 1, 2], style="mystyle.Treeview")
        self.table.grid(row=4, column=0, columnspan=4)

        # Heading State
        self.table.heading("#0", text="Nombre", anchor=CENTER)
        self.table.heading("#1", text="Precio", anchor=CENTER)
        self.table.heading("#2", text="Categoría", anchor=CENTER)
        self.table.heading("#3", text="Stock", anchor=CENTER)
        self.get_products()

    def new_request(self, query: str, parameters: tuple | None = None) -> Cursor:

        # Makes parameters an empty tuple if its value is None
        if parameters is None:
            parameters = ()

        # Sets the connexion to database
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()

            # Loads the response
            data = cursor.execute(query, parameters)
            conn.commit()

        # Returns query
        return data

    def get_products(self) -> None:
        query = "SELECT * FROM product ORDER BY name DESC"

        records = self.new_request(query)
        for element in records:
            print(element)
            self.table.insert("", 0, text=element[1], values=element[2:])

    def add_product(self) -> None:
        raise NotImplementedError("'add_product' function is not implemented yet")

    def validate_name(self):
        raise NotImplementedError

    def validate_price(self):
        raise NotImplementedError

    def validate_stock(self):
        raise NotImplementedError