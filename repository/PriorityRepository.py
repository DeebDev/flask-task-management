import os
import psycopg2
from dotenv import load_dotenv
from db import db

from models.Priority import Priority

load_dotenv()

def db_conn():
    return psycopg2.connect(database=os.getenv('DB_NAME'), host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), port=os.getenv('DB_PORT'))

def get_priorities():
    priorities = db.session.query(Priority).all()
    return priorities

def get_priority_by_id(id):
    priority = db.session.query(Priority).filter_by(id=id).first()
    if priority is None:
        return None
    return priority

def create_priority(name, due_date_within):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''INSERT INTO proirities (name, due_date_within) VALUES (%s, %s) RETURNING id;''', (name, due_date_within))
    new_priority_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return new_priority_id

def update_priority(id, name, due_date_within):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''UPDATE proirities SET name = %s, due_date_within = %s WHERE id = %s RETURNING id;''', (name, due_date_within, id))
    update_priority = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return update_priority

def delete_priority(id):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''DELETE FROM proirities WHERE id = %s;''', (id,))
    conn.commit()
    cur.close()
    conn.close()