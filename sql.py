from config import credentials as secrets
import mariadb


def sql_insert(date, activity_type, name, duration, intensity):
    print("inserting ", activity_type, " to database.")
    print(name)
    if (len(activity_type) > 0
            and len(name) > 0
            and len(duration) > 0
            and len(intensity) > 0):

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
    else:
        print("insertion failed")
        print(activity_type, name, date, duration, intensity)


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
        temp_list = []
        for item in data:
            temp_list.append(item)
        return_data.append(temp_list)

    conn.close()
    return return_data
