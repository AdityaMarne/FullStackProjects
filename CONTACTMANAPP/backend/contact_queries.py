from db import get_connection

def get_all_contacts():
    conn = get_connection()
    cursor = conn.cursor(dictionary = True)
    cursor.execute("Select * from contacts")
    result = cursor.fetchall()
    conn.close()
    return result

def get_contact_by_id(contact_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary = True)
    cursor.execute("select * from contacts where id = %s", (contact_id))
    result =  cursor.fetchone()
    conn.close()
    return result

def create_contact(name, phone, email, address):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO contacts (name, phone, email, address) VALUES (%s, %s, %s, %s)",
        (name, phone, email, address)
    )
    conn.commit()
    conn.close()

def update_contact(contact_id, name, phone, email, address):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE contacts SET name=%s, phone=%s, email=%s, address=%s WHERE id=%s",
        (name, phone, email, address, contact_id)
    )
    conn.commit()
    conn.close()

def delete_contact(contact_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE id=%s", (contact_id))
    conn.commit()
    conn.close()

def search_contacts(query):
    conn = get_connection()
    cursor = conn.cursor(dictionary = True)
    like_query = f"%{query}%"
    cursor.execute("""
        SELECT * FROM contacts
        WHERE name LIKE %s OR phone LIKE %s OR email LIKE %s OR address LIKE %s
    """, (like_query, like_query, like_query, like_query))
    result = cursor.fetchall()
    conn.close()
    return result

