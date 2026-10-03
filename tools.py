import sqlite3
import datetime

# --- Tool Functions ---

def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def _query(db: sqlite3.Connection, query: str, args=(), one=False):
    db.row_factory = _dict_factory
    cur = db.execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv

def get_customer(db: sqlite3.Connection, email: str = None, phone: str = None):
    if email:
        return _query(db, "SELECT * FROM customers WHERE email = ?", (email,), one=True)
    if phone:
        return _query(db, "SELECT * FROM customers WHERE phone = ?", (phone,), one=True)
    return None

def get_order(db: sqlite3.Connection, order_id: int):
    order = _query(db, "SELECT * FROM orders WHERE id = ?", (order_id,), one=True)
    if not order:
        return None
    items = _query(db, "SELECT * FROM order_items WHERE order_id = ?", (order_id,))
    order['items'] = items
    return order

def get_product(db: sqlite3.Connection, product_id: int):
    return _query(db, "SELECT * FROM products WHERE id = ?", (product_id,), one=True)

def get_conversations(db: sqlite3.Connection, customer_id: int):
    return _query(db, "SELECT * FROM conversations WHERE customer_id = ? ORDER BY timestamp DESC LIMIT 10", (customer_id,))

def check_refund_eligibility(db: sqlite3.Connection, order_item_id: int):
    item = _query(db, "SELECT oi.*, p.returnable_days, o.order_date FROM order_items oi JOIN products p ON oi.product_id = p.id JOIN orders o ON oi.order_id = o.id WHERE oi.id = ?", (order_item_id,), one=True)
    if not item:
        return {"eligible": False, "reason": "Item not found"}
    
    order_date = datetime.datetime.strptime(item['order_date'], "%Y-%m-%d").date()
    # For hackathon, assume today is 2026-10-03
    today = datetime.date(2026, 10, 3)
    days_since = (today - order_date).days
    
    if days_since <= item['returnable_days']:
        return {"eligible": True, "reason": f"Within {item['returnable_days']} days return policy."}
    else:
        return {"eligible": False, "reason": f"Exceeded {item['returnable_days']} days return policy. Ordered {days_since} days ago."}

def calculate_refund(db: sqlite3.Connection, order_item_id: int):
    item = _query(db, "SELECT * FROM order_items WHERE id = ?", (order_item_id,), one=True)
    if not item:
        return {"amount": 0, "error": "Item not found"}
    return {"amount": item['price'] * item['quantity']}

def create_return(db: sqlite3.Connection, order_item_id: int):
    eligibility = check_refund_eligibility(db, order_item_id)
    if not eligibility['eligible']:
        return {"success": False, "message": eligibility['reason']}
    
    today_str = "2026-10-03"
    db.execute("INSERT INTO returns (order_item_id, return_date, status, refund_amount) VALUES (?, ?, ?, ?)", (order_item_id, today_str, 'Pending', 0))
    db.commit()
    return {"success": True, "message": "Return initiated."}

def create_refund(db: sqlite3.Connection, order_item_id: int):
    eligibility = check_refund_eligibility(db, order_item_id)
    if not eligibility['eligible']:
        return {"success": False, "message": eligibility['reason']}
        
    amount = calculate_refund(db, order_item_id)['amount']
    today_str = "2026-10-03"
    db.execute("INSERT INTO returns (order_item_id, return_date, status, refund_amount) VALUES (?, ?, ?, ?)", (order_item_id, today_str, 'Refunded', amount))
    db.commit()
    return {"success": True, "message": f"Refund of {amount} INR processed."}

def create_support_ticket(db: sqlite3.Connection, customer_id: int, issue_description: str):
    db.execute("INSERT INTO support_tickets (customer_id, issue_description, status) VALUES (?, ?, ?)", (customer_id, issue_description, 'Open'))
    db.commit()
    return {"success": True, "message": "Support ticket created."}

def escalate_to_human(db: sqlite3.Connection, customer_id: int, reason: str):
    return create_support_ticket(db, customer_id, f"ESCALATED: {reason}")
