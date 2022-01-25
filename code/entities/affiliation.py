import copy
from utils.seniority import get_seniority

# definition of the affiliation entity of MAG data
class Affiliation:
    def __init__(self, affId, aff_name):

        # basic information of an affiliation
        self.affId = affId
        self.aff_name = aff_name

        # properties related to affiliation size
        self.year_paperId_authorIds = {}
        self.year_authorIds = {}
        self.year_authorId_paperIds = {}
        self.year_size = {}
        self.year_cumul_authorIds = {}  # cumulative authorIds up to that year
        self.year_cumul_size = {}   # cumulative size up to that year

        # properties related to collaborations
        self.year_authorId_paperId_internal_collab = {}
        self.year_authorId_paperId_external_collab = {}
        self.year_authorId_paperId_indiv_collab = {}
        self.year_authorId_internal_collab = {}
        self.year_authorId_external_collab = {}
        self.year_authorId_indiv_collab = {}

        self.year_paperId_internal_collab = {}
        self.year_paperId_external_inst_collab = {}
        self.year_paperId_external_indiv_collab = {}
        self.year_paperId_indiv_collab = {}
        self.year_internal_collab = {}
        self.year_external_inst_collab = {}
        self.year_external_indiv_collab = {}
        self.year_indiv_collab = {}  # internal (individual) collaborations + external individual collaborations
        self.year_cumul_internal_collab = {}
        self.year_cumul_external_inst_collab = {}
        self.year_cumul_external_indiv_collab = {}
        self.year_cumul_indiv_collab = {}
        self.year_avg_internal_collab = {}
        self.year_avg_external_inst_collab = {}
        self.year_avg_external_indiv_collab = {}
        self.year_avg_indiv_collab = {}

        # properties related to production and productivity
        self.year_production = {}
        self.year_paperId_contribution = {}
        self.year_productivity = {}
        self.year_cumul_production = {}
        self.year_cumul_productivity = {}

        # properties related to team size
        self.year_paperId_teamsize = {}
        self.year_paperId_internal_teamsize = {}
        self.year_paperId_external_teamsize = {}
        self.year_avg_teamsize = {}
        self.year_avg_internal_teamsize = {}
        self.year_avg_external_teamsize = {}
        self.year_authorId_teamsizes = {}
        self.year_authorId_avg_teamsize = {}

        # properties related to the overall citations and average impact
        self.year_paperId_citations = {}
        self.year_citations = {}
        self.year_avg_impact = {}
        self.year_authorId_paperId_citations = {}
        self.year_authorId_citations = {}
        self.year_authorId_avg_impact = {}

        # properties related to citations and average impact from one-author papers
        self.year_paperId_citations_oneauthor = {}
        self.year_citations_oneauthor = {}
        self.year_avg_impact_oneauthor = {}
        self.year_authorId_paperId_citations_oneauthor = {}
        self.year_authorId_citations_oneauthor = {}
        self.year_authorId_avg_impact_oneauthor = {}

        # properties related to citations and average impact from two-author papers
        self.year_paperId_citations_twoauthor = {}
        self.year_citations_twoauthor = {}
        self.year_avg_impact_twoauthor = {}
        self.year_authorId_paperId_citations_twoauthor = {}
        self.year_authorId_citations_twoauthor = {}
        self.year_authorId_avg_impact_twoauthor = {}

        # properties related to citations and average impact from three-author papers
        self.year_paperId_citations_threeauthor = {}
        self.year_citations_threeauthor = {}
        self.year_avg_impact_threeauthor = {}
        self.year_authorId_paperId_citations_threeauthor = {}
        self.year_authorId_citations_threeauthor = {}
        self.year_authorId_avg_impact_threeauthor = {}

        # properties related to citations and average impact from one-and-two-author papers
        self.year_paperId_citations_onetwoauthor = {}
        self.year_citations_onetwoauthor = {}
        self.year_avg_impact_onetwoauthor = {}
        self.year_authorId_paperId_citations_onetwoauthor = {}
        self.year_authorId_citations_onetwoauthor = {}
        self.year_authorId_avg_impact_onetwoauthor = {}

        # properties related to citations and average impact from three-to-six-author papers
        self.year_paperId_citations_three2sixauthor = {}
        self.year_citations_three2sixauthor = {}
        self.year_avg_impact_three2sixauthor = {}
        self.year_authorId_paperId_citations_three2sixauthor = {}
        self.year_authorId_citations_three2sixauthor = {}
        self.year_authorId_avg_impact_three2sixauthor = {}

        # properties related to seniority
        self.year_authorIds_5 = {}
        self.year_authorIds_10 = {}
        self.year_authorIds_15 = {}
        self.year_authorIds_20 = {}

    def add_paper(self, year, authorIds, external_authorIds, paperId, contribution,
                  teamsize, internal_teamsize, external_teamsize,
                  citations,
                  internal_collab, external_inst_collab, external_indiv_collab, indiv_collab):
        """
        add a paper and update the concerning properties
        :param year: publication year
        :param authorIds:
        :param paperId:
        :param contribution:
        :param teamsize:
        :param internal_teamsize:
        :param external_teamsize:
        :param citations:
        :param internal_collab:
        :param external_inst_collab:
        :param external_indiv_collab:
        :param indiv_collab:
        :return:
        """

        # paperId and its authorIds
        if year not in self.year_paperId_authorIds:
            self.year_paperId_authorIds[year] = {}
        if paperId not in self.year_paperId_authorIds[year]:
            self.year_paperId_authorIds[year][paperId] = set()
        self.year_paperId_authorIds[year][paperId] = \
            self.year_paperId_authorIds[year][paperId].union(authorIds)

        if year not in self.year_authorId_paperIds:
            self.year_authorId_paperIds[year] = {}
        for authorId in authorIds:
            if authorId not in self.year_authorId_paperIds[year]:
                self.year_authorId_paperIds[year][authorId] = set()
            self.year_authorId_paperIds[year][authorId].add(paperId)

        # production and productivity
        if year not in self.year_paperId_contribution:
            self.year_paperId_contribution[year] = {}
        self.year_paperId_contribution[year][paperId] = contribution

        # paperId and teamsize
        if year not in self.year_paperId_teamsize:
            self.year_paperId_teamsize[year] = {}
        self.year_paperId_teamsize[year][paperId] = teamsize
        if year not in self.year_paperId_internal_teamsize:
            self.year_paperId_internal_teamsize[year] = {}
        self.year_paperId_internal_teamsize[year][paperId] = internal_teamsize
        if year not in self.year_paperId_external_teamsize:
            self.year_paperId_external_teamsize[year] = {}
        self.year_paperId_external_teamsize[year][paperId] = external_teamsize

        if year not in self.year_authorId_teamsizes:
            self.year_authorId_teamsizes[year] = {}
        for authorId in authorIds:
            if authorId not in self.year_authorId_teamsizes[year]:
                self.year_authorId_teamsizes[year][authorId] = []
            self.year_authorId_teamsizes[year][authorId].append(len(authorIds)+len(external_authorIds))

        # collaborations
        if year not in self.year_paperId_internal_collab:
            self.year_paperId_internal_collab[year] = {}
        self.year_paperId_internal_collab[year][paperId] = internal_collab

        if year not in self.year_paperId_external_inst_collab:
            self.year_paperId_external_inst_collab[year] = {}
        self.year_paperId_external_inst_collab[year][paperId] = external_inst_collab
        if year not in self.year_paperId_external_indiv_collab:
            self.year_paperId_external_indiv_collab[year] = {}
        self.year_paperId_external_indiv_collab[year][paperId] = external_indiv_collab
        if year not in self.year_paperId_indiv_collab:
            self.year_paperId_indiv_collab[year] = {}
        self.year_paperId_indiv_collab[year][paperId] = indiv_collab

        if year not in self.year_authorId_paperId_internal_collab:
            self.year_authorId_paperId_internal_collab[year] = {}
            self.year_authorId_paperId_external_collab[year] = {}
            self.year_authorId_paperId_indiv_collab[year] = {}
        for authorId in authorIds:
            if authorId not in self.year_authorId_paperId_internal_collab[year]:
                self.year_authorId_paperId_internal_collab[year][authorId] = {}
                self.year_authorId_paperId_external_collab[year][authorId] = {}
                self.year_authorId_paperId_indiv_collab[year][authorId] = {}
            internal_authorIds = copy.deepcopy(authorIds)
            internal_authorIds.remove(authorId)
            self.year_authorId_paperId_internal_collab[year][authorId][paperId] = internal_authorIds
            self.year_authorId_paperId_external_collab[year][authorId][paperId] = external_authorIds
            self.year_authorId_paperId_indiv_collab[year][authorId][paperId] = \
                internal_authorIds.union(external_authorIds)

        # citations
        if year not in self.year_paperId_citations:
            self.year_paperId_citations[year] = {}
        self.year_paperId_citations[year][paperId] = citations

        if year not in self.year_authorId_paperId_citations:
            self.year_authorId_paperId_citations[year] = {}
        for authorId in authorIds:
            if authorId not in self.year_authorId_paperId_citations[year]:
                self.year_authorId_paperId_citations[year][authorId] = {}
            self.year_authorId_paperId_citations[year][authorId][paperId] = citations

        # one-author paper citations
        if len(authorIds) == 1:
            if year not in self.year_paperId_citations_oneauthor:
                self.year_paperId_citations_oneauthor[year] = {}
            self.year_paperId_citations_oneauthor[year][paperId] = citations

            if year not in self.year_authorId_paperId_citations_oneauthor:
                self.year_authorId_paperId_citations_oneauthor[year] = {}
            for authorId in authorIds:
                if authorId not in self.year_authorId_paperId_citations_oneauthor[year]:
                    self.year_authorId_paperId_citations_oneauthor[year][authorId] = {}
                self.year_authorId_paperId_citations_oneauthor[year][authorId][paperId] = citations

        # two-author paper citations
        if len(authorIds) == 2:
            if year not in self.year_paperId_citations_twoauthor:
                self.year_paperId_citations_twoauthor[year] = {}
            self.year_paperId_citations_twoauthor[year][paperId] = citations

            if year not in self.year_authorId_paperId_citations_twoauthor:
                self.year_authorId_paperId_citations_twoauthor[year] = {}
            for authorId in authorIds:
                if authorId not in self.year_authorId_paperId_citations_twoauthor[year]:
                    self.year_authorId_paperId_citations_twoauthor[year][authorId] = {}
                self.year_authorId_paperId_citations_twoauthor[year][authorId][paperId] = citations

        # three-author paper citations
        if len(authorIds) == 3:
            if year not in self.year_paperId_citations_threeauthor:
                self.year_paperId_citations_threeauthor[year] = {}
            self.year_paperId_citations_threeauthor[year][paperId] = citations
            if year not in self.year_authorId_paperId_citations_threeauthor:
                self.year_authorId_paperId_citations_threeauthor[year] = {}
            for authorId in authorIds:
                if authorId not in self.year_authorId_paperId_citations_threeauthor[year]:
                    self.year_authorId_paperId_citations_threeauthor[year][authorId] = {}
                self.year_authorId_paperId_citations_threeauthor[year][authorId][paperId] = citations

        # one-and-two-author paper citations
        if len(authorIds) in [1, 2]:
            if year not in self.year_paperId_citations_onetwoauthor:
                self.year_paperId_citations_onetwoauthor[year] = {}
            self.year_paperId_citations_onetwoauthor[year][paperId] = citations

            if year not in self.year_authorId_paperId_citations_onetwoauthor:
                self.year_authorId_paperId_citations_onetwoauthor[year] = {}
            for authorId in authorIds:
                if authorId not in self.year_authorId_paperId_citations_onetwoauthor[year]:
                    self.year_authorId_paperId_citations_onetwoauthor[year][authorId] = {}
                self.year_authorId_paperId_citations_onetwoauthor[year][authorId][paperId] = citations

        # three-to-six-author paper citations
        if len(authorIds) in [3, 4, 5, 6]:
            if year not in self.year_paperId_citations_three2sixauthor:
                self.year_paperId_citations_three2sixauthor[year] = {}
            self.year_paperId_citations_three2sixauthor[year][paperId] = citations

            if year not in self.year_authorId_paperId_citations_three2sixauthor:
                self.year_authorId_paperId_citations_three2sixauthor[year] = {}
            for authorId in authorIds:
                if authorId not in self.year_authorId_paperId_citations_three2sixauthor[year]:
                    self.year_authorId_paperId_citations_three2sixauthor[year][authorId] = {}
                self.year_authorId_paperId_citations_three2sixauthor[year][authorId][paperId] = citations

    def update_affiliation(self, authorId_first_year):
        """
        paper-specific properties --> affiliation-specific properties
        :return:
        """

        # authorIds and size
        for year in self.year_paperId_authorIds:
            self.year_authorIds[year] = set()
            for paperId in self.year_paperId_authorIds[year]:
                authorIds = self.year_paperId_authorIds[year][paperId]
                self.year_authorIds[year] = self.year_authorIds[year].union(authorIds)
            self.year_size[year] = len(self.year_authorIds[year])

        # cumulative authorIds and size
        years = list(self.year_size.keys())
        years.sort()
        first_year = years[0]
        self.year_cumul_authorIds[first_year] = set(self.year_authorIds[first_year])
        for i in range(1, len(years)):
            cur_year = years[i]
            prev_year = years[i-1]
            self.year_cumul_authorIds[cur_year] = self.year_cumul_authorIds[prev_year].union(set(self.year_authorIds[cur_year]))
        for year in self.year_cumul_authorIds:
            self.year_cumul_size[year] = len(self.year_cumul_authorIds[year])

        # internal collaborations
        for year in self.year_paperId_internal_collab:
            self.year_internal_collab[year] = set()
            for paperId in self.year_paperId_internal_collab[year]:
                internal_collab = self.year_paperId_internal_collab[year][paperId]
                self.year_internal_collab[year] = self.year_internal_collab[year].union(internal_collab)
        years = list(self.year_internal_collab.keys())
        years.sort()
        first_year = years[0]
        self.year_cumul_internal_collab[first_year] = self.year_internal_collab[first_year]
        for i in range(1, len(years)):
            cur_year = years[i]
            prev_year = years[i-1]
            self.year_cumul_internal_collab[cur_year] = self.year_cumul_internal_collab[prev_year].union(self.year_internal_collab[cur_year])
        for year in self.year_internal_collab:
            self.year_internal_collab[year] = len(self.year_internal_collab[year]) // 2
            self.year_cumul_internal_collab[year] = len(self.year_cumul_internal_collab[year]) // 2
            self.year_avg_internal_collab[year] = self.year_internal_collab[year] / self.year_size[year]

        for year in self.year_authorId_paperId_internal_collab:
            self.year_authorId_internal_collab[year] = {}
            for authorId in self.year_authorId_paperId_internal_collab[year]:
                if authorId not in self.year_authorId_internal_collab[year]:
                    self.year_authorId_internal_collab[year][authorId] = set()
                for paperId in self.year_authorId_paperId_internal_collab[year][authorId]:
                    internal_collab = self.year_authorId_paperId_internal_collab[year][authorId][paperId]
                    self.year_authorId_internal_collab[year][authorId] = self.year_authorId_internal_collab[year][authorId].union(internal_collab)
        for year in self.year_authorId_internal_collab:
            for authorId in self.year_authorId_internal_collab[year]:
                self.year_authorId_internal_collab[year][authorId] = len(self.year_authorId_internal_collab[year][authorId])

        # external institutional collaborations
        for year in self.year_paperId_external_inst_collab:
            self.year_external_inst_collab[year] = set()
            for paperId in self.year_paperId_internal_collab[year]:
                external_inst_collab = self.year_paperId_external_inst_collab[year][paperId]
                self.year_external_inst_collab[year] = self.year_external_inst_collab[year].union(external_inst_collab)
        years = list(self.year_external_inst_collab.keys())
        years.sort()
        first_year = years[0]
        self.year_cumul_external_inst_collab[first_year] = self.year_external_inst_collab[first_year]
        for i in range(1, len(years)):
            cur_year = years[i]
            prev_year = years[i-1]
            self.year_cumul_external_inst_collab[cur_year] = self.year_cumul_external_inst_collab[prev_year].union(self.year_external_inst_collab[cur_year])
        for year in self.year_external_inst_collab:
            self.year_external_inst_collab[year] = len(self.year_external_inst_collab[year])
            self.year_cumul_external_inst_collab[year] = len(self.year_cumul_external_inst_collab[year])
            self.year_avg_external_inst_collab[year] = self.year_external_inst_collab[year] / self.year_size[year]

        # external individual collaborations
        for year in self.year_paperId_external_indiv_collab:
            self.year_external_indiv_collab[year] = set()
            for paperId in self.year_paperId_external_indiv_collab[year]:
                external_indiv_collab = self.year_paperId_external_indiv_collab[year][paperId]
                self.year_external_indiv_collab[year] = self.year_external_indiv_collab[year].union(external_indiv_collab)
        years = list(self.year_external_indiv_collab.keys())
        years.sort()
        first_year = years[0]
        self.year_cumul_external_indiv_collab[first_year] = self.year_external_indiv_collab[first_year]
        for i in range(1, len(years)):
            cur_year = years[i]
            prev_year = years[i-1]
            self.year_cumul_external_indiv_collab[cur_year] = self.year_cumul_external_indiv_collab[prev_year].union(self.year_external_indiv_collab[cur_year])
        for year in self.year_external_indiv_collab:
            self.year_external_indiv_collab[year] = len(self.year_external_indiv_collab[year]) // 2
            self.year_cumul_external_indiv_collab[year] = len(self.year_cumul_external_indiv_collab[year]) // 2
            self.year_avg_external_indiv_collab[year] = self.year_external_indiv_collab[year] / self.year_size[year]

        for year in self.year_authorId_paperId_external_collab:
            self.year_authorId_external_collab[year] = {}
            for authorId in self.year_authorId_paperId_external_collab[year]:
                if authorId not in self.year_authorId_external_collab[year]:
                    self.year_authorId_external_collab[year][authorId] = set()
                for paperId in self.year_authorId_paperId_external_collab[year][authorId]:
                    external_collab = self.year_authorId_paperId_external_collab[year][authorId][paperId]
                    self.year_authorId_external_collab[year][authorId] = self.year_authorId_external_collab[year][authorId].union(external_collab)
        for year in self.year_authorId_external_collab:
            for authorId in self.year_authorId_external_collab[year]:
                self.year_authorId_external_collab[year][authorId] = len(self.year_authorId_external_collab[year][authorId])

        # individual collaborations
        for year in self.year_paperId_indiv_collab:
            self.year_indiv_collab[year] = set()
            for paperId in self.year_paperId_indiv_collab[year]:
                indiv_collab = self.year_paperId_indiv_collab[year][paperId]
                self.year_indiv_collab[year] = self.year_indiv_collab[year].union(indiv_collab)
        years = list(self.year_indiv_collab.keys())
        years.sort()
        first_year = years[0]
        self.year_cumul_indiv_collab[first_year] = self.year_indiv_collab[first_year]
        for i in range(1, len(years)):
            cur_year = years[i]
            prev_year = years[i-1]
            self.year_cumul_indiv_collab[cur_year] = self.year_cumul_indiv_collab[prev_year].union(self.year_indiv_collab[cur_year])
        for year in self.year_indiv_collab:
            self.year_indiv_collab[year] = len(self.year_indiv_collab[year]) // 2
            self.year_cumul_indiv_collab[year] = len(self.year_cumul_indiv_collab[year]) // 2
            self.year_avg_indiv_collab[year] = self.year_indiv_collab[year] / self.year_size[year]

        for year in self.year_authorId_paperId_indiv_collab:
            self.year_authorId_indiv_collab[year] = {}
            for authorId in self.year_authorId_paperId_indiv_collab[year]:
                if authorId not in self.year_authorId_indiv_collab[year]:
                    self.year_authorId_indiv_collab[year][authorId] = set()
                for paperId in self.year_authorId_paperId_indiv_collab[year][authorId]:
                    indiv_collab = self.year_authorId_paperId_indiv_collab[year][authorId][paperId]
                    self.year_authorId_indiv_collab[year][authorId] = self.year_authorId_indiv_collab[year][authorId].union(indiv_collab)
        for year in self.year_authorId_indiv_collab:
            for authorId in self.year_authorId_indiv_collab[year]:
                self.year_authorId_indiv_collab[year][authorId] = len(self.year_authorId_indiv_collab[year][authorId])

        # production and productivity
        for year in self.year_paperId_authorIds:
            self.year_production[year] = len(self.year_paperId_authorIds[year])
        for year in self.year_paperId_contribution:
            self.year_productivity[year] = sum(self.year_paperId_contribution[year].values())
        years = list(self.year_production)
        years.sort()
        first_year = years[0]
        self.year_cumul_production[first_year] = self.year_production[first_year]
        self.year_cumul_productivity[first_year] = self.year_productivity[first_year]
        for i in range(1, len(years)):
            cur_year = years[i]
            prev_year = years[i-1]
            self.year_cumul_production[cur_year] = self.year_cumul_production[prev_year] + self.year_production[cur_year]
            self.year_cumul_productivity[cur_year] = self.year_cumul_productivity[prev_year] + self.year_productivity[cur_year]

        # teamsize
        for year in self.year_paperId_teamsize:
            self.year_avg_teamsize[year] = sum(self.year_paperId_teamsize[year].values()) / len(self.year_paperId_teamsize[year])
        for year in self.year_paperId_internal_teamsize:
            self.year_avg_internal_teamsize[year] = sum(self.year_paperId_internal_teamsize[year].values()) / len(self.year_paperId_internal_teamsize[year])
        for year in self.year_paperId_external_teamsize:
            self.year_avg_external_teamsize[year] = sum(self.year_paperId_external_teamsize[year].values()) / len(self.year_paperId_external_teamsize[year])

        for year in self.year_authorId_teamsizes:
            if year not in self.year_authorId_avg_teamsize:
                self.year_authorId_avg_teamsize[year] = {}
            for authorId in self.year_authorId_teamsizes[year]:
                self.year_authorId_avg_teamsize[year][authorId] = \
                    sum(self.year_authorId_teamsizes[year][authorId]) / len(self.year_authorId_teamsizes[year][authorId])

        # citations and average impact
        for year in self.year_paperId_citations:
            self.year_citations[year] = sum(self.year_paperId_citations[year].values())
        for year in self.year_citations:
            self.year_avg_impact[year] = 0 if len(self.year_citations) == 0 \
                else self.year_citations[year] / len(self.year_paperId_citations[year])

        for year in self.year_authorId_paperId_citations:
            if year not in self.year_authorId_citations:
                self.year_authorId_citations[year] = {}
                self.year_authorId_avg_impact[year] = {}
            for authorId in self.year_authorId_paperId_citations[year]:
                self.year_authorId_citations[year][authorId] = sum(self.year_authorId_paperId_citations[year][authorId].values())
                self.year_authorId_avg_impact[year][authorId] = 0 if len(self.year_authorId_paperId_citations[year][authorId]) == 0 \
                    else self.year_authorId_citations[year][authorId] / len(self.year_authorId_paperId_citations[year][authorId])
                # if len(self.year_authorId_paperId_citations[year][authorId]) != 1:
                #     print(self.year_authorId_citations[year][authorId], len(self.year_authorId_paperId_citations[year][authorId]))

        # citations and average impact of one-author papers
        for year in self.year_paperId_citations_oneauthor:
            self.year_citations_oneauthor[year] = sum(self.year_paperId_citations_oneauthor[year].values())
        for year in self.year_citations_oneauthor:
            self.year_avg_impact_oneauthor[year] = 0 if len(self.year_citations_oneauthor) == 0 \
                else self.year_citations_oneauthor[year] / len(self.year_paperId_citations_oneauthor[year])

        for year in self.year_authorId_paperId_citations_oneauthor:
            if year not in self.year_authorId_citations_oneauthor:
                self.year_authorId_citations_oneauthor[year] = {}
                self.year_authorId_avg_impact_oneauthor[year] = {}
            for authorId in self.year_authorId_paperId_citations_oneauthor[year]:
                self.year_authorId_citations_oneauthor[year][authorId] = sum(self.year_authorId_paperId_citations_oneauthor[year][authorId].values())
                self.year_authorId_avg_impact_oneauthor[year][authorId] = 0 if len(self.year_authorId_paperId_citations_oneauthor[year][authorId]) == 0 \
                    else self.year_authorId_citations_oneauthor[year][authorId] / len(self.year_authorId_paperId_citations_oneauthor[year][authorId])

        # citations and average impact of two-author papers
        for year in self.year_paperId_citations_twoauthor:
            self.year_citations_twoauthor[year] = sum(self.year_paperId_citations_twoauthor[year].values())
        for year in self.year_citations_twoauthor:
            self.year_avg_impact_twoauthor[year] = 0 if len(self.year_citations_twoauthor) == 0 \
                else self.year_citations_twoauthor[year] / len(self.year_paperId_citations_twoauthor[year])

        for year in self.year_authorId_paperId_citations_twoauthor:
            if year not in self.year_authorId_citations_twoauthor:
                self.year_authorId_citations_twoauthor[year] = {}
                self.year_authorId_avg_impact_twoauthor[year] = {}
            for authorId in self.year_authorId_paperId_citations_twoauthor[year]:
                self.year_authorId_citations_twoauthor[year][authorId] = sum(self.year_authorId_paperId_citations_twoauthor[year][authorId].values())
                self.year_authorId_avg_impact_twoauthor[year][authorId] = 0 if len(self.year_authorId_paperId_citations_twoauthor[year][authorId]) == 0 \
                    else self.year_authorId_citations_twoauthor[year][authorId] / len(self.year_authorId_paperId_citations_twoauthor[year][authorId])

        # citations and average impact of three-author papers
        for year in self.year_paperId_citations_threeauthor:
            self.year_citations_threeauthor[year] = sum(self.year_paperId_citations_threeauthor[year].values())

        for year in self.year_citations_threeauthor:
            self.year_avg_impact_threeauthor[year] = 0 if len(self.year_citations_threeauthor) == 0 \
                else self.year_citations_threeauthor[year] / len(self.year_paperId_citations_threeauthor[year])

        for year in self.year_authorId_paperId_citations_threeauthor:
            if year not in self.year_authorId_citations_threeauthor:
                self.year_authorId_citations_threeauthor[year] = {}
                self.year_authorId_avg_impact_threeauthor[year] = {}
            for authorId in self.year_authorId_paperId_citations_threeauthor[year]:
                self.year_authorId_citations_threeauthor[year][authorId] = sum(self.year_authorId_paperId_citations_threeauthor[year][authorId].values())
                self.year_authorId_avg_impact_threeauthor[year][authorId] = 0 if len(self.year_authorId_paperId_citations_threeauthor[year][authorId]) == 0 \
                    else self.year_authorId_citations_threeauthor[year][authorId] / len(self.year_authorId_paperId_citations_threeauthor[year][authorId])

        # citations and average impact of one-and-two-author papers
        for year in self.year_paperId_citations_onetwoauthor:
            self.year_citations_onetwoauthor[year] = sum(self.year_paperId_citations_onetwoauthor[year].values())
        for year in self.year_citations_onetwoauthor:
            self.year_avg_impact_onetwoauthor[year] = 0 if len(self.year_citations_onetwoauthor) == 0 \
                else self.year_citations_onetwoauthor[year] / len(self.year_paperId_citations_onetwoauthor[year])

        for year in self.year_authorId_paperId_citations_onetwoauthor:
            if year not in self.year_authorId_citations_onetwoauthor:
                self.year_authorId_citations_onetwoauthor[year] = {}
                self.year_authorId_avg_impact_onetwoauthor[year] = {}
            for authorId in self.year_authorId_paperId_citations_onetwoauthor[year]:
                self.year_authorId_citations_onetwoauthor[year][authorId] = sum(self.year_authorId_paperId_citations_onetwoauthor[year][authorId].values())
                self.year_authorId_avg_impact_onetwoauthor[year][authorId] = 0 if len(self.year_authorId_paperId_citations_onetwoauthor[year][authorId]) == 0 \
                    else self.year_authorId_citations_onetwoauthor[year][authorId] / len(self.year_authorId_paperId_citations_onetwoauthor[year][authorId])

        # citations and average impact of three-to-six-author papers
        for year in self.year_paperId_citations_three2sixauthor:
            self.year_citations_three2sixauthor[year] = sum(self.year_paperId_citations_three2sixauthor[year].values())
        for year in self.year_citations_three2sixauthor:
            self.year_avg_impact_three2sixauthor[year] = 0 if len(self.year_citations_three2sixauthor) == 0 \
                else self.year_citations_three2sixauthor[year] / len(self.year_paperId_citations_three2sixauthor[year])

        for year in self.year_authorId_paperId_citations_three2sixauthor:
            if year not in self.year_authorId_citations_three2sixauthor:
                self.year_authorId_citations_three2sixauthor[year] = {}
                self.year_authorId_avg_impact_three2sixauthor[year] = {}
            for authorId in self.year_authorId_paperId_citations_three2sixauthor[year]:
                self.year_authorId_citations_three2sixauthor[year][authorId] = sum(self.year_authorId_paperId_citations_three2sixauthor[year][authorId].values())
                self.year_authorId_avg_impact_three2sixauthor[year][authorId] = 0 if len(self.year_authorId_paperId_citations_three2sixauthor[year][authorId]) == 0 \
                    else self.year_authorId_citations_three2sixauthor[year][authorId] / len(self.year_authorId_paperId_citations_three2sixauthor[year][authorId])

        # seniority
        for year in self.year_authorIds:
            authorIds = self.year_authorIds[year]
            for authorId in authorIds:
                seniority = get_seniority(authorId_first_year, authorId, year)
                if seniority >= 5:
                    if year not in self.year_authorIds_5:
                        self.year_authorIds_5[year] = 0
                    self.year_authorIds_5[year] += 1
                if seniority >= 10:
                    if year not in self.year_authorIds_10:
                        self.year_authorIds_10[year] = 0
                    self.year_authorIds_10[year] += 1
                if seniority >= 15:
                    if year not in self.year_authorIds_15:
                        self.year_authorIds_15[year] = 0
                    self.year_authorIds_15[year] += 1
                if seniority >= 20:
                    if year not in self.year_authorIds_20:
                        self.year_authorIds_20[year] = 0
                    self.year_authorIds_20[year] += 1

        # release the memory of paper-specific properties that will not be used anymore
        self.year_paperId_authorIds = {}
        self.year_cumul_authorIds = {}
        self.year_authorIds = {}
        self.year_paperId_contribution = {}
        self.year_paperId_teamsize = {}
        self.year_paperId_internal_teamsize = {}
        self.year_paperId_external_teamsize = {}
        self.year_paperId_internal_collab = {}
        self.year_paperId_external_inst_collab = {}
        self.year_paperId_external_indiv_collab = {}
        self.year_paperId_indiv_collab = {}
        self.year_paperId_citations = {}
        self.year_paperId_citations_oneauthor = {}
        self.year_paperId_citations_twoauthor = {}
        self.year_paperId_citations_threeauthor = {}
        self.year_paperId_citations_onetwoauthor = {}
        self.year_paperId_citations_three2sixauthor = {}


        self.year_authorId_paperId_internal_collab = {}
        self.year_authorId_paperId_external_collab = {}
        self.year_authorId_paperId_indiv_collab = {}
        self.year_authorId_teamsizes = {}
        self.year_authorId_paperId_citations = {}
        self.year_authorId_citations = {}
        self.year_authorId_paperId_citations_oneauthor = {}
        self.year_authorId_citations_oneauthor = {}
        self.year_authorId_paperId_citations_twoauthor = {}
        self.year_authorId_citations_twoauthor = {}
        self.year_authorId_paperId_citations_threeauthor = {}
        self.year_authorId_citations_threeauthor = {}
        self.year_authorId_paperId_citations_onetwoauthor = {}
        self.year_authorId_citations_onetwoauthor = {}
        self.year_authorId_paperId_citations_three2sixauthor = {}
        self.year_authorId_citations_three2sixauthor = {}
