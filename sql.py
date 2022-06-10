from config import credentials as secrets
import mariadb


def sql_insert(date, activity_type, name, duration, intensity):
    db_host = secrets['mysql']['host']
    db_username = secrets['mysql']['username']
    db_password = secrets['mysql']['password']
    db_name = secrets['mysql']['database']

    conn = mariadb.connect(host=db_host,
                           user=db_username,
                           passwd=db_password,
                           database="training")

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO test values('{date}', "
        "'{activity_type}', "
        "'{name}', "
        "'{duration}', "
        "'{intensity}');".format(date=date,
                                 activity_type=activity_type,
                                 name=name,
                                 duration=duration,
                                 intensity=intensity
                                 )
    )

    conn.commit()
    conn.close()


def sql_retrieve(date):
    return_data = []
    db_host = secrets['mysql']['host']
    db_username = secrets['mysql']['username']
    db_password = secrets['mysql']['password']
    db_name = secrets['mysql']['database']

    conn = mariadb.connect(host=db_host, user=db_username, passwd=db_password, database="training")
    cursor = conn.cursor()
    statement = "SELECT * from test WHERE date=%s"
    query_term = (date,)
    cursor.execute(statement, query_term)

    for data in cursor:
        for item in data:
            return_data.append(item)

    conn.close()
    return return_data
