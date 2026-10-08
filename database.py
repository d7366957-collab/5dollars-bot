"""
Gestión de base de datos SQLite
"""
import sqlite3
from datetime import datetime
from config import (
    DATABASE_PATH, ENTRY_PRICE, REFERRAL_COMMISSION,
    REFERRAL_REGISTRATION_FEE, BONUSES
)


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            balance REAL DEFAULT 0,
            referrer_id INTEGER,
            referral_code TEXT UNIQUE,
            wallet_address TEXT,
            total_registered INTEGER DEFAULT 0,
            total_active INTEGER DEFAULT 0,
            total_pending INTEGER DEFAULT 0,
            total_earned REAL DEFAULT 0,
            total_withdrawn REAL DEFAULT 0,
            total_bonuses REAL DEFAULT 0,
            has_deposited INTEGER DEFAULT 0,
            is_banned INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS deposits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket TEXT UNIQUE,
            user_id INTEGER,
            amount REAL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            approved_at TIMESTAMP,
            approved_by INTEGER
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS withdrawals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket TEXT UNIQUE,
            user_id INTEGER,
            amount REAL,
            wallet TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            paid_at TIMESTAMP,
            paid_by INTEGER
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS commissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            from_user_id INTEGER,
            amount REAL,
            type TEXT DEFAULT 'deposit',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS bonuses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            referrals_count INTEGER,
            amount REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada")


# ============ USUARIOS ============

def get_user(user_id):
    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return user


