import psycopg2


class Connector:
    """
    Encapsulates a database connection
    """
    db_connection: any = None

    def cursor(self):
        return self.db_connection.cursor()

    def close(self):
        self.db_connection.close()

    def commit(self):
        self.db_connection.commit()


class PostgreSQLConnector(Connector):
    def __init__(self):
        try:
            self.db_connection = psycopg2.connect(
                database='postgres',
                user='postgres',
                password='postgres',
                host='sensorhub-postgresql.c5jrbbbr7rhi.us-east-2.rds.amazonaws.com',
                port='5432'
            )
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            if self.db_connection is not None:
                self.db_connection.close()


class SQLiteConnector(Connector):
    def __init__(self):
        pass
