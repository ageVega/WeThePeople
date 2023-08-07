# admin.py
from .connection import get_connection
from psycopg2 import extras
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

# Definición de la clase usuario
class Admin(UserMixin):
    def __init__(self, id, nickname, password):
        self.id = id
        self.nickname = nickname
        self.password = password
        
    def check_password(self, password):
        return check_password_hash(self.password, password)


# Funcion para conseguir un cursor
def get_cursor():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    return conn, cur

# Funcion para cerrar conexion y cursor
def close_connection_and_cursor(conn, cur):
    cur.close()
    conn.close()

def get_admin_by_id(admin_id):
    conn, cur = get_cursor()
    cur.execute("SELECT * FROM admins WHERE id = %s", (admin_id,))
    admin_data = cur.fetchone()
    close_connection_and_cursor(conn, cur)

    if admin_data:
        return Admin(id=admin_data['id'], nickname=admin_data['nickname'], password=admin_data['password'])
    return None

def get_admin_by_nickname(nickname):
    conn, cur = get_cursor()
    cur.execute("SELECT * FROM admins WHERE nickname = %s", (nickname,))
    admin_data = cur.fetchone()
    close_connection_and_cursor(conn, cur)

    if admin_data:
        return Admin(id=admin_data['id'], nickname=admin_data['nickname'], password=admin_data['password'])
    return None

def create_admin(nickname, password):
    conn, cur = get_cursor()
    password_hash = generate_password_hash(password)

    try:
        cur.execute("INSERT INTO admins (nickname, password) VALUES (%s, %s)", (nickname, password_hash))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error creating admin: {str(e)}")
        return None
    finally:
        close_connection_and_cursor(conn, cur)

def delete_admin(admin_id):
    conn, cur = get_cursor()

    try:
        cur.execute("DELETE FROM admins WHERE id = %s", (admin_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error deleting admin: {str(e)}")
        return None
    finally:
        close_connection_and_cursor(conn, cur)
