import psycopg2
from extras.const import NAME, HOST, USER, PSSW, PORT
from logs.logs import logExeption


def connect():
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(database=NAME,
                                host=HOST,
                                user=USER,
                                password=PSSW,
                                port=PORT)
        return conn, ""
    except Exception as e:
        logExeption(e, "init.connect")
        return conn, e


def saveFace(idPersona):
    """save faces in postgres"""
    date = None
    cve = None
    conn = None
    try:
        # connect to the PostgreSQL server
        conn, err = connect()
        if not conn:
            return err
        cur = conn.cursor()
        cur.execute(
            """SELECT * FROM identificacion WHERE persona=%s""", (idPersona,))
        rows = cur.fetchall()
        print(rows)
        date = rows[0][6]
        cve = rows[0][1]
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as e:
        logExeption(e, "dbConnection.saveFace")
    finally:
        if conn is not None:
            conn.close()
        return date, cve
