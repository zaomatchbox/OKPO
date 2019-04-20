from sqlite3 import connect
import os


def update(item_name, new_name):
    new_name = new_name.strip()
    sql = f"UPDATE goods SET name = '{new_name}' where name = '{item_name}';"
    print('SQL', sql)

    db_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'db.sqlite3')
    with connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        get_sql = f"SELECT name FROM goods WHERE name = '{new_name}';"
        cursor.execute(get_sql)
        results = cursor.fetchall()
    print('RESULTS', results)
    return [r[0] for r in results][0]


def search():
    sql = f'SELECT name FROM goods;'
    db_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'db.sqlite3')
    with connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
    print('RESULTS', results)
    return [r[0] for r in results]
