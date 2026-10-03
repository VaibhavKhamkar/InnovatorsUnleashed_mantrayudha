import sqlite3
import datetime
from pathlib import Path

DB_FILE = "mantrayudha.db"

def get_db():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create tables
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT
        );

        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            returnable_days INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        );

        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price INTEGER NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        );

        CREATE TABLE IF NOT EXISTS returns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_item_id INTEGER NOT NULL,
            return_date TEXT NOT NULL,
            status TEXT NOT NULL,
            refund_amount INTEGER,
            FOREIGN KEY (order_item_id) REFERENCES order_items (id)
        );

        CREATE TABLE IF NOT EXISTS support_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            issue_description TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        );
        
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            message TEXT NOT NULL,
            role TEXT NOT NULL,
            timestamp TEXT NOT NULL
        );
    ''')
    
    # Insert some mock data if empty
    cursor.execute("SELECT COUNT(*) FROM customers")
    if cursor.fetchone()[0] == 0:
        cursor.executescript('''
            INSERT INTO customers (name, email, phone) VALUES 
            ('Alice Smith', 'alice@example.com', '555-0101'),
            ('Bob Jones', 'bob@example.com', '555-0102');
            
            INSERT INTO products (name, price, returnable_days) VALUES 
            ('Laptop', 80000, 30),
            ('Headphones', 5000, 15),
            ('Mouse', 1500, 15);
            
            INSERT INTO orders (customer_id, order_date, status) VALUES 
            (1, '2026-09-01', 'Delivered'),
            (2, '2026-10-01', 'Processing');
            
            INSERT INTO order_items (order_id, product_id, quantity, price) VALUES 
            (1, 1, 1, 80000),
            (1, 2, 1, 5000),
            (2, 3, 2, 1500);
        ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
