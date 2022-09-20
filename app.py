#!/usr/bin/env python

#https://github.com/psycopg/psycopg2/issues/261

import psycopg2

ISOLEVEL = psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT

import time

user = 'test-user'
password = 'testpassword123'

host = '10.9.98.25'
port = '5432'
database = 'test-db'
LIMIT_RETRIES = 5

class DB():
    def __init__(self, user, password, host, port, database, reconnect):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self._connection = None
        self._cursor = None
        self.reconnect = reconnect
        self.init()

    def connect(self,retry_counter=0):
        if not self._connection:
            try:
                self._connection = psycopg2.connect(user = self.user, password = self.password, host = self.host, port = self.port, database = self.database, connect_timeout=3, )
                retry_counter = 0
                self._connection.autocommit = False
                return self._connection
            except psycopg2.OperationalError as error:
                if not self.reconnect or retry_counter >= LIMIT_RETRIES:
                    raise error
                else:
                    retry_counter += 1
                    print("got error {}. reconnecting {}".format(str(error).strip(), retry_counter))
                    time.sleep(5)
                    self.connect(retry_counter)
            except (Exception, psycopg2.Error) as error:
                raise error

    def cursor(self):
        if not self._cursor or self._cursor.closed:
            if not self._connection:
                self.connect()
            self._cursor = self._connection.cursor()
            return self._cursor

    def execute(self, query, retry_counter=0):
        try:
            #query = "set statement_timeout=3;" + query
            self._cursor.execute(query)
            retry_counter = 0
        except (psycopg2.DatabaseError, psycopg2.OperationalError) as error:
            if retry_counter >= LIMIT_RETRIES:
                raise error
            else:
                retry_counter += 1
                print("got error {}. retrying {}".format(str(error).strip(), retry_counter))
                time.sleep(1)
                self.reset()
                self.execute(query, retry_counter)
        except (Exception, psycopg2.Error) as error:
            raise error
        return self._cursor.fetchone()

    def is_master(self):
        row = self.execute("select pg_is_in_recovery();")
        if row and row[0]:
            return False
        return True

    def reset(self):
        self.close()
        self.connect()
        self.cursor()

    def close(self):
        if self._connection:
            if self._cursor:
                self._cursor.close()
            self._connection.close()
            print("PostgreSQL connection is closed")
        self._connection = None
        self._cursor = None

    def init(self):
        self.connect()
        self.cursor()


print("Start")
print("PostgreSQL connection init to happen next")
db = DB(user=user, password=password, host=host, port=port, database=database, reconnect=True)

print("PostgreSQL connection init complete")
print(db.execute("select pg_sleep(10);"))
time.sleep(20)
print(db.execute("select 2;"))
print(db.execute("select 3;"))
print(db.execute("select 4;"))
print(db.execute("select 5;"))
time.sleep(1)
print("End")

except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)

finally:
    # closing database connection.
     print("PostgreSQL connection to be closed")
    if db.connection:
        db.close()
        print("PostgreSQL connection is closed")
