import mysql.connector


def query(sql):
    connection = mysql.connector.connect(host='localhost',
                                         db='test',
                                         charset='utf8mb4')
    cursor = connection.cursor()
    try:
        # with connection.cursor() as cursor:
        #     # Create a new record
        #     sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        #
        # cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
        #
        # # connection is not autocommit by default. So you must commit to save
        # # your changes.
        # connection.commit()

        # Read a single record
        cursor.execute(sql)
        """Returns all rows from a cursor as a list of dicts"""
        desc = cursor.description
        return [dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()]
    finally:
        cursor.close()
        connection.close()
