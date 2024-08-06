class QuoteRequestResponse:
    def __init__(self, quote, author):
        self.quote = quote
        self.author = author

    def get_quote(self):
        return self.quote

    def set_quote(self, newQuote):
        self.quote = newQuote

    def set_author(self):
        return self.author

    def get_author(self, newAuthor):
        self.author = newAuthor