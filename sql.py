from config import credentials as secrets
import mariadb


class SqlManipulator:
    def __init__(self):
        self.db_host = secrets['mysql']['host']
        self.db_username = secrets['mysql']['username']
        self.db_password = secrets['mysql']['password']
        self.db_name = secrets['mysql']['database']

    def sql_insert(self, date, activity_type, name, duration, intensity):
        print("inserting ", activity_type, " to database.")

        if (len(activity_type) > 0
                and len(name) > 0
                and duration > 0
                and len(intensity) > 0):

            conn = mariadb.connect(host=self.db_host,
                                   user=self.db_username,
                                   passwd=self.db_password,
                                   database="training")

            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO test values("
                "'{date}', "
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

    def sql_remove_workout(self, workout_details):
        print("test: ", workout_details)

        conn = mariadb.connect(host=self.db_host,
                               user=self.db_username,
                               passwd=self.db_password,
                               database="training")

        cursor = conn.cursor()
        statement = "DELETE from test WHERE (date=%s and activity_type=%s and duration=%s)"
        query_term = (workout_details[0], workout_details[1], workout_details[3],)
        cursor.execute(statement, query_term)

        conn.commit()
        conn.close()

    def sql_retrieve(self, date):
        return_data = []

        conn = mariadb.connect(host=self.db_host,
                               user=self.db_username,
                               passwd=self.db_password,
                               database="training")

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
