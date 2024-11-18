class QuoteRequestResponse:
    def __init__(self, quote, author, multiQuote):
        self.quote = quote
        self.author = author
        self.multiQuote = multiQuote

    def get_quote(self):
        return self.quote

    def set_quote(self, newQuote):
        self.quote = newQuote

    def get_author(self):
        return self.author

    def set_author(self, newAuthor):
        self.author = newAuthor

    def get_multiQuote(self):
        return self.multiQuote
    
    def set_multiQuote(self, newMultiQuote):
        self.multiQuote = newMultiQuote