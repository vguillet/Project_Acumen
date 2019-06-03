# from Group12.dbinterface import configuration
# import sqlite3
# from Group12.dbinterface.DBGUIAPI import DBManager
from dbinterface.Sqlite3ScratchFile import DBManager

# sqldb = configuration.database_path
# print("db path:",sqldb) # For me (Xavier) this returns: db path: C:\Users\XGOBY\ProjectAcumen\Group12\dbinterface\testdb.db
# print(type(sqldb)) # For me (Xavier) this returns: <class 'str'>

##################### This is unimporant, do not care about the following 3 lines of code! #####################
# dbsplit = sqldb.split('\\')
# print(dbsplit) # For me (Xavier) this returns: ['C:', 'Users', 'XGOBY', 'ProjectAcumen', 'Group12', 'dbinterface', 'testdb.db']
# print("dbfile:",dbsplit[-1]) # For me (Xavier) this returns: dbfile: testdb.db
################################################################################################################

if __name__ == '__main__':
    # For testing whether testdb.db is indeed present in Group12\dbinterface\testdb.db
    # and if the connection with the database is successfully made.
    table_name = "CapitalsOfTheEU"
    print(DBManager().get_all_table_data(table_name))







