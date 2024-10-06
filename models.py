from tkinter import ttk
from tkinter import *
from sqlite3 import Cursor
import sqlite3


class MainWindow:

    db = "database/products.db"

    def __init__(self, root: Tk) -> None:
        self.window = root
        self.new_window = None

        # Main settings
        self.window.title("Gestor de Productos")
        self.window.resizable(True, True)
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
        frame = LabelFrame(self.window, text="Nuevo Producto", width=380)
        frame.grid(row=0, column=0, columnspan=3)
        frame.configure(
            # background="#3F454E",
            borderwidth=1,
            font=("Calibri", 10, "bold"),
            padx=15,
            pady=15
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

        # Stock label
        self.stock_label = Label(frame, text="Cantidad: ")
        self.stock_label.grid(row=3, column=0)

        # Stock entry
        self.stock = Entry(frame)
        self.stock.grid(row=3, column=1)

        # Category label
        self.category_label = Label(frame, text="Categoría: ")
        self.category_label.grid(row=4)

        # Category dropdown menu
        self.choices = ["Consumible", "Electrónica", "Ordenador", "Telefonía"]
        self.dropdown_menu = ttk.Combobox(
            frame,  # Where menu will be
            values=self.choices,  # Contains all available elements
            textvariable=StringVar()  # Sets variable type (according to docs, is necessary set it)
        )
        self.dropdown_menu.current(0)  # Sets default value
        self.dropdown_menu.grid(row=5, columnspan=2)

        # Add button
        self.add_button = ttk.Button(frame, text="Guardar", command=self.add_product)
        self.add_button.grid(row=6, columnspan=2, sticky=W + E)

        # Message label
        self.info = Label(frame, text="", fg="#C21632")
        self.info.grid(row=7, columnspan=2, sticky=W + E)

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
        self.table.grid(row=8, column=0, columnspan=4)

        # Heading State
        self.table.heading("#0", text="Nombre", anchor=CENTER)
        self.table.heading("#1", text="Precio", anchor=CENTER)
        self.table.heading("#2", text="Categoría", anchor=CENTER)
        self.table.heading("#3", text="Stock", anchor=CENTER)

        # Update buttons
        self.del_button = ttk.Button(text="BORRAR", command=self.del_product)
        self.del_button.grid(row=9, column=0, sticky=W + E)

        self.update_button = ttk.Button(text="MODIFICAR", command=self.update_product)
        self.update_button.grid(row=9, column=1, sticky=W + E)

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

        # Delete all table values
        table_entries = self.table.get_children()
        for row in table_entries:
            self.table.delete(row)

        query = "SELECT * FROM product ORDER BY name DESC"

        records = self.new_request(query)

        for element in records:
            self.table.insert("", 0, text=element[1], values=element[2:])

    def add_product(self) -> None:
        # Resets info message
        self.info.config(text="")

        if self.validate_name() and self.validate_price() and self.validate_stock():

            # Set the request and its parameters
            query = "INSERT INTO product(name, price, category, stock) VALUES (?, ?, ?, ?)"
            parameters = (self.name.get(), self.price.get(), self.dropdown_menu.get(), self.stock.get())
            self.new_request(query, parameters)

            # User notification and update fields
            self.info.config(text=f"¡Producto '{self.name.get()}' agregado!")
            self.name.delete(0, END)
            self.price.delete(0, END)
            self.stock.delete(0, END)
            self.dropdown_menu.current(0)

            # Update products table
            self.get_products()

        else:
            self.info.config(text="¡Todos los campos son obligatorios!")

    def update_product(self) -> None:
        # Resets info message
        self.info.config(text="")

        # Sets the selected value on the table
        product = self.table.selection()

        if len(product) == 0:
            self.info.config(text="¡Debes seleccionar al menos un producto!")

        else:
            # Work flow to check if the new window exists
            if self.new_window is None or not self.new_window.winfo_exists():

                # Sets selected row into respective variables
                old_name = self.table.item(self.table.selection()[0])["text"]
                old_price = self.table.item(self.table.selection()[0])["values"][0]
                old_category = self.table.item(self.table.selection()[0])["values"][1]
                old_stock = self.table.item(self.table.selection()[0])["values"][2]

                # Sets new window
                self.new_window = Toplevel()

                # Sets new window settings
                self.new_window.title("Editar Producto")
                self.new_window.wm_iconbitmap("assets/new-product-icon.ico")
                self.new_window.wm_minsize(630, 420)
                self.new_window.resizable(False, False)

                self.new_window.grid_columnconfigure(0, weight=1)

                # EXTERNAL WINDOW SETTINGS
                title = Label(self.new_window, text="Editar Producto")
                title.grid(row=0, column=0, padx=5, pady=5)
                title.config(
                    font=("Calibri", 24, "bold")
                )

                external_frame = LabelFrame(self.new_window, text="Nuevo Producto", width=380)
                external_frame.grid(row=1, column=0, columnspan=4)
                external_frame.configure(
                    borderwidth=1,
                    font=("Calibri", 10, "bold"),
                    padx=15,
                    pady=15
                )

                # Old name label
                self.old_name = Label(external_frame, text="Nombre anterior:")
                self.old_name.grid(row=0, column=0)

                # Old name entry
                self.old_name_entry = Entry(
                    external_frame,
                    textvariable=StringVar(self.new_window, old_name),
                    state="readonly"
                )
                self.old_name_entry.grid(row=0, column=1)

                # New name label
                self.new_name = Label(external_frame, text="Nuevo nombre:")
                self.new_name.grid(row=1, column=0)

                # New name entry
                self.new_name_entry = Entry(external_frame)
                self.new_name_entry.grid(row=1, column=1)

                # Old price label
                self.old_price = Label(external_frame, text="Precio anterior:")
                self.old_price.grid(row=2, column=0)

                # Old price entry
                self.old_price_entry = Entry(
                    external_frame,
                    textvariable=StringVar(self.new_window, old_price),
                    state="readonly"
                )
                self.old_price_entry.grid(row=2, column=1)

                # New price label
                self.new_price = Label(external_frame, text="Nuevo precio:")
                self.new_price.grid(row=3, column=0)

                # New price entry
                self.new_price_entry = Entry(external_frame)
                self.new_price_entry.grid(row=3, column=1)

                # Old category entry
                self.old_category_entry = Entry(
                    external_frame,
                    textvariable=StringVar(self.new_window, old_category),
                    state="readonly"
                )
                self.old_category_entry.grid(row=5, column=0)

                # New category label
                self.new_category = Label(external_frame, text="Nueva categoría:")
                self.new_category.grid(row=5, column=1)

                # New category dropdown
                self.new_category_entry = ttk.Combobox(
                    external_frame,
                    values=self.choices,
                    textvariable=StringVar()
                )
                current_category = self.choices.index(old_category)
                self.new_category_entry.current(current_category)
                self.new_category_entry.grid(row=5, column=1)

                # Old stock label
                self.old_stock = Label(external_frame, text="Cantidad anterior:")
                self.old_stock.grid(row=6, column=0)

                # Old stock entry
                self.old_stock_entry = Entry(
                    external_frame,
                    textvariable=StringVar(self.new_window, old_stock),
                    state="readonly"
                )
                self.old_stock_entry.grid(row=6, column=1)

                # New stock label
                self.new_stock = Label(external_frame, text="Nueva cantidad:")
                self.new_stock.grid(row=7, column=0)

                # New stock entry
                self.new_stock_entry = Entry(external_frame)
                self.new_stock_entry.grid(row=7, column=1)

                self.edit_button = ttk.Button(external_frame, text="Actualizar",
                                              command=lambda:
                                              self.update_database_product(
                                                  self.old_name_entry.get(),
                                                  self.new_name_entry.get(),
                                                  self.old_price_entry.get(),
                                                  self.new_price_entry.get(),
                                                  self.old_category_entry.get(),
                                                  self.new_category_entry.get(),
                                                  self.old_stock_entry.get(),
                                                  self.new_stock_entry.get()
                                              ))
                self.edit_button.grid(row=8, columnspan=2)

            else:
                # Focus to windows if exists
                self.new_window.focus()

    def update_database_product(self, old_name: str, new_name: str,
                                old_price: str, new_price: str,
                                old_category: str, new_category: str,
                                old_stock: str, new_stock: str) -> None:

        if len(new_name) != 0 and len(new_price) != 0 and len(new_stock) != 0:

            # Sets new request to database
            query = ("UPDATE product SET name = ?, price = ?, category = ?, stock = ? WHERE name = ? AND"
                     " price = ? AND category = ? AND stock = ?")
            parameters = (new_name, new_price, new_category, new_stock, old_name, old_price, old_category, old_stock)
            self.new_request(query, parameters)

            # Closes the window
            self.new_window.destroy()

            # Notify the user
            self.info.config(text="El producto se ha actualizado con éxito", fg="#057849")

            # Updates table view
            self.get_products()

    def del_product(self) -> None:
        # Resets info message
        self.info.config(text="")

        # Sets the selected value on the table
        product = self.table.selection()

        if len(product) == 0:
            self.info.config(text="¡Debes seleccionar al menos un producto!")

        else:
            # Prepares the element to be erased
            product_name = self.table.item(product[0])["text"]

            # New request and its parameters
            query = "DELETE FROM product WHERE name = ?"
            parameter = (product_name, )
            self.new_request(query, parameter)

            # Updates table view
            self.get_products()

    def validate_name(self):
        return len(self.name.get()) != 0

    def validate_price(self):
        return len(self.price.get()) != 0

    def validate_stock(self):
        return len(self.stock.get()) != 0