def create_user(user_id, username, first_name, referrer_id=None, referral_code=None):
    conn = get_connection()
    
    if not referral_code:
        referral_code = f"REF{user_id}"
    
    try:
        conn.execute("""
            INSERT INTO users (id, username, first_name, referrer_id, referral_code)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, username, first_name, referrer_id, referral_code))
        conn.commit()
        print(f"✅ Usuario creado: {user_id}")
    except sqlite3.IntegrityError:
        print(f"⚠️ Usuario ya existe: {user_id}")
    
    conn.close()
    return get_user(user_id)


def update_user(user_id, **kwargs):
    conn = get_connection()
    fields = ", ".join([f"{k} = ?" for k in kwargs.keys()])
    values = list(kwargs.values()) + [user_id]
    conn.execute(f"UPDATE users SET {fields} WHERE id = ?", values)
    conn.commit()
    conn.close()


def add_balance(user_id, amount):
    conn = get_connection()
    conn.execute("""
        UPDATE users 
        SET balance = balance + ?,
            total_earned = total_earned + ?
        WHERE id = ?
    """, (amount, amount, user_id))
    conn.commit()
    conn.close()


def get_user_by_referral_code(code):
    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE referral_code = ?", (code,)).fetchone()
    conn.close()
    return user


# ============ DEPÓSITOS ============

def create_deposit(user_id, amount, ticket):
    conn = get_connection()
    conn.execute("""
        INSERT INTO deposits (ticket, user_id, amount)
        VALUES (?, ?, ?)
    """, (ticket, user_id, amount))
    conn.commit()
    conn.close()


def get_pending_deposits():
    conn = get_connection()
    deposits = conn.execute("""
        SELECT d.*, u.username, u.first_name
        FROM deposits d
        JOIN users u ON d.user_id = u.id
        WHERE d.status = 'pending'
        ORDER BY d.created_at ASC
    """).fetchall()
    conn.close()
    return deposits


def approve_deposit(ticket, admin_id):
    conn = get_connection()
    deposit = conn.execute("SELECT * FROM deposits WHERE ticket = ?", (ticket,)).fetchone()
    
    if not deposit:
        conn.close()
        return None
    
    conn.execute("""
        UPDATE deposits 
        SET status = 'approved',
            approved_at = CURRENT_TIMESTAMP,
            approved_by = ?
        WHERE ticket = ?
    """, (admin_id, ticket))
    
    conn.execute("""
        UPDATE users 
        SET has_deposited = 1
        WHERE id = ?
    """, (deposit['user_id'],))
    
    conn.commit()
    conn.close()
    
    process_referral_commission(deposit['user_id'])
    
    return deposit


def reject_deposit(ticket, admin_id):
    conn = get_connection()
    conn.execute("""
        UPDATE deposits 
        SET status = 'rejected',
            approved_at = CURRENT_TIMESTAMP,
            approved_by = ?
        WHERE ticket = ?
    """, (admin_id, ticket))
    conn.commit()
    conn.close()


# ============ COMISIONES ============

def process_referral_registration(user_id):
    """Procesa la comisión de $0.05 cuando alguien se registra"""
    user = get_user(user_id)
    
    if not user or not user['referrer_id']:
        return
    
    referrer = get_user(user['referrer_id'])
    
    if not referrer:
        return
    
    conn = get_connection()
    
    conn.execute("""
        UPDATE users 
        SET balance = balance + ?,
            total_earned = total_earned + ?,
            total_registered = total_registered + 1,
            total_pending = total_pending + 1
        WHERE id = ?
    """, (REFERRAL_REGISTRATION_FEE, REFERRAL_REGISTRATION_FEE, referrer['id']))
    
    conn.execute("""
        INSERT INTO commissions (user_id, from_user_id, amount, type)
        VALUES (?, ?, ?, 'registration')
    """, (referrer['id'], user_id, REFERRAL_REGISTRATION_FEE))
    
    conn.commit()
    conn.close()
    
    return referrer


def process_referral_commission(user_id):
    """Procesa la comisión de $3.00 cuando un referido deposita"""
    user = get_user(user_id)
    
    if not user or not user['referrer_id']:
        return
    
    referrer = get_user(user['referrer_id'])
    
    if not referrer:
        return
    
    if not referrer['has_deposited']:
        return
    
    conn = get_connection()
    
    conn.execute("""
        UPDATE users 
        SET balance = balance + ?,
            total_earned = total_earned + ?,
            total_active = total_active + 1,
            total_pending = total_pending - 1
        WHERE id = ?
    """, (REFERRAL_COMMISSION, REFERRAL_COMMISSION, referrer['id']))
    
    conn.execute("""
        INSERT INTO commissions (user_id, from_user_id, amount, type)
        VALUES (?, ?, ?, 'deposit')
    """, (referrer['id'], user_id, REFERRAL_COMMISSION))
    
    conn.commit()
    conn.close()
    
    check_bonuses(referrer['id'])
    
    return referrer


def check_bonuses(user_id):
    user = get_user(user_id)
    
    if not user or not user['has_deposited']:
        return None
    
    active = user['total_active']
    
    for required, amount in sorted(BONUSES.items()):
        if active >= required:
            conn = get_connection()
            existing = conn.execute("""
                SELECT * FROM bonuses 
                WHERE user_id = ? AND referrals_count = ?
            """, (user_id, required)).fetchone()
            
            if not existing:
                conn.execute("""
                    INSERT INTO bonuses (user_id, referrals_count, amount)
                    VALUES (?, ?, ?)
                """, (user_id, required, amount))
                
                conn.execute("""
                    UPDATE users 
                    SET balance = balance + ?,
                        total_earned = total_earned + ?,
                        total_bonuses = total_bonuses + ?
                    WHERE id = ?
                """, (amount, amount, amount, user_id))
                
                conn.commit()
                conn.close()
                print(f"🎁 Bono ${amount} otorgado a {user_id}")
                return (required, amount)
            
            conn.close()
    
    return None


def get_commissions(user_id):
    conn = get_connection()
    commissions = conn.execute("""
        SELECT c.*, u.username 
        FROM commissions c
        JOIN users u ON c.from_user_id = u.id
        WHERE c.user_id = ?
        ORDER BY c.created_at DESC
    """, (user_id,)).fetchall()
    conn.close()
    return commissions


def get_referrals(user_id):
    conn = get_connection()
    referrals = conn.execute("""
        SELECT id, username, has_deposited, created_at
        FROM users
        WHERE referrer_id = ?
        ORDER BY created_at DESC
    """, (user_id,)).fetchall()
    conn.close()
    return referrals


# ============ RETIROS ============

def create_withdrawal(user_id, amount, wallet, ticket):
    conn = get_connection()
    conn.execute("""
        INSERT INTO withdrawals (ticket, user_id, amount, wallet)
        VALUES (?, ?, ?, ?)
    """, (ticket, user_id, amount, wallet))
    conn.commit()
    conn.close()


def get_pending_withdrawals():
    conn = get_connection()
    withdrawals = conn.execute("""
        SELECT w.*, u.username, u.first_name, u.balance
        FROM withdrawals w
        JOIN users u ON w.user_id = u.id
        WHERE w.status = 'pending'
        ORDER BY w.created_at ASC
    """).fetchall()
    conn.close()
    return withdrawals


def approve_withdrawal(ticket, admin_id):
    conn = get_connection()
    withdrawal = conn.execute("SELECT * FROM withdrawals WHERE ticket = ?", (ticket,)).fetchone()
    
    if not withdrawal:
        conn.close()
        return None
    
    conn.execute("""
        UPDATE withdrawals 
        SET status = 'paid',
            paid_at = CURRENT_TIMESTAMP,
            paid_by = ?
        WHERE ticket = ?
    """, (admin_id, ticket))
    
    conn.execute("""
        UPDATE users 
        SET balance = balance - ?,
            total_withdrawn = total_withdrawn + ?
        WHERE id = ?
    """, (withdrawal['amount'], withdrawal['amount'], withdrawal['user_id']))
    
    conn.commit()
    conn.close()
    return withdrawal


def reject_withdrawal(ticket, admin_id):
    conn = get_connection()
    conn.execute("""
        UPDATE withdrawals 
        SET status = 'rejected',
            paid_at = CURRENT_TIMESTAMP,
            paid_by = ?
        WHERE ticket = ?
    """, (admin_id, ticket))
    conn.commit()
    conn.close()


def get_withdrawals(user_id):
    conn = get_connection()
    withdrawals = conn.execute("""
        SELECT * FROM withdrawals
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,)).fetchall()
    conn.close()
    return withdrawals


