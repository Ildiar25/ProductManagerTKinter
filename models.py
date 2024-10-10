from tkinter.ttk import Treeview
from tkinter import ttk
from tkinter import *
from sqlite3 import Cursor
import sqlite3


class MainWindow:

    # Path database
    db = "database/products.db"

    # Order values
    ordered_by_name = False
    ordered_by_price = True
    ordered_by_category = True
    ordered_by_stock = True

    # Color values
    primary = "#3a3f44"
    secondary = "#7a8288"
    success = "#62c462"
    info = "#5bc0de"
    warning = "#f89406"
    danger = "#ee5f5b"
    light = "#e9ecef"
    dark = "#272b30"

    def __init__(self, root: Tk) -> None:
        self.window = root
        self.new_window = None

        # Main window settings
        self.window.title("Gestor de Productos")
        self.window.minsize(580, 700)
        self.window.resizable(True, True)
        self.window.wm_iconbitmap("assets/product-manager-icon.ico")

        # Main window grid config
        self.window.grid_columnconfigure(0, weight=1)

        # Background window style settings
        self.window.configure(
            background=self.dark,
            padx=10,
            pady=10
        )

        # ---------- Main frames ----------

        # This frame contains the main form
        add_element_frame = Frame(self.window)
        add_element_frame.configure(
            background=self.primary,
            pady=15,
            padx=15,
        )
        add_element_frame.grid_columnconfigure(0, weight=1)
        add_element_frame.grid_columnconfigure(1, weight=3)
        add_element_frame.grid_columnconfigure(2, weight=1)
        add_element_frame.grid(row=0, column=0, padx=5, pady=5)

        # This frame contains the database table
        table_content_frame = Frame(self.window)
        table_content_frame.configure(
            background=self.primary,
            pady=15,
            padx=15
        )
        table_content_frame.grid_columnconfigure(0, weight=4)
        table_content_frame.grid(row=1, column=0, sticky=W + N + E + S, padx=5, pady=5)

        # This frame contains the action buttons
        action_buttons_frame = Frame(self.window)
        action_buttons_frame.configure(
            background=self.primary,
            pady=5,
            padx=5
        )
        action_buttons_frame.grid(row=2, column=0, sticky=W + N + E + S, padx=5, pady=5)

        # Form frame
        label_frame = LabelFrame(add_element_frame, text="Nuevo Producto")
        label_frame.grid(row=0, column=1)
        label_frame.configure(
            background=self.primary,
            foreground=self.light,
            borderwidth=2,
            font=("Calibri", 12, "bold"),
            padx=15,
            pady=15
        )
        label_frame.grid_columnconfigure(0, weight=1)
        label_frame.grid_columnconfigure(1, weight=1)
        label_frame.grid_columnconfigure(2, weight=1)
        label_frame.grid_columnconfigure(3, weight=1)
        label_frame.grid_columnconfigure(4, weight=1)

        # Name label
        self.name_label = Label(label_frame, text="Nombre: ", anchor=E)
        self.name_label.configure(
            background=self.primary,
            foreground=self.light,
            font=("Calibri", 12, "italic")
        )
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky=W + E)

        # Name entry
        self.name = Entry(label_frame)
        self.name.configure(
            background=self.dark,
            font=("Calibri", 12, "italic"),
            foreground=self.light,
            justify="right"
        )
        self.name.focus()  # Autofocus on the field
        self.name.grid(row=0, column=1, columnspan=3, sticky=W + E)

        # Price label
        self.price_label = Label(label_frame, text="Precio: ", anchor=E)
        self.price_label.configure(
            background=self.primary,
            foreground=self.light,
            font=("Calibri", 12, "italic")
        )
        self.price_label.grid(row=1, column=0, padx=5, pady=5, sticky=W + E)

        # Price entry
        self.price = Entry(label_frame)
        self.price.configure(
            background=self.dark,
            font=("Calibri", 12, "italic"),
            foreground=self.light,
            justify="right"
        )
        self.price.grid(row=1, column=1, columnspan=3, sticky=W + E)

        # Stock label
        self.stock_label = Label(label_frame, text="Cantidad: ", anchor=E)
        self.stock_label.configure(
            background=self.primary,
            foreground=self.light,
            font=("Calibri", 12, "italic")
        )
        self.stock_label.grid(row=2, column=0, padx=5, pady=5, sticky=W + E)

        # Stock entry
        self.stock = Entry(label_frame)
        self.stock.configure(
            background=self.dark,
            font=("Calibri", 12, "italic"),
            foreground=self.light,
            justify="right"
        )
        self.stock.grid(row=2, column=1, columnspan=3, sticky=W + E)

        # Category label
        self.category_label = Label(label_frame, text="Categoría: ", anchor=E)
        self.category_label.configure(
            background=self.primary,
            foreground=self.light,
            font=("Calibri", 12, "italic")
        )
        self.category_label.grid(row=3, column=0, padx=5, pady=5, sticky=W + E)

        # Category dropdown menu
        self.choices = ["Consumible", "Electrónica", "Ordenador", "Telefonía"]
        self.dropdown_menu = ttk.Combobox(label_frame, values=self.choices, state="readonly")
        self.dropdown_menu.configure(
            background=self.primary,
            font=("Calibri", 12, "italic"),
            justify="right"
        )
        self.dropdown_menu.current(0)  # Sets default value
        self.dropdown_menu.grid(row=3, column=3)

        self.divider01 = Frame(label_frame, height=3)
        self.divider01.configure(
            background=self.secondary,
        )
        self.divider01.grid(row=4, column=0, columnspan=5, padx=5, pady=10, sticky=W + E)

        # Add button
        self.add_button = Button(label_frame, text="Agregar producto",
                                 command=lambda: self.add_product(table_content_frame)
                                 )
        self.add_button.configure(
            background=self.warning,
            foreground=self.dark,
            font=("Calibri", 12, "bold")
        )
        self.add_button.grid(row=5, column=0, columnspan=5, padx=5, pady=5, sticky=W + E)

        # Message label
        self.info = Label(label_frame, text="", anchor=CENTER)
        self.info.configure(
            background=self.primary,
            font=("Calibri", 13, "italic"),
            fg=self.success
        )
        self.info.grid(row=6, column=0, columnspan=5, sticky=W + N + E + S)

        # Update buttons
        self.del_button = Button(action_buttons_frame, text="BORRAR", width=50,
                                 command=lambda: self.del_product(table_content_frame)
                                 )
        self.del_button.configure(
            background=self.secondary,
            font=("Calibri", 12, "bold"),
            padx=5,
            pady=5,
            relief="flat",
            overrelief="ridge"
        )
        self.del_button.grid(row=0, column=0, sticky=W + E)

        self.update_button = Button(action_buttons_frame, text="MODIFICAR", width=50,
                                    command=lambda: self.update_product(table_content_frame)
                                    )
        self.update_button.configure(
            background=self.secondary,
            font=("Calibri", 12, "bold"),
            padx=5,
            pady=5,
            relief="flat",
            overrelief="ridge"
        )
        self.update_button.grid(row=0, column=1, sticky=W + E)

        self.get_products(table_content_frame)

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

    def get_products_by_name(self, frame: Misc) -> None:

        # Clear the table frame
        for widget in frame.winfo_children():
            widget.destroy()

        new_table = self.create_table(frame)

        if self.ordered_by_name:
            query = "SELECT * FROM product ORDER BY name ASC"
            records = self.new_request(query)

        else:
            query = "SELECT * FROM product ORDER BY name DESC"
            records = self.new_request(query)

        for element in records:
            new_table.insert("", 0, text=element[1], values=element[2:])

        self.ordered_by_name = not self.ordered_by_name

    def get_products_by_price(self, frame: Misc) -> None:

        # Clear the table frame
        for widget in frame.winfo_children():
            widget.destroy()

        new_table = self.create_table(frame)

        if self.ordered_by_price:
            query = "SELECT * FROM product ORDER BY price ASC"
            records = self.new_request(query)

        else:
            query = "SELECT * FROM product ORDER BY price DESC"
            records = self.new_request(query)

        for element in records:
            new_table.insert("", 0, text=element[1], values=element[2:])

        self.ordered_by_price = not self.ordered_by_price

    def get_products_by_category(self, frame: Misc) -> None:

        # Clear the table frame
        for widget in frame.winfo_children():
            widget.destroy()

        new_table = self.create_table(frame)

        if self.ordered_by_category:
            query = "SELECT * FROM product ORDER BY category ASC"
            records = self.new_request(query)

        else:
            query = "SELECT * FROM product ORDER BY category DESC"
            records = self.new_request(query)

        for element in records:
            new_table.insert("", 0, text=element[1], values=element[2:])

        self.ordered_by_category = not self.ordered_by_category

    def get_products_by_stock(self, frame: Misc) -> None:

        # Clear the table frame
        for widget in frame.winfo_children():
            widget.destroy()

        new_table = self.create_table(frame)

        if self.ordered_by_stock:
            query = "SELECT * FROM product ORDER BY stock ASC"
            records = self.new_request(query)

        else:
            query = "SELECT * FROM product ORDER BY stock DESC"
            records = self.new_request(query)

        for element in records:
            new_table.insert("", 0, text=element[1], values=element[2:])

        self.ordered_by_stock = not self.ordered_by_stock

    def get_products(self, frame: Misc) -> None:

        # Clear the table frame
        for widget in frame.winfo_children():
            widget.destroy()

        # Adds new table
        new_table = self.create_table(frame)

        # Connects to databse
        query = "SELECT * FROM product ORDER BY name DESC"
        records = self.new_request(query)

        for element in records:
            new_table.insert("", 0, text=element[1], values=element[2:])

    def add_product(self, frame: Misc) -> None:
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
            self.get_products(frame)

        else:
            self.info.config(text="¡Todos los campos son obligatorios!")

    def create_table(self, frame: Misc) -> Treeview:
        # Product Tables:
        style = ttk.Style()  # Creates the Style object

        # Treeview Style -- Sets the main table appearance and its font style
        style.configure(
            "mystyle.Treeview",
            background=self.secondary,
            highlightthikness=0,
            font=("Calibri", 11)
        )

        # Heading Style -- Sets the heading text style
        style.configure(
            "mystyle.Treeview.Heading",
            font=("Calibri", 12, "bold")
        )

        # Style Layout -- Deletes all borders
        style.layout(
            "mystyle.Treeview",
            [("mystyle.Treeview.treearea", {"sticky": W + N + E + S})]
        )

        # Table structure
        table = ttk.Treeview(frame, columns=[0, 1, 2], style="mystyle.Treeview")
        table.grid(row=0, column=0, sticky=W + E)

        # Heading State
        table.heading("#0", text=f"Nombre {'⮝' if self.ordered_by_name else '⮟'}",
                      anchor=CENTER,
                      command=lambda: self.get_products_by_name(frame)
                      )
        table.heading("#1", text=f"Precio (€) {'⮝' if self.ordered_by_price else '⮟'}",
                      anchor=CENTER,
                      command=lambda: self.get_products_by_price(frame)
                      )
        table.heading("#2", text=f"Categoría {'⮝' if self.ordered_by_category else '⮟'}",
                      anchor=CENTER,
                      command=lambda: self.get_products_by_category(frame)
                      )
        table.heading("#3", text=f"Stock (uds) {'⮝' if self.ordered_by_stock else '⮟'}",
                      anchor=CENTER,
                      command=lambda: self.get_products_by_stock(frame)
                      )

        return table

    def update_product(self, frame: Misc) -> None:
        # Resets info message
        self.info.config(text="")

        # Iterates over all widgets on frame
        product = [child for child in frame.winfo_children() if isinstance(child, ttk.Treeview)]

        # Select the table value
        row = product[0].selection()

        if len(row) == 0:
            self.info.config(text="¡Debes seleccionar al menos un producto!", foreground=self.danger)

        else:
            # Work flow to check if the new window exists
            if self.new_window is None or not self.new_window.winfo_exists():

                # Sets selected row into respective variables
                old_name = product[0].item(row[0])["text"]
                old_price = product[0].item(row[0])["values"][0]
                old_category = product[0].item(row[0])["values"][1]
                old_stock = product[0].item(row[0])["values"][2]

                # Sets new window
                self.new_window = Toplevel()

                # New window -- Settings
                self.new_window.title("Modificar Producto")
                self.new_window.wm_iconbitmap("assets/new-product-icon.ico")
                self.new_window.wm_minsize(630, 420)
                self.new_window.resizable(False, False)

                # New window -- Grid settings
                self.new_window.grid_columnconfigure(0, weight=1)

                # New window -- Styling
                self.new_window.configure(
                    background=self.dark,
                    padx=10,
                    pady=10
                )

                new_window_frame = Frame(self.new_window)
                new_window_frame.configure(
                    background=self.primary,
                    padx=15,
                    pady=15
                )
                new_window_frame.pack()

                # New window -- Widgets
                title = Label(new_window_frame, text=f"Editar {old_name}")
                title.grid(row=0, column=0, padx=5, pady=5)
                title.config(
                    background=self.primary,
                    font=("Calibri", 24, "bold"),
                    foreground=self.light
                )

                external_frame = LabelFrame(new_window_frame, text="Rellena el formulario")
                external_frame.configure(
                    background=self.primary,
                    foreground=self.light,
                    borderwidth=2,
                    font=("Calibri", 12, "bold"),
                    padx=15,
                )
                external_frame.grid(row=1, column=0, sticky=W + N + E + S)

                # Old name label
                old_name_label = Label(external_frame, text="Nombre anterior:", anchor=E)
                old_name_label.configure(
                    background=self.primary,
                    foreground=self.light,
                    font=("Calibri", 12, "italic")
                )
                old_name_label.grid(row=0, column=0, padx=5, pady=5, sticky=W + E)

                # Old name entry
                old_name_entry = Entry(
                    external_frame,
                    textvariable=StringVar(external_frame, old_name),
                    state="disabled"
                )
                old_name_entry.configure(
                    disabledbackground=self.dark,
                    font=("Calibri", 12, "italic"),
                    disabledforeground=self.warning,
                    justify="right"
                )
                old_name_entry.grid(row=0, column=1, sticky=W + E)

                # New name label
                new_name_label = Label(external_frame, text="Nuevo nombre:", anchor=E)
                new_name_label.configure(
                    background=self.primary,
                    foreground=self.light,
                    font=("Calibri", 12, "italic")
                )
                new_name_label.grid(row=1, column=0, padx=5, pady=5, sticky=W + E)

                # New name entry
                new_name_entry = Entry(external_frame)
                new_name_entry.configure(
                    background=self.dark,
                    font=("Calibri", 12, "italic"),
                    foreground=self.light,
                    justify="right"
                )
                new_name_entry.grid(row=1, column=1, sticky=W + E)

                # Old price label
                old_price_label = Label(external_frame, text="Precio anterior:", anchor=E)
                old_price_label.configure(
                    background=self.primary,
                    foreground=self.light,
                    font=("Calibri", 12, "italic")
                )
                old_price_label.grid(row=2, column=0, padx=5, pady=5, sticky=W + E)

                # Old price entry
                old_price_entry = Entry(
                    external_frame,
                    textvariable=StringVar(self.new_window, f"{old_price} €"),
                    state="disabled"
                )
                old_price_entry.configure(
                    disabledbackground=self.dark,
                    font=("Calibri", 12, "italic"),
                    disabledforeground=self.warning,
                    justify="right"
                )
                old_price_entry.grid(row=2, column=1, sticky=W + E)

                # New price label
                new_price_label = Label(external_frame, text="Nuevo precio:", anchor=E)
                new_price_label.configure(
                    background=self.primary,
                    foreground=self.light,
                    font=("Calibri", 12, "italic")
                )
                new_price_label.grid(row=3, column=0, padx=5, pady=5, sticky=W + E)

                # New price entry
                new_price_entry = Entry(external_frame)
                new_price_entry.configure(
                    background=self.dark,
                    font=("Calibri", 12, "italic"),
                    foreground=self.light,
                    justify="right"
                )
                new_price_entry.grid(row=3, column=1, sticky=W + E)

                # Old stock label
                old_stock_label = Label(external_frame, text="Cantidad anterior:", anchor=E)
                old_stock_label.configure(
                    background=self.primary,
                    foreground=self.light,
                    font=("Calibri", 12, "italic")
                )
                old_stock_label.grid(row=4, column=0, padx=5, pady=5, sticky=W + E)

                # Old stock entry
                old_stock_entry = Entry(
                    external_frame,
                    textvariable=StringVar(self.new_window, f"{old_stock} uds"),
                    state="disabled"
                )
                old_stock_entry.configure(
                    disabledbackground=self.dark,
                    font=("Calibri", 12, "italic"),
                    disabledforeground=self.warning,
                    justify="right"
                )
                old_stock_entry.grid(row=4, column=1, sticky=W + E)

                # New stock label
                new_stock_label = Label(external_frame, text="Nueva cantidad:", anchor=E)
                new_stock_label.configure(
                    background=self.primary,
                    foreground=self.light,
                    font=("Calibri", 12, "italic")
                )
                new_stock_label.grid(row=5, column=0, padx=5, pady=5, sticky=W + E)

                # New stock entry
                new_stock_entry = Entry(external_frame)
                new_stock_entry.configure(
                    background=self.dark,
                    font=("Calibri", 12, "italic"),
                    foreground=self.light,
                    justify="right"
                )
                new_stock_entry.grid(row=5, column=1, sticky=W + E)

                # Old category label
                old_category_label = Label(external_frame, text="Nueva categoría:", anchor=E)
                old_category_label.configure(
                    background=self.primary,
                    foreground=self.light,
                    font=("Calibri", 12, "italic")
                )
                old_category_label.grid(row=6, column=0, padx=5, pady=5, sticky=W + E)

                # New category dropdown
                new_category_entry = ttk.Combobox(external_frame, values=self.choices, state="readonly")
                new_category_entry.configure(
                    background=self.primary,
                    font=("Calibri", 12, "italic"),
                    justify="right"
                )
                current_category = self.choices.index(old_category)
                new_category_entry.current(current_category)

                new_category_entry.grid(row=6, column=1)

                divider02 = Frame(new_window_frame, height=3)
                divider02.configure(
                    background=self.secondary,
                )
                divider02.grid(row=2, column=0, columnspan=5, padx=5, pady=10, sticky=W + E)

                old_data = [old_name, old_price, old_category, old_stock]
                new_data = [new_name_entry.get(), new_price_entry.get(),
                            new_category_entry.get(), new_stock_entry.get()]

                edit_button = Button(new_window_frame, text="Actualizar",
                                     command=lambda: self.update_database_product(frame, old_data,
                                                                                  new_data=[new_name_entry.get(),
                                                                                            new_price_entry.get(),
                                                                                            new_category_entry.get(),
                                                                                            new_stock_entry.get()]),
                                     width=50
                                     )

                edit_button.configure(
                    background=self.success,
                    foreground=self.dark,
                    font=("Calibri", 12, "bold")
                )
                edit_button.grid(row=3, column=0)

            else:
                # Focus to windows if exists
                self.new_window.focus()

    def update_database_product(self, frame: Misc, old_data: list[str], new_data: list[str]) -> None:
        if len(new_data[0]) != 0 and len(new_data[1]) != 0 and len(new_data[3]) != 0:

            # Sets new request to database
            query = ("UPDATE product SET name = ?, price = ?, category = ?, stock = ? WHERE name = ? AND"
                     " price = ? AND category = ? AND stock = ?")
            parameters = (new_data[0], new_data[1], new_data[2], new_data[3],
                          old_data[0], old_data[1], old_data[2], old_data[3],)
            self.new_request(query, parameters)

            # Closes the window
            self.new_window.destroy()

            # Notify the user
            self.info.config(text="El producto se ha actualizado con éxito", foreground=self.success)

            # Updates table view
            self.get_products(frame)

    def del_product(self, frame: Misc) -> None:
        # Resets info message
        self.info.config(text="")

        # Iterates over all widgets on frame
        product = [child for child in frame.winfo_children() if isinstance(child, ttk.Treeview)]

        # Select the table value
        row = product[0].selection()

        if len(row) == 0:
            self.info.config(text="¡Debes seleccionar al menos un producto!", foreground=self.danger)

        else:
            # Prepares the element to be erased
            product_name = product[0].item(row[0])["text"]

            # New request and its parameters
            query = "DELETE FROM product WHERE name = ?"
            parameter = (product_name, )
            self.new_request(query, parameter)

            # Updates table view
            self.get_products(frame)

    def validate_name(self):
        return len(self.name.get()) != 0

    def validate_price(self):
        return len(self.price.get()) != 0

    def validate_stock(self):
        return len(self.stock.get()) != 0
