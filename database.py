import sqlite3

def get_connection():
    return sqlite3.connect("vault.db")

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    # config stores the salt and the hash of the master password
    cursor.execute('''CREATE TABLE IF NOT EXISTS config 
                      (salt BLOB, master_hash BLOB)''')
    # secrets stores the service details
    cursor.execute('''CREATE TABLE IF NOT EXISTS secrets 
                      (id INTEGER PRIMARY KEY, service TEXT, username TEXT, password TEXT)''')
    conn.commit()
    conn.close()