# ============ DEPÓSITOS AUTOMÁTICOS ============

def link_wallet_to_user(user_id, wallet):
    """Vincula wallet al usuario"""
    conn = get_connection()
    conn.execute("UPDATE users SET wallet_address = ? WHERE id = ?", (wallet, user_id))
    conn.commit()
    conn.close()


def get_user_by_wallet(wallet):
    """Busca usuario por wallet"""
    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE wallet_address = ?", (wallet,)).fetchone()
    conn.close()
    return user


def create_auto_deposit(user_id, amount, tx_hash):
    """Crea depósito automático"""
    ticket = f"AUTO-{tx_hash}"
    
    conn = get_connection()
    try:
        conn.execute("""
            INSERT INTO deposits (ticket, user_id, amount, status)
            VALUES (?, ?, ?, 'pending')
        """, (ticket, user_id, amount))
        conn.commit()
        conn.close()
        return ticket
    except sqlite3.IntegrityError:
        conn.close()
        return None


# ============ ESTADÍSTICAS ============

def get_global_stats():
    conn = get_connection()
    
    total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    active_users = conn.execute("SELECT COUNT(*) FROM users WHERE has_deposited = 1").fetchone()[0]
    free_users = conn.execute("SELECT COUNT(*) FROM users WHERE has_deposited = 0").fetchone()[0]
    total_deposits = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM deposits WHERE status = 'approved'").fetchone()[0]
    total_withdrawals = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM withdrawals WHERE status = 'paid'").fetchone()[0]
    total_balance = conn.execute("SELECT COALESCE(SUM(balance), 0) FROM users").fetchone()[0]
    pending_deposits = conn.execute("SELECT COUNT(*) FROM deposits WHERE status = 'pending'").fetchone()[0]
    pending_withdrawals = conn.execute("SELECT COUNT(*) FROM withdrawals WHERE status = 'pending'").fetchone()[0]
    
    conn.close()
    
    return {
        'total_users': total_users,
        'active_users': active_users,
        'free_users': free_users,
        'total_deposits': total_deposits,
        'total_withdrawals': total_withdrawals,
        'total_balance': total_balance,
        'pending_deposits': pending_deposits,
        'pending_withdrawals': pending_withdrawals,
    }


def get_ranking(limit=50):
    conn = get_connection()
    ranking = conn.execute("""
        SELECT id, username, total_active, total_earned
        FROM users
        WHERE has_deposited = 1
        ORDER BY total_active DESC, total_earned DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return ranking
