#connecting to the DB using pymysql module
import sys
import pymysql

class DbOperationException(Exception):
    pass

class GameDataOperations:
    def connectDb(self):
        conn = pymysql.Connect(
            host='localhost',port=3306,
            user='root',password='akshay031',
            db='games',charset='utf8')
        print("Database connected successfully")
        return conn

    def disconnectDb(self,connection):
        connection.close()
        print("Database disconnected successfully")

    def createTable(self):
        createTableQuery = 'create table IF NOT EXISTS games(id int primary key auto_increment,name varchar(50) not null, price int ,constraint new check(price % 100 = 0), minimum_players int default (1),maximum_players int default (11),description varchar(1000));'
        try:
            connection = self.connectDb()
            cursor = connection.cursor()
            returnValue = cursor.execute(createTableQuery)
            if returnValue != 0:
                raise DbOperationException
            print("Return Value: ",returnValue)
            connection.commit()
        except pymysql.err.OperationalError:
            print("Error while creating the table XYZ")
        except DbOperationException:
            print("Error while creating the table ABC")
        except:
            print("Some error occured while connecting the database.")
        finally:
            cursor.close()
            self.disconnectDb(connection)

    def createDb(self):
        createDbQuery = 'create database IF NOT EXISTS nmamit_db'
        try:
            connection = self.connectDb()
            cursor = connection.cursor()
            returnValue = cursor.execute(createDbQuery)
            cursor.close()
        except:
            print("Error in connecting to the database")

    def readGameData(self,operation):
        name = input('Enter the name of the game: ')
        price = int(input("Enter Price of the game(per head): "))
        minPlayers = int(input("Enter minimum number of players: "))
        maxPlayers = int(input('Enter maximum number of players: '))
        if operation == 'insert':
            print("Enter description of the game(to stop press ctrl+z): ",end='')
            description = sys.stdin.read()
            description = description.replace('\n', ' ').strip()
            return (name, price, minPlayers, maxPlayers, description)
        id = int(input('Enter Id of the Game to be updated: '))
        return (name, price, minPlayers, maxPlayers, id)

    def createGame(self):
        insertRowQuery = 'insert into games(name,price ,minimum_players,maximum_players,description) values(%s,%s,%s,%s,%s)'
        gameObject = self.readGameData('insert')
        try:
            connection = self.connectDb()
            cursor = connection.cursor()
            returnValue = cursor.execute(insertRowQuery, gameObject)
            if returnValue != 1:
                raise DbOperationException
            cursor.close()
            connection.commit()
            print("Row inserted successfully")
            self.disconnectDb(connection)
        except DbOperationException:
            print('Error in inserting a row')
        except:
            print('Error in connecting to the database')

    def updateGame(self):
        updateQuery = 'update games set name=%s,price=%s ,minimum_players=%s,maximum_players=%s where id=%s'
        gameObject = self.readGameData('update')
        try:
            connection = self.connectDb()
            cursor = connection.cursor()
            returnValue = cursor.execute(updateQuery, gameObject)
            if returnValue != 1:
                print(f'Game with id {gameObject[4]} not found')
            else:
                print("Row updated successfully")
            connection.commit()
            cursor.close()
            self.disconnectDb(connection)
        except:
            print('Error while updating the row')

    def deleteGame(self):
        id = int(input("Enter id of the game to be deleted: "))
        updateQuery = f'delete from games where id = {id}'
        try:
            connection = self.connectDb()
            cursor = connection.cursor()
            returnValue = cursor.execute(updateQuery)
            if returnValue != 1:
                print(f'Game with id = {id} not found')
            else:
                print("Row deleted successfully")
            connection.commit()
            cursor.close()
            self.disconnectDb(connection)
        except:
            print('Error while deleting the row')
    
    def searchGame(self):
        id = int(input("Enter id of the game to be searched: "))
        searchQuery = f'select * from games where id = {id}'
        try:
            connection = self.connectDb()
            cursor = connection.cursor()
            numberOfRows = cursor.execute(searchQuery)
            row = cursor.fetchone()
            if row is None:
                print(f'Game with id = {id} not found')
            else:
                print('Game details is:\n ',str(row))

            '''
            if numberOfRows == 0:
                print(f'Game with id = {id} not found')
            else:
                row = cursor.fetchone()
                print('Game details is:\n ',str(row))
            '''
            connection.commit()
            cursor.close()
            self.disconnectDb(connection)
        except pymysql.err.DataError:
            print('Error while searching the row')

    def listGames(self):
        query = f'select * from games'
        try:
            connection = self.connectDb()
            cursor = connection.cursor()
            numberOfRows = cursor.execute(query)
            connection.commit()
            rows= cursor.fetchall()
            if rows is None:
                print(f'Game with id = {id} not found')
            else:
                for row in rows:
                    print('Game details is:\n ',str(row))
            cursor.close()
            self.disconnectDb(connection)
        except pymysql.err.DataError:
            print('Error while searching the row')

class Menu:
    def __init__(self,gameOperations):
        self.gameOperations = gameOperations

    def exitProgram(self):
        exit('End of the program')
    
    def invalidInput(self):
        print("Invalid Input Entered")

    def getMenu(self):
        menu = {
        1 : self.gameOperations.createGame,
        2 : self.gameOperations.searchGame,
        3 : self.gameOperations.updateGame,
        4 : self.gameOperations.deleteGame,
        5 : self.gameOperations.listGames,
        6 : self.exitProgram
        }
        return menu
    
    def getInstance(self):
        return self
        
    def runMenu(self):
        menu=self.getMenu()
        while True:
            print("1. Create 2:Search 3.Update 4:Delete 5:List-All 6:Exit\n Your choice: ")
            choice=int(input())
            menu.get(choice, self.invalidInput)()

def startApp():
    operations = GameDataOperations()
    menu = Menu(operations)
    menu.runMenu()

startApp()



