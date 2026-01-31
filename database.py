import sqlite3
import datetime
from config import DB_NAME

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Products table
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE NOT NULL,
            name TEXT,
            last_price REAL,
            currency TEXT DEFAULT 'TL',
            last_checked TIMESTAMP
        )
    ''')
    
    # Price history table
    c.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            price REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Veritabanı '{DB_NAME}' başarıyla başlatıldı/kontrol edildi.")

def update_price(url, name, price):
    conn = get_db_connection()
    c = conn.cursor()
    
    # Check if product exists
    c.execute('SELECT id, last_price FROM products WHERE url = ?', (url,))
    product = c.fetchone()
    
    current_time = datetime.datetime.now()
    
    if product:
        product_id = product['id']
        old_price = product['last_price']
        
        # Update product info
        c.execute('''
            UPDATE products 
            SET name = ?, last_price = ?, last_checked = ? 
            WHERE id = ?
        ''', (name, price, current_time, product_id))
        
        # Log history
        c.execute('''
            INSERT INTO price_history (product_id, price, timestamp)
            VALUES (?, ?, ?)
        ''', (product_id, price, current_time))
        
        conn.commit()
        conn.close()
        return old_price
    else:
        # New product
        c.execute('''
            INSERT INTO products (url, name, last_price, last_checked)
            VALUES (?, ?, ?, ?)
        ''', (url, name, price, current_time))
        product_id = c.lastrowid
        
        # Log history
        c.execute('''
            INSERT INTO price_history (product_id, price, timestamp)
            VALUES (?, ?, ?)
        ''', (product_id, price, current_time))
        
        conn.commit()
        conn.close()
        return None # No old price
