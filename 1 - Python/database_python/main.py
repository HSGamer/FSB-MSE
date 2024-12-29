from dao import create_connection, create_table
from gui import App

if __name__ == '__main__':
    db_file = 'store_management.db'
    db_file_exists = False
    try:
        with open(db_file):
            db_file_exists = True
    except FileNotFoundError:
        db_file_exists = False
    conn = create_connection(db_file)
    if not db_file_exists:
        create_table(conn)

    app = App(conn)
    app.mainloop()

    conn.close()
