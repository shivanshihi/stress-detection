import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='newknife',
        database='stress_detection_db'
    )

def insert_result(user_id, stress_level):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO stress_results (user_id, stress_level) VALUES (%s, %s)",
        (user_id, stress_level)
    )
    conn.commit()
    conn.close()

