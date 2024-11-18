import random
import requests
import json
from QuoteRequestResponse import QuoteRequestResponse as QuoteResponse

class QuoteService:
    def __init__(self):
        self.quotesList = []
        self.authorsList = []

    def InitializeQuotePool(self, databaseService, statsService):
        #Function that intializes the list of quotes and their authors from the database
        tempQuoteList = []
        tempAuthorList = []
        
        result = databaseService.EnsureQuotePoolUpdated()

        for i in result:
            tempQuoteList.append(i[1])
            tempAuthorList.append(i[0])

        self.quotesList = tempQuoteList
        self.authorsList = tempAuthorList
        statsService.InitializeAuthorStatistics(tempAuthorList)

    def UpdateQuotePool(self, author, quote):
        #Function that updates the run-time list of quotes and authors
        self.quotesList.append(quote)
        self.authorsList.append(author.title())

    def GetInspirationalQuote(self):
        #Function to get inspirational quotes
        
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " -" + json_data[0]['a']
        return quote

    def HandleQuoteRequest(self, message):
        print("\n New Quote Request Received")

        splitMessage = message.lower().strip().split()

        if len(splitMessage) > 1:
            tempQuote = []

            #Specific Person Quote Requests
            requestedAuthor = ' '.join(map(str, splitMessage[1:]))
            print("Specific Quote Author Requested: " + requestedAuthor)

            #Creating our list of temporary quotes
            for i in range(len(self.authorsList)):
                if self.authorsList[i].lower() == requestedAuthor:
                    tempQuote.append(self.quotesList[i])


            #Random number, print formatting and sending of quote
            if len(tempQuote) >= 1:
                x = random.randrange(0, len(tempQuote))
                quote = tempQuote[x]
                #Format names properly
                author = requestedAuthor.title()
                if(MultiQuoteCheck(quote)):
                #Chaos Ensues...
                    return QuoteResponse("N/A", "N/A", ReformatMultiQuote(quote, author))
                else:
                    return QuoteResponse(quote, author)

            else:
                return QuoteResponse("N/A", author)            
            
        else:
            #Random Quote
            x = random.randrange(0, len(self.quotesList))
            author = self.authorsList[x]
            quote = self.quotesList[x]
            if(MultiQuoteCheck(quote)):
                #Chaos Ensues...
                return QuoteResponse("N/A", "N/A", ReformatMultiQuote(quote, author))
            else:
                return QuoteResponse(quote, author, "N/A")
        

def MultiQuoteCheck(quote):
    splitQuote = quote.split("$$$")
    return len(splitQuote) > 1
    

def ReformatMultiQuote(quotes, authors):
    splitQuotes = quotes.split("$$$")
    splitAuthors = authors.split("$$$")
    listOfFormatedQuotes = []

    for i in range(len(splitQuotes)):
        current = f'{splitQuotes[i]} - {splitAuthors[i]}'
        listOfFormatedQuotes.append(current)
    
    return '\n'.join(map(str, listOfFormatedQuotes))