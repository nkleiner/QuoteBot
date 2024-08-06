import random
import requests
import json
from QuoteRequestResponse import QuoteRequestResponse as QuoteResponse
from DatabaseService import EnsureQuotePoolUpdated

global quotesList
global authorsList

def UpdateQuotePool():
    #Function that gathers the list of quotes and their authors from the database
    tempQuoteList = []
    tempAuthorList = []
    
    result = EnsureQuotePoolUpdated()

    for i in result:
        tempQuoteList.append(i[1])
        tempAuthorList.append(i[0])

    global quotesList
    global authorsList

    quotesList = tempQuoteList
    authorsList = tempAuthorList 

def GetInspirationalQuote():
    #Function to get inspirational quotes
    
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote


def HandleQuoteRequest(message):
    print("\n New Quote Request Received")

    splitMessage = message.lower().strip().split()

    if len(splitMessage) > 1:
        tempQuote = []
        
        #Specific Person Quote Requests
        requestedAuthor = splitMessage[1]
        print("Specific Quote Author Requested: " + requestedAuthor)

        #Creating our list of temporary quotes
        for i in range(len(authorsList)):
            if authorsList[i].lower() == requestedAuthor:
                tempQuote.append(quotesList[i])


        #Random number, print formatting and sending of quote
        if len(tempQuote) >= 1:
            x = random.randrange(0, len(tempQuote))
            quote = tempQuote[x]
            author = requestedAuthor[0].upper()
            author += requestedAuthor[1:]
            return QuoteResponse(quote, author)

        else:
            return QuoteResponse("N/A", author)            
        
    else:
        #Random Quote
        x = random.randrange(0, len(quotesList))
        author = authorsList[x]
        quote = quotesList[x]
        return QuoteResponse(quote, author)