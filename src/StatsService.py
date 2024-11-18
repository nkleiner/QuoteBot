class StatsService:
    def __init__(self):
        self.authorStats = {"default": 0}

    def InitializeAuthorStatistics(self, authorsList):
        #Function that initializes the statistics of the quote database on startup (perhaps this could be stored in the DB as well for efficiency?)
        self.authorStats = {"default": 0}
        for author in authorsList:
            splitAuthors = author.split("$$$")
            for newAuthor in splitAuthors:
                newAuthor = newAuthor.strip()
                if(self.authorStats.get(newAuthor) is None):
                    self.authorStats[newAuthor] = 1

                else:
                    oldTotal = self.authorStats[newAuthor]
                    self.authorStats.update({newAuthor: oldTotal + 1})

    def UpdateAuthorStatistics(self, author):
        splitAuthors = author.split("$$$")
        for newAuthor in splitAuthors:
            newAuthor = newAuthor.strip()
            if(self.authorStats.get(newAuthor) is None):
                self.authorStats[newAuthor] = 1

            else:
                oldTotal = self.authorStats[newAuthor]
                self.authorStats.update({newAuthor: oldTotal + 1})

    def GetRequestedAuthorStat(self, message):
        splitMessage = message.lower().strip().split()
        requestedAuthor = ' '.join(map(str, splitMessage[1:])).title()
        return self.authorStats.get(requestedAuthor), requestedAuthor