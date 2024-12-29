import tkinter
from tkinter import messagebox
from tkinter.ttk import *

from dao import *


class ItemWindow(tkinter.Toplevel):
    def __init__(self, parent, connection, item: Item=None):
        super().__init__(parent)
        self.connection = connection

        self.grid_columnconfigure(1, weight=1)

        code_label = tkinter.Label(self, text="Code")
        code_label.grid(row=0, column=0)
        self.code_entry = tkinter.Entry(self)
        self.code_entry.grid(row=0, column=1, sticky="EW")

        name_label = tkinter.Label(self, text="Name")
        name_label.grid(row=1, column=0)
        self.name_entry = tkinter.Entry(self)
        self.name_entry.grid(row=1, column=1, sticky="EW")

        button_frame = tkinter.Frame(self)
        button_frame.grid(row=2, column=0, columnspan=2)

        save_button = tkinter.Button(button_frame, text="Save")
        save_button.grid(row=0, column=0, sticky="EW")

        cancel_button = tkinter.Button(button_frame, text="Cancel")
        cancel_button.grid(row=0, column=1, sticky="EW")

        if item:
            self.create_item = False
            self.code_entry.insert(0, item.code)
            self.name_entry.insert(0, item.name)
            self.code_entry.config(state=tkinter.DISABLED)
            self.title("Edit item")
        else:
            self.create_item = True
            self.title("Create item")

        save_button.config(command=self.save)
        cancel_button.config(command=self.destroy)

    def validate(self):
        code = self.code_entry.get()
        name = self.name_entry.get()

        if not code or not name:
            messagebox.showerror("Error", "Code and name are required", parent=self)
            return False

        if self.create_item and is_item_code_exists(self.connection, code):
            messagebox.showerror("Error", f"Item with code {code} already exists", parent=self)
            return False

        if is_item_name_exists(self.connection, name):
            messagebox.showerror("Error", f"Item with name {name} already exists", parent=self)
            return False

        return True

    def save(self):
        if not self.validate():
            return

        code = self.code_entry.get()
        name = self.name_entry.get()

        item = Item(code, name)
        if self.create_item:
            insert_item(self.connection, item)
        else:
            update_item(self.connection, item)

        self.destroy()
        messagebox.showinfo("Success", "Item saved")

class ItemImportGUI(tkinter.Toplevel):
    def __init__(self, parent, connection, item: Item, item_import: ItemImport = None):
        super().__init__(parent)
        self.connection = connection

        self.item_import = item_import
        self.item = item

        self.grid_columnconfigure(1, weight=1)

        item_label = tkinter.Label(self, text="Item")
        item_label.grid(row=0, column=0)
        self.item_entry = tkinter.Entry(self)
        self.item_entry.grid(row=0, column=1, sticky="EW")
        self.item_entry.insert(0, item.name)
        self.item_entry.config(state=tkinter.DISABLED)

        quantity_label = tkinter.Label(self, text="Quantity")
        quantity_label.grid(row=1, column=0)
        self.quantity_entry = tkinter.Entry(self)
        self.quantity_entry.grid(row=1, column=1, sticky="EW")

        price_label = tkinter.Label(self, text="Price")
        price_label.grid(row=2, column=0)
        self.price_entry = tkinter.Entry(self)
        self.price_entry.grid(row=2, column=1, sticky="EW")

        import_date_label = tkinter.Label(self, text="Import date")
        import_date_label.grid(row=3, column=0)
        self.import_date_entry = tkinter.Entry(self)
        self.import_date_entry.grid(row=3, column=1, sticky="EW")

        button_frame = tkinter.Frame(self)
        button_frame.grid(row=4, column=0, columnspan=2)

        save_button = tkinter.Button(button_frame, text="Save")
        save_button.grid(row=0, column=0, sticky="EW")

        cancel_button = tkinter.Button(button_frame, text="Cancel")
        cancel_button.grid(row=0, column=1, sticky="EW")

        if item_import:
            self.title("Edit item import")
            self.quantity_entry.insert(0, item_import.quantity)
            self.price_entry.insert(0, item_import.price)
            self.import_date_entry.insert(0, item_import.import_date)
        else:
            self.title("Create item import")

        save_button.config(command=self.save)
        cancel_button.config(command=self.destroy)

    def validate(self):
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()
        import_date = self.import_date_entry.get()

        if not quantity or not price or not import_date:
            messagebox.showerror("Error", "Quantity, price and import date are required", parent=self)
            return False

        return True

    def save(self):
        if not self.validate():
            return

        item_code = self.item.code
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()
        import_date = self.import_date_entry.get()

        item_import = ItemImport(None, item_code, quantity, price, import_date)
        if self.item_import:
            item_import.import_id = self.item_import.import_id
            update_item_import(self.connection, item_import)
        else:
            insert_item_import(self.connection, item_import)

        self.destroy()
        messagebox.showinfo("Success", "Item import saved")

