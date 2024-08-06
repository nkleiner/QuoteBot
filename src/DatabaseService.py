import sqlite3


class DatabaseService:
    def __init__(self):
        self.connection = sqlite3.connect('quote.db')
        self.crsr = self.connection.cursor()

    def GetInitialDatabaseInformation(self):
        #Initial list of quotes and authors created
        sql_command = """SELECT * FROM quotes"""
        result = self.crsr.execute(sql_command)
        quoteList, authorList = self.EnsureQuotePoolUpdated()

    def EnsureQuotePoolUpdated(self):
        sql_command = """SELECT * FROM quotes"""
        result = self.crsr.execute(sql_command)
        return result

    def InsertNewQuote(self, message):
        entry = message.split("-")

        if(len(entry) == 1):
            return False

        author = entry[1].strip()
        quote = entry[0].strip()
        self.crsr.execute("""insert into quotes (author, quote) values (?, ?)""", (author, quote))
        self.connection.commit()
        return True

    
    def HandleDatabaseRefreshRequest(self, quotes):
        try:
            self.crsr.execute("""DROP TABLE quotes""")
            self.table_initialization(quotes)
            self.connection.commit()
            return True

        except:
            self.connection.commit()
            return False
    
    def CheckForInitilizationStatus(self):
        result = self.crsr.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='quotes'; """).fetchall()
        if(result == []):
            return True
        
        else:
            return False

    def InitializeDatabaseConnection(self):
        print("Successfully connected to the database")
        
        if(self.CheckForInitilizationStatus()):
            self.table_initialization([])

        self.connection.commit()

    def table_initialization(self, quotes):    
        sql_command = """CREATE TABLE if NOT EXISTS quotes (
        author VARCHAR(50),
        quote VARCHAR(100))"""

        self.crsr.execute(sql_command)
        print("Table quotes Initialized Successfully")

        for quote in quotes:
            message = ""
            quote = quote.split('-')
            if len(quote) > 2:
                for i in quote[0:-1]:
                    message += i
                    if i != quote[-2]:
                        message += '-'

            elif len(quote) == 1:
                print(quote)
                continue

            else:
                message = quote[0]
                
            author = quote[-1].strip()
            self.crsr.execute("""insert into quotes (author, quote) values (?, ?)""", (author, message))