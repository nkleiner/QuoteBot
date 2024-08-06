import sqlite3

global crsr
global connection

def GetInitialDatabaseInformation():
    #Initial list of quotes and authors created
    sql_command = """SELECT * FROM quotes"""
    result = crsr.execute(sql_command)
    quoteList, authorList = EnsureQuotePoolUpdated()

def EnsureQuotePoolUpdated():
    sql_command = """SELECT * FROM quotes"""
    result = crsr.execute(sql_command)
    return result

def InsertNewQuote(message):
    entry = message.split("-")

    if(len(entry) == 1):
        return False

    author = entry[1].strip()
    quote = entry[0].strip()
    crsr.execute("""insert into quotes (author, quote) values (?, ?)""", (author, quote))
    connection.commit()
    return True

    
def HandleDatabaseRefreshRequest(quotes):
    try:
        crsr.execute("""DROP TABLE quotes""")
        table_initialization(quotes)
        connection.commit()
        return True

    except:
        connection.commit()
        return False
    
def CheckForInitilizationStatus():
    result = crsr.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='quotes';""")
    if(result.arraysize == 0):
        return True
    
    else:
        return False

def InitializeDatabaseConnection():
    global crsr
    global connection

    connection = sqlite3.connect('quote.db')
    crsr = connection.cursor()
    intialization = CheckForInitilizationStatus()

    print("Successfully connected to the database")
    table_initialization(crsr)
    connection.commit()

def table_initialization(quotes):    
    sql_command = """CREATE TABLE if NOT EXISTS quotes (
    author VARCHAR(50),
    quote VARCHAR(100))"""

    crsr.execute(sql_command)
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
        crsr.execute("""insert into quotes (author, quote) values (?, ?)""", (author, message))