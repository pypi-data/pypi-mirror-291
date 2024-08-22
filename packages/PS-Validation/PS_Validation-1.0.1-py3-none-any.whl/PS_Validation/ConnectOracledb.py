import oracledb
from pandas import DataFrame
import os

class QueryExecuter:
    def __init__(self):
        username='A157336'
        password='hamdiemada157336'
        host='10.199.104.126'
        port='1521'
        sid='analytics'
        try:
            lib_dir=rf"C:\Users\{os.getlogin()}\instantclient"
            oracledb.init_oracle_client(lib_dir=lib_dir)
        except:
            print(r'instantclient clint folder not found add to this path: C:\Users\{os.getlogin()}\instantclient')
            raise
        connection = oracledb.connect(user=username, password=password, host=host, port=port, sid=sid)
        self.connection= connection
        print("Connection successful.")

    def generateParamsPlaceholders(self, parts, chunk_size=995):
        """
        Generates placeholders for SQL queries in chunks based on batch size.
        and Generates parameters for SQL queries in chunks based on batch size.
    
        :return: A tuple of list of chunks, placeholders and params
        """
        # Create placeholder pairs for each part and man
        x = [f"(:place{i})" for i in range(len(parts))]
        placeholders = [', '.join(x[i: i + chunk_size]) for i in range(0, len(x), chunk_size)]
        #Generates parameters for SQL queries in chunks based on batch size.
        params = [ {
            f"place{idx+i}": part 
            for idx, part in enumerate(parts[i:i+chunk_size])
            }  
            for i in range(0, len(parts), chunk_size)
            ]
        return placeholders, params

    def execute_query(self, query, param=None):
        try:
            with self.connection.cursor() as cursor:
                # Set session parameters for case-insensitive search
                cursor.execute(query, param)
                rows = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                return DataFrame(rows, columns=columns)
        except oracledb.DatabaseError as e:
            print("There was a problem executing the query: ", e)
            raise 