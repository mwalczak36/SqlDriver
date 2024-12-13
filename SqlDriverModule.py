#Edited: 12/12/24
#Author: Michael Walczak

import sqlite3
import csv
import os


class SqlDriver:
    def __init__(self)->object:
        self.__sTableName = self.__sCreateTable = self.__sInsert = self.__sInsertReset = self.__sDataType = ""
        self.__lstHeaderRow = self.__lstMainData = []
        self.__iRows = 0

    def _connectionDecorator(func):
        def wrapper(self, *args, **kwargs):
            sDatabaseFile = kwargs.get("sDatabaseFile", "csvDatabase.db")
            try:
                connection = sqlite3.connect(sDatabaseFile)
                cursor = connection.cursor()
                func(self, connection, cursor, *args, sDatabaseFile)
            except TypeError: print("Could not wrap function")
            connection.commit()
            connection.close()
        return wrapper

    @_connectionDecorator
    def createTable(self, connection:sqlite3.Connection, cursor:sqlite3.Cursor, sFilePath:str, sDatabaseFile:str):

        self.__sTableName = ""
        if "\\" in sFilePath: self.__sTableName = sFilePath[sFilePath.rfind("\\")+1:sFilePath.find('.')]
        else: self.__sTableName = f"{sFilePath[:sFilePath.find('.')]}"

        self.__sCreateTable = f"CREATE TABLE {self.__sTableName}("
        self.__sInsert = f"INSERT INTO {self.__sTableName}("

        self.__lstHeaderRow = self.__lstMainData = []
        try:
            with open(sFilePath, "r") as file:

                reader = csv.reader(file, skipinitialspace=True)
                self.__lstHeaderRow = [header.strip() for header in next(reader)]

                for row in reader:
                    if not bool(row) or row[0].isspace(): continue
                    else: self.__lstMainData.append([column.strip() for column in row])      
        except FileNotFoundError:
            print(f"Could not open file: {sFilePath}")
            return

        for headerColumn, dataColumn in zip(self.__lstHeaderRow, self.__lstMainData[0]):

            headerColumn = headerColumn.strip()
            self.__sDataType = self._getDataType(dataColumn)[1]

            if self.__sDataType == "str": self.__sCreateTable += f"'{headerColumn}' text, "
            elif self.__sDataType == "int": self.__sCreateTable += f"'{headerColumn}' integer, "
            elif self.__sDataType == "float": self.__sCreateTable += f"'{headerColumn}' real, "
            self.__sInsert += f"'{headerColumn}', "

        self.__sCreateTable = f"{self.__sCreateTable[:-2]})"
        self.__sInsert = f"{self.__sInsert[:-2]})"

        try: 
            cursor.execute(self.__sCreateTable)
            print(self.__sCreateTable)
        except sqlite3.OperationalError: 
            print(f"Could not execute query: {self.__sCreateTable}")
            return
        
        self.__sInsert += " VALUES("
        self.__sInsertReset = self.__sInsert

        self.__iRows = 0
        for row in self.__lstMainData:

            for column in row:

                column = column.replace("'", "") #type: str
                self.__sInsert += f"'{column}', "

            self.__sInsert = f"{self.__sInsert[:-2]})"

            try:
                cursor.execute(self.__sInsert)
                print(self.__sInsert)
                self.__iRows += 1
            except sqlite3.OperationalError:
                print(f"Could not execute query: {self.__sInsert}")

            self.__sInsert = self.__sInsertReset
        print(f"Rows Successfully Parsed: {self.__iRows}")

    @_connectionDecorator
    def createTables(self, connection, cursor, sFolderPath:str, sDatabaseFile): 

        try:
            for filename in os.scandir(sFolderPath):

                if filename.name[-4:].lower() == ".csv" or filename.name[-4:].lower() == ".txt":

                    self.createTable(filename.path, sDatabaseFile=sDatabaseFile)

        except FileNotFoundError:
            print(f"Could not open Folder: {sFolderPath}")

    @_connectionDecorator
    def displayTable(self, connection:sqlite3.Connection, cursor:sqlite3.Cursor, sTableName:str, sDatabaseFile:str)->None:
        if "\\" in sTableName: sTableName = sTableName[sTableName.rfind("\\")+1:]
        try:
            cursor.execute(f"SELECT * FROM {sTableName}")
            for tupSQLRows in cursor.fetchall(): print(tupSQLRows)
        except sqlite3.OperationalError: 
            print(f"Could not execute query: SELECT * FROM {sTableName}")
            return

    @_connectionDecorator
    def dropTable(self, connection:sqlite3.Connection, cursor:sqlite3.Cursor, sTableName:str, sDatabaseFile:str)->None:
        try:
            cursor.execute(f"DROP TABLE {sTableName}")
            print(f"Table: {sTableName} Successfully Dropped")
        except:
            print(f"Could not execute query: DROP TABLE {sTableName}")
            return

    def _getDataType(self, sToCheck:str)->tuple:
        try:     
            if int(sToCheck) == float(sToCheck):
                return int(sToCheck), 'int'
        except:
            try:
                    return float(sToCheck), 'float' 
            except:
                    if sToCheck in ["True","False"]:
                        return True if sToCheck == "True" else False, 'boolean'
                    else: 
                        return sToCheck, 'str'
                    
    def deleteFile(self, sFile="csvDatabase.db", *args)->None:
        try: 
            os.remove(sFile)
            print(f"File: {sFile} Successfully Deleted")
        except: print(f"Could not delete file: {sFile}")

    @_connectionDecorator
    def executeSQL(self, connection:sqlite3.Connection, cursor:sqlite3.Cursor, sSQL:str, sDatabaseFile:str)->None:
        try:
            cursor.execute(sSQL)
            print(sSQL)
            if sSQL.startswith("SELECT"):
                for tupSQLRows in cursor.fetchall(): 
                    print(tupSQLRows)
        except: print(f"Could not execute query: {sSQL}")
            
#https://people.sc.fsu.edu/~jburkardt/data/csv/csv.html