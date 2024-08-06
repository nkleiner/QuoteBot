import os
import discord
import json
from DatabaseService import DatabaseService
from QuoteService import QuoteService

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
    quoteService = QuoteService()

    intents = discord.Intents.default()
    intents.message_content = True
    dbService.InitializeDatabaseConnection()
    quoteService.UpdateQuotePool(dbService)

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
            result = dbService.InsertNewQuote(user_message)

            if(result):
                await message.add_reaction(u"\U0001F44D")
                quoteService.UpdateQuotePool(dbService)
            
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
            await message.channel.send("Hello! I am quote bot. Here's a list of what I can do!")
            await message.channel.send("1. !quote")
            await message.channel.send("2. !quote *name*")
            await message.channel.send("3. !inspire")
            await message.channel.send("4. !refresh_database")
            await message.channel.send("5. !format")
            
        #Inspirational Quotes
        if message.content.startswith('!inspire'):
            quote = quoteService.GetInspirationalQuote()
            await message.channel.send(quote)

        if message.content.startswith('!stats'):
            if channel == 'general':
                raise NotImplementedError

            else:
                raise NotImplementedError

        if message.content.startswith('!refresh_database'):
            await message.channel.send("Gathering quotes to refresh database")
            council = client.get_channel(quoteChannelID)
            channel_quotes = [message.content async for message in council.history(limit=None)]
            await message.channel.send("Quotes gathered, preparing database reset")

            status = dbService.HandleDatabaseRefreshRequest(channel_quotes)

            if status == True:
                await message.channel.send("Quote database successfully refreshed")

            else:
                await message.channel.send("Quote database refresh failed, please contact administrator")

    client.run(botToken)








