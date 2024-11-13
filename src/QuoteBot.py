import os
import discord
import json
from DatabaseService import DatabaseService
from QuoteService import QuoteService
from StatsService import StatsService

def LoadConfiguration():
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, "config.json")
    configurationFile = open(abs_file_path)
    jsonConfigData = json.load(configurationFile)
    botToken = jsonConfigData["token"]
    quoteChannelID = jsonConfigData["quoteChannelID"]
    return botToken, int(quoteChannelID)

if __name__ == "__main__":
    #Connection to database
    dbService = DatabaseService()
    statsService = StatsService()
    quoteService = QuoteService()

    intents = discord.Intents.default()
    intents.message_content = True
    dbService.InitializeDatabaseConnection()
    quoteService.InitializeQuotePool(dbService, statsService)

    botToken, quoteChannelID = LoadConfiguration()
    
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():    
        print('We have logged in as {0.user}'.format(client))

    @client.event
    async def on_message(message):
        
        username = str(message.author).split('#')[0]
        user_message = str(message.content)
        channel = str(message.channel.name)
        print(f'{username}: {user_message} ({channel})')

        #Doesn't respond to it's own messages
        if message.author == client.user:        
            return

        #Watching for New Quotes to be added to the database
        if channel == "quote-channel":
            print("New Quote Submitted")
            result, author, quote = dbService.InsertNewQuote(user_message)

            if(result):
                await message.add_reaction(u"\U0001F44D")
                statsService.UpdateAuthorStatistics(author)
                quoteService.UpdateQuotePool(author, quote)
            
            else:
                await message.add_reaction(u"\U0001F44E")

        #Quote Feature, can be random quote or user specific
        if message.content.startswith('!quote'):
            quoteResponse = quoteService.HandleQuoteRequest(message.content)

            if(quoteResponse.quote == "N/A"):
                await message.channel.send(f'No quotes for {quoteResponse.author} exist in the current database') 
        
            else:
                await message.channel.send(f'{quoteResponse.quote} - {quoteResponse.author}')
            
        #Help menu
        if message.content.startswith('!help'):
            introduction = "Hello! I am quote bot. Here's a list of what I can do!"
            one = "1. !quote : Returns a random quote."
            two = "2. !quote *name* : Returns a random quote from the specified author."
            three = "3. !inspire : Returns a random inspirational quote unassociated with the custom quote database."
            four =  "4. !refresh_database : Refreshes the quote database, requires moderator status."
            five = "5. !stats *name* : Returns the number of quotes the given author has stored."
            six = "6. !format : Demonstrates the format quote entries should be in."
            await message.channel.send("{0}\n {1}\n {2}\n {3}\n {4}\n {5}\n {6}".format(introduction, one, two, three, four, five, six))
            
        #Inspirational Quotes
        if message.content.startswith('!inspire'):
            quote = quoteService.GetInspirationalQuote()
            await message.channel.send(quote)

        if message.content.startswith('!stats'):
            statResult, author = statsService.GetRequestedAuthorStat(user_message)

            if(statResult == None):
                await message.channel.send(f"Quote Bot failed to retrieve statistics for the author {author}! Please contact the developer if you believe this happened in error.")

            else:
                await message.channel.send(f"User {author} has a total of {statResult} quotes in the database!")

        if message.content.startswith('!refresh_database'):
            await message.channel.send("Gathering quotes to refresh database")
            council = client.get_channel(quoteChannelID)
            channel_quotes = [message.content async for message in council.history(limit=None)]
            await message.channel.send("Quotes gathered, preparing database reset")

            status = dbService.HandleDatabaseRefreshRequest(channel_quotes)

            if status == True:
                quoteService.InitializeQuotePool(dbService, statsService)
                await message.channel.send("Quote database successfully refreshed")

            else:
                await message.channel.send("Quote database refresh failed, please contact administrator")

    client.run(botToken)








