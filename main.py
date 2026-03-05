import sys
import getpass
from database import init_db, get_connection
from security_utils import derive_key, generate_salt, hash_password, generate_strong_password

def setup():
    init_db()
    conn = get_connection()
    res = conn.execute("SELECT salt, master_hash FROM config").fetchone()
    
    if res is None:
        print("--- Welcome! Let's set up your secure vault ---")
        mp = getpass.getpass("Create a strong Master Password: ")
        salt = generate_salt()
        m_hash = hash_password(mp, salt)
        conn.execute("INSERT INTO config (salt, master_hash) VALUES (?, ?)", (salt, m_hash))
        conn.commit()
        print("\nVault created! Please restart the app to login.")
        conn.close()
        sys.exit()
    conn.close()
    return res # salt, master_hash

def login(stored_salt, stored_hash):
    attempt = getpass.getpass("Enter Master Password: ")
    if hash_password(attempt, stored_salt) == stored_hash:
        print("\n[ACCESS GRANTED]")
        return derive_key(attempt, stored_salt)
    else:
        print("\n[ACCESS DENIED] Incorrect password.")
        sys.exit()

def add_entry(fernet):
    service = input("Service (e.g., GitHub): ")
    user = input("Username: ")
    
    choice = input("Generate a random password? (y/n): ")
    if choice.lower() == 'y':
        pwd = generate_strong_password()
        print(f"Generated Password: {pwd}")
    else:
        pwd = getpass.getpass("Enter password to store: ")
        
    encrypted_pwd = fernet.encrypt(pwd.encode()).decode()
    
    conn = get_connection()
    conn.execute("INSERT INTO secrets (service, username, password) VALUES (?, ?, ?)", 
                 (service, user, encrypted_pwd))
    conn.commit()
    conn.close()
    print(f"Successfully saved {service}!\n")

def view_entries(fernet):
    conn = get_connection()
    cursor = conn.execute("SELECT id, service, username, password FROM secrets")
    rows = cursor.fetchall()
    
    if not rows:
        print("\nVault is empty.")
    else:
        print("\n" + "="*50)
        for row in rows:
            decrypted = fernet.decrypt(row[3].encode()).decode()
            print(f"ID: {row[0]} | Service: {row[1]} | User: {row[2]} | Pass: {decrypted}")
        print("="*50 + "\n")
    conn.close()

def delete_entry():
    target_id = input("Enter the ID to delete: ")
    conn = get_connection()
    cursor = conn.execute("SELECT service FROM secrets WHERE id=?", (target_id,))
    row = cursor.fetchone()
    
    if row:
        confirm = input(f"Delete {row[0]}? (y/n): ")
        if confirm.lower() == 'y':
            conn.execute("DELETE FROM secrets WHERE id=?", (target_id,))
            conn.commit()
            print("Deleted.")
    else:
        print("ID not found.")
    conn.close()

def main():
    salt, m_hash = setup()
    fernet = login(salt, m_hash)
    
    while True:
        print("\n--- VAULT MENU ---")
        print("1. Add Password")
        print("2. View All")
        print("3. Delete Entry")
        print("4. Exit")
        
        choice = input("Selection: ")
        if choice == "1":
            add_entry(fernet)
        elif choice == "2":
            view_entries(fernet)
        elif choice == "3":
            delete_entry()
        elif choice == "4":
            print("Vault locked. Goodbye!")
            break

if __name__ == "__main__":
    main()