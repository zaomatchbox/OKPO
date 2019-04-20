from sqlite3 import connect
import os


def search(term=''):
    q = term.strip()
    if q:
        search_term = f"WHERE name LIKE '%{q}%'"
    else:
        search_term = ''

    sql = f'SELECT name FROM orders_item {search_term};'
    print('SQL', sql)

    db_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'db.sqlite3')
    with connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
    print('RESULTS', results)
    return [r[0] for r in results]
