import sqlite3

class DatabaseService:
    def __init__(self):
        self.connection = sqlite3.connect('quote.db')
        self.crsr = self.connection.cursor()

    def EnsureQuotePoolUpdated(self):
        sql_command = """SELECT * FROM quotes"""
        result = self.crsr.execute(sql_command)
        return result

    def InsertNewQuote(self, message):
        listOfQuotes = message.split("\n")

        #MultiQuote
        if(len(listOfQuotes) > 1):
            authors = []
            quotes = []

            for currentQuote in listOfQuotes:
                entry = currentQuote.split("-")
                if(len(entry) != 2):
                    return False
                
                else:
                    authors.append(entry[1])
                    quotes.append(entry[0])
            
            #While a more sophisticated answer might exist 
            #For now we're going to distinguish multi-quote entries by seperated authors and quotes with a special $$$
            author = '$$$'.join(map(str, authors))
            quote = '$$$'.join(map(str, quotes))

        else:
            entry = message.split("-")

            if(len(entry) != 2):
                #Perhaps handle this better..?
                return False
            
            else:
                author = entry[1].strip().title()
                quote = entry[0].strip()


        self.crsr.execute("""insert into quotes (author, quote) values (?, ?)""", (author, quote))
        return True, author, quote

    
    def HandleDatabaseRefreshRequest(self, quotes):
        try:
            self.crsr.execute("""DROP TABLE quotes""")
            self.InitializeDatabaseTables(quotes)
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
            self.InitializeDatabaseTables([])

        self.connection.commit()

    def InitializeDatabaseTables(self, quotes):    
        sql_command = """CREATE TABLE if NOT EXISTS quotes (
        author VARCHAR(50),
        quote VARCHAR(100))"""

        self.crsr.execute(sql_command)
        print("Quotes Table Initialized Successfully")

        for quote in quotes:
            self.InsertNewQuote(quote)
        self.connection.commit()