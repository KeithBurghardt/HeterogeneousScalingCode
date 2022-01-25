# definition of the paper entity in MAG data
class Paper:
    def __init__(self, paperId, title, authors, year, date, references, citations):
        self.paperId = paperId
        self.title = title
        self.year = year
        self.date = date
        self.authors = authors
        self.references = references
        self.citations = citations
        self.aff_authorIds = {}
        self.aff_contribution = {}

        new_authors = []
        authorIds = set()
        for author in self.authors:
            authorId = author.authorId
            if authorId not in authorIds:
                new_authors.append(author)
            authorIds.add(authorId)
        self.authors = new_authors

        for author in self.authors:
            affId = author.affId
            authorId = author.authorId
            if affId not in self.aff_authorIds:
                self.aff_authorIds[affId] = set()
            self.aff_authorIds[affId].add(authorId)

        authornum = len(self.authors)
        for affId in self.aff_authorIds:
            self.aff_contribution[affId] = len(self.aff_authorIds[affId]) / authornum
