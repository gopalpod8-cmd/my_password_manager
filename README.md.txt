
---

# 🔐 Secure Local Password Manager

A lightweight, high-security password management system built with **Python**, **SQLite**, and **AES-256 Encryption**. This project is designed to provide a "Zero-Knowledge" environment for managing sensitive credentials locally.

---

## 🚀 Purpose

The primary goal of this system is to provide **Digital Sovereignty**. By moving password management away from cloud providers and into a local, encrypted database, users gain:

* **Zero-Knowledge Privacy:** The developer, the OS, and external entities have no way to see the passwords. Only the holder of the Master Password can unlock the data.
* **Security against Data Breaches:** Since the data is not on a central server, it cannot be leaked in a mass corporate hack.
* **Encouragement of Strong Credentials:** The built-in generator allows users to create unique, complex passwords for every service, eliminating the dangerous habit of password reuse.

---

## ⚙️ How It Works (Workflow)

The system operates on three main security pillars:

### 1. Key Derivation (The Lock)

When you enter your **Master Password**, the system does not store it. Instead:

* It combines your password with a unique, random **Salt**.
* It runs them through the **PBKDF2-HMAC-SHA256** algorithm.
* It performs **480,000 iterations** to stretch the password into a 32-byte cryptographic key. This makes "brute-force" attacks computationally expensive and impractical for hackers.

### 2. Encryption Engine (The Vault)

The system uses the **Fernet (AES-256-CBC)** authenticated encryption standard:

* **Adding:** Your plaintext password is encrypted into a non-human-readable "ciphertext" before hitting the disk.
* **Viewing:** The ciphertext is pulled from the database and decrypted back into plaintext only in the computer's volatile memory (RAM).

### 3. Local Database (The Storage)

All data is stored in `vault.db`, a local SQLite database.

* **Config Table:** Stores the Salt and a Hash of the Master Password for authentication.
* **Secrets Table:** Stores the Service name, Username, and the Encrypted Password blob.

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Encryption:** `cryptography` library (Fernet/AES-256)
* **Database:** SQLite3
* **Security Utilities:** `hashlib`, `os`, `getpass`

---

