from sqlite3 import connect
import os


def search(login, password):
    sql = f"SELECT 1 FROM auth_user WHERE username = '{login}' AND password = hex('{password}');"
    print('SQL', sql)

    db_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'db.sqlite3')
    with connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
    return len(results) > 0
