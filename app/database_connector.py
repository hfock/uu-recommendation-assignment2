import psycopg2


def establish_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="bbc",
        user="postgres",
        password="postgres")

    return conn


def create_tables():
    ## https://www.postgresqltutorial.com/postgresql-python/create-tables/
    """ create tables in the PostgreSQL database"""
    commands = (
        """
            DROP TABLE IF EXISTS users;
        """
        """
            DROP TABLE IF EXISTS personas;
        """,
        """ CREATE TABLE IF NOT EXISTS personas(
                persona_id serial PRIMARY KEY,
                name VARCHAR ( 50 ) UNIQUE NOT NULL
            );
        """,
        """
            CREATE TABLE IF NOT EXISTS users(
                user_id serial PRIMARY KEY,
                username VARCHAR ( 50 ) UNIQUE NOT NULL,
                password VARCHAR ( 50 ) NOT NULL,
                email VARCHAR ( 255 ) UNIQUE NOT NULL,
                created_on TIMESTAMP NOT NULL,
                last_login TIMESTAMP,
                persona_id INT,
                FOREIGN KEY (persona_id) REFERENCES personas(persona_id)
            );  
        """)

    conn = None
    try:
        # connect to the PostgreSQL server
        conn = establish_connection()
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    conn = create_tables()
