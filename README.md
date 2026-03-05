

### **Project: Secure Local Password Manager**

### **1. Purpose**

The purpose of this project is to create a **Zero-Knowledge** security tool. Unlike cloud-based managers, this system keeps your sensitive data entirely on your local hardware.

* **Privacy:** No third-party company has access to your keys.
* **Security:** It protects against data breaches by ensuring your "vault" never travels over the internet.
* **Control:** You are the sole owner of the encryption logic and the physical database.

### **2. Workflow**

The system uses a professional-grade cryptographic pipeline:

1. **Authentication:** Upon startup, the user enters a Master Password.
2. **Key Stretching:** The system uses **PBKDF2-HMAC-SHA256** with a unique salt to turn that password into a strong 32-byte key.
3. **The Vault:**
* **Encryption:** New entries are scrambled into ciphertext using **AES-256 (Fernet)**.
* **Decryption:** Stored entries are unlocked only in the computer's temporary memory (RAM) when requested.


4. **Storage:** All data is housed in a local **SQLite database** (`vault.db`), which is automatically excluded from GitHub for safety.

---



You have built a fully functional security application from scratch and successfully mastered Git version control.

**Would you like me to show you how to add a "Password Strength Meter" so the app can tell you if a password you type is too weak?**
