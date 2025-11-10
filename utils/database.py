# koneksi MySQL
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=int(os.getenv("DB_PORT"))
)
cursor = db.cursor()

def close_connection():
    cursor.close()
    db.close()

# Mengecek koneksi database ke Python
#if db.is_connected():
#   print("berhasil.")

# Buat database
# cursor.execute("CREATE DATABASE game_adventure")
# print("Database berhasil dibuat")

# Buat tabel dalam database
# 1. Tabel user
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         username VARCHAR(100) NOT NULL UNIQUE,
#         password_hash VARCHAR(255) NOT NULL
#     )
# ''')

# # 2. Tabel karakter dalam game
# cursor.execute('''
#     CREATE TABLE characters (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT NOT NULL,
#     class_name VARCHAR(50),
#     hp INT,
#     energy INT,
#     defense INT,
#     damage INT,
#     gold INT DEFAULT 0,
#     exp INT DEFAULT 0,
#     floor INT DEFAULT 1,
#     title VARCHAR(100) DEFAULT 'Novice',
#     score INT DEFAULT 0
# );
# ''')

# # 3. Tabel Inventory
# cursor.execute('''
#     CREATE TABLE inventory_items (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         character_id INT NOT NULL,
#         item_name VARCHAR(100) NOT NULL,
#         quantity INT DEFAULT 1,
#         FOREIGN KEY (character_id) REFERENCES characters(id) ON DELETE CASCADE
#     );
# ''')