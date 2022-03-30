import psycopg2
from config import config
from datetime import datetime


def insert_user(username, password, email):
    """ insert a new vendor into the vendors table """
    sql = """INSERT INTO users(username, password, email)
                 VALUES(%s) RETURNING user_id;"""
    conn = None
    user_id = None

    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (username, password, email))
        # get the generated id back
        user_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return user_id


if __name__ == '__main__':
    insert_user('Focktastic', 'pwd', 'h@fock.com')