class App(tkinter.Tk):
    def __init__(self, connection):
        super().__init__()
        self.item_imports = None
        self.connection = connection
        self.title("Inventory Management")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # region Item Frame
        self.add_item_button = tkinter.Button(self, text="Add item")
        self.add_item_button.grid(row=0, column=0, padx=10, pady=5, sticky="EW")

        self.item_table = Treeview(self, columns=("code", "name", "quantity"), show="headings")
        self.item_table.heading("code", text="Code")
        self.item_table.heading("name", text="Name")
        self.item_table.heading("quantity", text="Quantity")
        self.item_table.grid(row=1, column=0, padx=10, pady=5, sticky="NSEW")

        item_search_frame = tkinter.Frame(self)
        item_search_frame.grid(row=2, column=0, padx=10, pady=5, sticky="EW")
        item_search_frame.grid_columnconfigure(1, weight=1)

        search_label = tkinter.Label(item_search_frame, text="Search Price")
        search_label.grid(row=0, column=0)
        self.search_var = tkinter.StringVar()
        self.search_entry = tkinter.Entry(item_search_frame, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=1, sticky="EW")

        item_actions_frame = tkinter.Frame(self)
        item_actions_frame.grid(row=3, column=0, padx=10, pady=5, sticky="EW")
        item_actions_frame.grid_columnconfigure(0, weight=1)
        item_actions_frame.grid_columnconfigure(1, weight=1)

        self.edit_item_button = tkinter.Button(item_actions_frame, text="Edit")
        self.edit_item_button.grid(row=0, column=0, sticky="EW")

        self.delete_item_button = tkinter.Button(item_actions_frame, text="Delete")
        self.delete_item_button.grid(row=0, column=1, sticky="EW")
        # endregion

        # region Item Import Frame
        self.add_item_import_button = tkinter.Button(self, text="Add item import")
        self.add_item_import_button.grid(row=0, column=1, padx=10, pady=5, sticky="EW")

        item_import_display_frame = tkinter.Frame(self)
        item_import_display_frame.grid(row=1, column=1, rowspan=2, padx=10, pady=5, sticky="NSEW")
        item_import_display_frame.grid_columnconfigure(0, weight=1)
        item_import_display_frame.grid_rowconfigure(1, weight=1)

        self.item_import_combo = Combobox(item_import_display_frame)
        self.item_import_combo.grid(row=0, column=0, sticky="EW")
        self.item_import_combo["state"] = "readonly"

        item_import_info_frame = tkinter.Frame(item_import_display_frame)
        item_import_info_frame.grid(row=1, column=0, pady=10, sticky="NSEW")
        item_import_info_frame.grid_columnconfigure(1, weight=1)

        quantity_label = tkinter.Label(item_import_info_frame, text="Quantity")
        quantity_label.grid(row=0, column=0)
        self.quantity_entry = tkinter.Entry(item_import_info_frame, state="readonly")
        self.quantity_entry.grid(row=0, column=1, sticky="EW")

        price_label = tkinter.Label(item_import_info_frame, text="Price")
        price_label.grid(row=1, column=0)
        self.price_entry = tkinter.Entry(item_import_info_frame, state="readonly")
        self.price_entry.grid(row=1, column=1, sticky="EW")

        import_date_label = tkinter.Label(item_import_info_frame, text="Import date")
        import_date_label.grid(row=2, column=0)
        self.import_date_entry = tkinter.Entry(item_import_info_frame, state="readonly")
        self.import_date_entry.grid(row=2, column=1, sticky="EW")

        item_import_actions_frame = tkinter.Frame(self)
        item_import_actions_frame.grid(row=3, column=1, padx=10, pady=5, sticky="EW")
        item_import_actions_frame.grid_columnconfigure(0, weight=1)
        item_import_actions_frame.grid_columnconfigure(1, weight=1)

        self.edit_item_import_button = tkinter.Button(item_import_actions_frame, text="Edit")
        self.edit_item_import_button.grid(row=0, column=0, sticky="EW")

        self.delete_item_import_button = tkinter.Button(item_import_actions_frame, text="Delete")
        self.delete_item_import_button.grid(row=0, column=1, sticky="EW")
        # endregion

        # region Bindings
        self.add_item_button.config(command=self.add_item)
        self.item_table.bind("<<TreeviewSelect>>", self.on_item_selected)
        self.search_var.trace("w", self.on_search)
        self.edit_item_button.config(command=self.edit_item)
        self.delete_item_button.config(command=self.delete_item)
        self.item_import_combo.bind("<<ComboboxSelected>>", self.on_item_import_selected)
        self.add_item_import_button.config(command=self.add_item_import)
        self.edit_item_import_button.config(command=self.edit_item_import)
        self.delete_item_import_button.config(command=self.delete_item_import)
        # endregion

        self.display_items()

    def on_search(self, *args):
        self.display_items()

    def on_item_selected(self, event):
        self.display_item_imports()

    def on_item_import_selected(self, event):
        self.display_item_import_info()

    def display_item_imports(self):
        item = self.get_selected_item(show_error=False)
        self.item_imports = [] if not item else get_item_imports_by_item_code(self.connection, item.code)
        self.item_import_combo["values"] = [f"{item_import.import_date} - {item_import.quantity}" for item_import in self.item_imports]

        if self.item_imports:
            self.item_import_combo.current(0)
        else:
            self.item_import_combo.set("")

        self.display_item_import_info()

    def display_item_import_info(self):
        item_import = self.get_selected_item_import(show_error=False)

        self.quantity_entry.config(state=tkinter.NORMAL)
        self.price_entry.config(state=tkinter.NORMAL)
        self.import_date_entry.config(state=tkinter.NORMAL)

        self.quantity_entry.delete(0, tkinter.END)
        self.price_entry.delete(0, tkinter.END)
        self.import_date_entry.delete(0, tkinter.END)

        if item_import:
            self.quantity_entry.insert(0, item_import.quantity)
            self.price_entry.insert(0, item_import.price)
            self.import_date_entry.insert(0, item_import.import_date)

        self.quantity_entry.config(state="readonly")
        self.price_entry.config(state="readonly")
        self.import_date_entry.config(state="readonly")

    def get_selected_item_import(self, show_error=True) -> ItemImport | None:
        selection = self.item_import_combo.current()
        if selection == -1:
            if show_error:
                messagebox.showerror("Error", "No item import selected")
            return None

        return self.item_imports[selection]

    def display_items(self):
        self.item_table.delete(*self.item_table.get_children())
        search = self.search_var.get()
        if search:
            items = search_items_with_quantity_by_price(self.connection, search)
        else:
            items = get_items_with_quantity(self.connection)

        for item, quantity in items:
            self.item_table.insert("", "end", values=(item.code, item.name, quantity))

        self.display_item_imports()

    def add_item(self):
        window = ItemWindow(self, self.connection)
        window.grab_set()
        window.wait_window()
        self.display_items()

    def get_selected_item(self, show_error=True) -> Item | None:
        selection = self.item_table.selection()
        if not selection:
            if show_error:
                messagebox.showerror("Error", "No item selected")
            return None

        code = self.item_table.item(selection[0])["values"][0]
        return get_item_by_code(self.connection, code)

    def edit_item(self):
        item = self.get_selected_item()
        if not item:
            return

        window = ItemWindow(self, self.connection, item)
        window.grab_set()
        window.wait_window()
        self.display_items()

    def delete_item(self):
        item = self.get_selected_item()
        if not item:
            return

        if get_item_imports_by_item_code(self.connection, item.code):
            messagebox.showerror("Error", "Item has imports, cannot delete")
            return

        if messagebox.askyesno("Delete", f"Are you sure you want to delete item {item.code}"):
            delete_item(self.connection, item.code)
            messagebox.showinfo("Success", "Item deleted")
            self.display_items()

    def add_item_import(self):
        item = self.get_selected_item()
        if not item:
            return

        window = ItemImportGUI(self, self.connection, item)
        window.grab_set()
        window.wait_window()
        self.display_items()

    def edit_item_import(self):
        item = self.get_selected_item()
        if not item:
            return

        item_import = self.get_selected_item_import()
        if not item_import:
            return

        window = ItemImportGUI(self, self.connection, item, item_import)
        window.grab_set()
        window.wait_window()
        self.display_items()

    def delete_item_import(self):
        item_import = self.get_selected_item_import()
        if not item_import:
            return

        if messagebox.askyesno("Delete", f"Are you sure you want to delete item import {item_import.import_date} - {item_import.quantity}"):
            delete_item_import(self.connection, item_import.import_id)
            messagebox.showinfo("Success", "Item import deleted")
            self.display_items()