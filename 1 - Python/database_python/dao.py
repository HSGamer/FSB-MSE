import sqlite3

from entities import Item, ItemImport


def create_connection(database_file):
    connection = None
    try:
        connection = sqlite3.connect(database_file)
    except sqlite3.Error as e:
        print(e)
    return connection


def create_table(connection):
    try:
        c = connection.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute('''CREATE TABLE IF NOT EXISTS item
                    (code TEXT PRIMARY KEY,
                    name TEXT NOT NULL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS item_import
                    (import_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_code TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    import_date TEXT NOT NULL,
                    FOREIGN KEY (item_code) REFERENCES item(code))''')
        connection.commit()
    except sqlite3.Error as e:
        print(e)


def insert_item(connection, item: Item) -> Item:
    sql = '''INSERT INTO item(code, name)
             VALUES(?, ?)'''
    cur = connection.cursor()
    cur.execute(sql, (item.code, item.name))
    connection.commit()
    return item


def get_item_by_code(connection, code) -> Item | None:
    sql = '''SELECT * FROM item WHERE code = ?'''
    cur = connection.cursor()
    cur.execute(sql, (code,))
    result = cur.fetchone()
    if result:
        return Item(result[0], result[1])
    return None


def is_item_code_exists(connection, code) -> bool:
    sql = '''SELECT * FROM item WHERE code = ?'''
    cur = connection.cursor()
    cur.execute(sql, (code,))
    result = cur.fetchone()
    return result is not None


def is_item_name_exists(connection, name) -> bool:
    sql = '''SELECT * FROM item WHERE name = ?'''
    cur = connection.cursor()
    cur.execute(sql, (name,))
    result = cur.fetchone()
    return result is not None


def get_items(connection) -> [Item]:
    sql = '''SELECT * FROM item'''
    cur = connection.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    items = []
    for row in result:
        items.append(Item(row[0], row[1]))
    return items


def get_items_with_quantity(connection) -> [(Item, int)]:
    sql = '''SELECT i.code, i.name, SUM(ii.quantity) FROM item i
             LEFT JOIN item_import ii ON i.code = ii.item_code
             GROUP BY i.code'''
    cur = connection.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    items = []
    for row in result:
        items.append((Item(row[0], row[1]), row[2] if row[2] else 0))
    return items


def search_items_with_quantity_by_price(connection, price) -> [(Item, int)]:
    sql = '''SELECT i.code, i.name, SUM(ii.quantity) FROM item i
             LEFT JOIN item_import ii ON i.code = ii.item_code
             WHERE ii.price = ?
             GROUP BY i.code'''
    cur = connection.cursor()
    cur.execute(sql, (price,))
    result = cur.fetchall()
    items = []
    for row in result:
        items.append((Item(row[0], row[1]), row[2] if row[2] else 0))
    return items


def update_item(connection, item: Item):
    sql = '''UPDATE item SET name = ? WHERE code = ?'''
    cur = connection.cursor()
    cur.execute(sql, (item.name, item.code))
    connection.commit()


def delete_item(connection, code):
    sql = '''DELETE FROM item WHERE code = ?'''
    cur = connection.cursor()
    cur.execute(sql, (code,))
    connection.commit()


def insert_item_import(connection, item_import: ItemImport) -> ItemImport:
    sql = '''INSERT INTO item_import(item_code, quantity, price, import_date)
             VALUES(?, ?, ?, ?)'''
    cur = connection.cursor()
    cur.execute(sql, (item_import.item_code, item_import.quantity, item_import.price, item_import.import_date))
    connection.commit()
    id = cur.lastrowid
    return ItemImport(id, item_import.item_code, item_import.quantity, item_import.price, item_import.import_date)


def get_item_import_by_id(connection, import_id) -> ItemImport | None:
    sql = '''SELECT * FROM item_import WHERE import_id = ?'''
    cur = connection.cursor()
    cur.execute(sql, (import_id,))
    result = cur.fetchone()
    if result:
        return ItemImport(result[0], result[1], result[2], result[3], result[4])
    return None


def get_item_imports(connection) -> [ItemImport]:
    sql = '''SELECT * FROM item_import'''
    cur = connection.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    item_imports = []
    for row in result:
        item_imports.append(ItemImport(row[0], row[1], row[2], row[3], row[4]))
    return item_imports


def get_item_imports_by_item_code(connection, item_code: ItemImport) -> [ItemImport]:
    sql = '''SELECT * FROM item_import WHERE item_code = ?'''
    cur = connection.cursor()
    cur.execute(sql, (item_code,))
    result = cur.fetchall()
    item_imports = []
    for row in result:
        item_imports.append(ItemImport(row[0], row[1], row[2], row[3], row[4]))
    return item_imports


def update_item_import(connection, item_import: ItemImport):
    sql = '''UPDATE item_import SET quantity = ?, price = ?, import_date = ? WHERE import_id = ?'''
    cur = connection.cursor()
    cur.execute(sql, (item_import.quantity, item_import.price, item_import.import_date, item_import.import_id))
    connection.commit()


def delete_item_import(connection, import_id):
    sql = '''DELETE FROM item_import WHERE import_id = ?'''
    cur = connection.cursor()
    cur.execute(sql, (import_id,))
    connection.commit()
