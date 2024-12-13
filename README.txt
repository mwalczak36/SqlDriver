#Author: Michael Walczak
SqlDriver — Sql database and table creation

sqlite3 — interface for SQLite databases
SqlDriverModule is a module that will create an object out of the SqlDriver class and let you execute Sql commands.


Tutorial:

First create a new SqlDriver object out of the SqlDriver class. 

from SqlDriverModule import SqlDriver
myDriver = SqlDriver()

You can create a single table using the createTable method.
myDriver.createTable()

createTable takes 1 required argument and 1 optional argument.
The first required one is:  sFilePath
This can be a local path:   createTable("Pay.txt")
or it can be a folder path: createTable("C:\Projects\Tables\Pay.txt")

The second optional one is: sDatabaseFile
All Sql methods take an optionl database file argument
This parameter can also be a local or a folder path:
createTable("C:\Projects\Tables\Pay.txt", sDatabaseFile="C:\Projects\Tables\myDatabase.db")
If no database file is specified then csvDatabase.db will be used as default in the program folder

You can also loop thru a folder, and create a table out of each file in the folder using the plural version:
myDriver.createTables()

This method has the same parameters as the regular createTable
but the first parameter is a folder path, instead of a file path
It also has an optional database file parameter
myDriver.createTables("C:\Projects\Tables")
myDriver.createTables("C:\Projects\Tables", sDatabaseFile="myDatabase.db")
myDriver.createTables("Tables", sDatabaseFile="C:\Projects\Tables\myDatabase.db")
All variations of file and folder locations are acceptable

displayTable(sTableName:str, sDatabaseFile:str)->None

dropTable(sTableName:str, sDatabaseFile:str)->None

deleteFile(sFile="csvDatabase.db")->None #deletes the default database by default

executeSQL(sSQL:str, sDatabaseFile:str)->None #SELECT statements will automatically print