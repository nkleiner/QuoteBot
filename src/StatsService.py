class StatsService:
    def __init__(self):
        self.authorStats = {"default": 0}

    def InitializeAuthorStatistics(self, authorsList):
        #Function that initializes the statistics of the quote database on startup (perhaps this could be stored in the DB as well for efficiency?)
        tempAuthorsList = []
        tempStatsList = []

        for i in range(len(authorsList)):
            if(authorsList[i] in tempAuthorsList):
                authIndex = tempAuthorsList.index(authorsList[i])
                tempStatsList[authIndex] += 1

            else:
                tempAuthorsList.append(authorsList[i])
                tempStatsList.append(1)


        for i in range(len(tempAuthorsList)):
            self.authorStats[tempAuthorsList[i]] = tempStatsList[i]

    def UpdateAuthorStatistics(self, author):
        if(self.authorStats.get(author) is None):
            self.authorStats[author] = 1

        else:
            oldTotal = self.authorStats[author]
            self.authorStats.update({author: oldTotal + 1})

    def GetRequestedAuthorStat(self, message):
        splitMessage = message.lower().strip().split()
        requestedAuthor = ' '.join(map(str, splitMessage[1:])).title()
        return self.authorStats.get(requestedAuthor), requestedAuthor