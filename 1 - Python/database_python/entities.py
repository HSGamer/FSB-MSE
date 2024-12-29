class Item:
    def __init__(self, code, name):
        self.code = code
        self.name = name


class ItemImport:
    def __init__(self, import_id, item_code, quantity, price, import_date):
        self.import_id = import_id
        self.item_code = item_code
        self.quantity = quantity
        self.price = price
        self.import_date = import_date