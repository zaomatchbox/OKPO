import psycopg2

DATABASE = 'abacaba'
USER_NAME = 'docker'
HOST = '192.168.100.2'  # for swarm mode


def get_connection():
    conn = psycopg2.connect(
        dbname=DATABASE,
        user=USER_NAME,
        host=HOST
    )

    cursor = conn.cursor()
    return cursor


def get_all_users(conn):
    get_tables = '''SELECT USERNAME FROM accounts'''
    conn.execute(get_tables)
    for row in conn:
        print(row)


def get_by_password(conn, password):
    get_tables = "SELECT username FROM accounts WHERE user_id = {}".format(password)
    print(get_tables)
    conn.execute(get_tables)
    for row in conn:
        print(row)


if __name__ == "__main__":
    conn = get_connection()
    get_all_users(conn)
    get_by_password(conn, 1)
    get_by_password(conn, 123)
    get_by_password(conn, '105 OR 1=1')
