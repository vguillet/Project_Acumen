# IMPORTANT!
# This Python script/file (called configuration.py) which fixes the issue of not being able to
#  acces/use/connect to the same SQLite3 database from all the different scripts in all the
# different directories/folders.
# Note that this configuration file is (for now, we may need or want to or not change it later)

# INSTRUCTIONS:
# In order to get the database path follow the outlined steps:

# 1st) Use the following line of code where all other modules are imported:
# from Group12.dbinterface import configuration

# 2nd) Next, you can acces the path of the database via the following line of code:
# db = configuration.database_path

# This variable db (which is of type str) can then later be used for accesing the same SQLite3 database
# from any other Python script

import os.path

package_dir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(package_dir, 'testdb.db')