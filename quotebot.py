import os
import discord
import requests
import sqlite3
import random
import json

def getQuotes(result):
    #Function that gathers the list of quotes and their authors from the database
    
    quoteList = []
    authorList = []
    
    for i in result:
        quoteList.append(i[1])
        authorList.append(i[0])
        
    return quoteList, authorList
        

def get_quote():
    #Function to get inspirational quotes
    
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote

def createconnection():
    intialization = False
    
    #try:
    connection = sqlite3.connect('quote.db')
    crsr = connection.cursor()

    print("Successfully connected to the database")
    if intialization:
        table_initialization(crsr)
        connection.commit()


    return crsr, connection
    print("Connection to server failed")


def table_initialization(crsr, quotes):
    
    crsr.execute("""DROP TABLE quotes""")
    
    sql_command = """CREATE TABLE quotes (
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


    return True


if __name__ == "__main__":
    #Connection to database
    crsr, connection = createconnection()
    intents = discord.Intents.default()
    intents.message_content = True
    
    client = discord.Client(intents=intents)
    



    @client.event
    async def on_ready():    
        print('We have logged in as {0.user}'.format(client))

    @client.event
    async def on_message(message):

        #Initial list of quotes and authors created
        sql_command = """SELECT * FROM quotes"""
        result = crsr.execute(sql_command)
        quoteList, authorList = getQuotes(result)
        
        username = str(message.author).split('#')[0]
        user_message = str(message.content)
        channel = str(message.channel.name)
        print(f'{username}: {user_message} ({channel})')
        splitMessage = user_message.lower().strip().split()

        #Watching for New Quotes to be added to the database
        if channel == "quote-channel":
            print("New Quote Submitted")

            entry = user_message.split("-")

            author = entry[1].strip()
            quote = entry[0].strip()

            print(author, quote)
            
            crsr.execute("""insert into quotes (author, quote) values (?, ?)""", (author, quote))
            connection.commit()

            await message.add_reaction(u"\U0001F44D")
            
        #Doesn't respond to it's own messages
        if message.author == client.user:        
            return


        #Quote Feature, can be random quote or user specific
        if message.content.startswith('!quote'):
            print()
            print("New Request Received")

            #I and the Guys Specific Quotes
            if channel == "general":
                if len(splitMessage) > 1:
                    tempQuote = []
                    
                    #Specific Person Quote Requests
                    requestedAuthor = splitMessage[1]
                    print("Specific Quote Author Requested: " + requestedAuthor)

                    #Creating our list of temporary quotes
                    for i in range(len(authorList)):
                        if authorList[i].lower() == requestedAuthor:
                            tempQuote.append(quoteList[i])

                    #Random number, print formatting and sending of quote
                    if len(tempQuote) >= 1:
                        x = random.randrange(0, len(tempQuote))
                        quote = tempQuote[x]
                        author = requestedAuthor[0].upper()
                        author += requestedAuthor[1:]
                        await message.channel.send(f'{quote} - {author}')

                    else:
                        await message.channel.send(f'No quotes for {requestedAuthor} exist in the current database')
                        
                    
                else:
                    #Random Quote
                    x = random.randrange(0, len(iquoteList))
                    author = authorList[x]
                    quote = quoteList[x]

                    await message.channel.send(f'{quote} - {author}')


        #Help menu
        if message.content.startswith('!help'):
            await message.channel.send("Hello! I am quote bot. Here's a list of what I can do!")
            await message.channel.send("1. !quote")
            await message.channel.send("2. !quote *name*")
            await message.channel.send("3. !inspire")
            await message.channel.send("4. !refresh_database")
            
        #Inspirational Quotes
        if message.content.startswith('!inspire'):
            quote = get_quote()
            await message.channel.send(quote)


        if message.content.startswith('!stats'):
            if channel == 'general':
                raise NotImplementedError

            else:
                raise NotImplementedError

        if message.content.startswith('!refresh_database'):
            
            await message.channel.send("Gathering quotes to refresh database")
            council = client.get_channel()

            channel_quotes = [message.content async for message in council.history(limit=None)]

            await message.channel.send("Quotes gathered, preparing database reset")

            status = table_initialization(crsr, channel_quotes)

            if status == True:
                await message.channel.send("Quote database successfully refreshed")
                connection.commit()

            else:
                await message.channel.send("Quote database refresh failed, please contact administrator")
                connection.commit()

    client.run('')




