import feedparser
import re
import time
from HTML_tools import title_to_HTML, authors_to_HTML, abstract_to_HTML

class Author:
    def __init__(self, author_string):
        names = author_string.split(' ')
        assert len(names) > 1
        
        if '.' not in names[0]:
            self.first_name = names[0]
        else:
            self.first_name = None
            
        self.first_initial = names[0][0].capitalize()
        
        self.middle_initials = [middle_name[0] for middle_name in names[1:-1]]
        self.last_name = names[-1]
        
    def __str__(self):
        name = f'{self.first_initial}.'
            
        if self.middle_initials:
            for middle_initial in self.middle_initials:
                name += f' {middle_initial}.'
        name += f' {self.last_name}'
        return name
        
    def __repr__(self):
        if self.first_name is not None:
            name = self.first_name
        else:
            name = f'{self.first_initial}.'
            
        if self.middle_initials:
            for middle_initial in self.middle_initials:
                name += f' {middle_initial}.'
        name += f' {self.last_name}'
        return name
    
    def __eq__(self, other):
        if isinstance(other, str):
            try:
                other = Author(other)
            except:
                return False
        
        if not isinstance(other, Author):
            return False
        
        if other.first_initial != self.first_initial or other.last_name != self.last_name:
            return False
        
        if other.middle_initials and self.middle_initials:
            if len(other.middle_initials) != len(self.middle_initials):
                return False
            else:
                for other_initial, self_initial in zip(other.middle_initials, self.middle_initials):
                    if other_initial != self_initial:
                        return False
        
        return True

class Paper:
    def __init__(self, authors, title, abstract, link, journal, pdf_link=None):
        self.authors = authors
        self.title = title
        self.abstract = abstract.replace('\n', ' ')
        self.link = link
        self.pdf_link = pdf_link
        self.journal = journal
        
        self.result = None
        
    @property
    def author_list(self):
        return ', '.join(str(author) for author in self.authors)
    
    def __repr__(self):
        return f'{self.authors[0]} et al. - {self.title}'
        
    def matches(self, authors=None, title_keywords=None, abstract_keywords=None,
                update=False):
        result = {}
        if authors is not None:
            matching_authors = [author for author in authors if author in self.authors]
            if matching_authors:
                result['authors'] = matching_authors
        if title_keywords is not None:
            matching_title_keywords = [title_keyword for title_keyword in title_keywords
                                       if title_keyword.lower() in self.title.lower()]
            if matching_title_keywords:
                result['title_keywords'] = matching_title_keywords
        if abstract_keywords is not None:
            matching_abstract_keywords = [abstract_keyword for abstract_keyword in abstract_keywords
                                          if abstract_keyword.lower() in self.abstract.lower()]
            if matching_abstract_keywords:
                result['abstract_keywords'] = matching_abstract_keywords
        
        if update:
            self.result = result
        return result

    def HTML_summary(self, id=None):
        HTML_title = title_to_HTML(self.title, 
                                   bold_keywords=self.result.get('title_keywords', []),
                                   link=self.link,
                                   pdf_link=self.pdf_link)
        HTML_authors = authors_to_HTML(self.authors, 
                                       bold_authors=self.result.get('authors', []),
                                       max_authors=3)

        HTML_abstract = 'abstract'
        if 'abstract_keywords' in self.result:
            HTML_abstract += '(' + ', '.join(self.result['abstract_keywords']) + ')'
        if id is not None:
            HTML_abstract = f'<a href="#abstract-{id}" style="text-decoration: none"><span>{HTML_abstract}</span></a>'

        HTML = f'{HTML_title}{HTML_authors} | {self.journal} | {HTML_abstract}'
        HTML = f'<div>{HTML}</div>'
        return HTML

    def HTML_abstract(self, id=None):
        HTML_title = title_to_HTML(self.title, 
                                   bold_keywords=self.result.get('title_keywords', []),
                                   link=self.link,
                                   pdf_link=self.pdf_link,
                                   id=id)
        HTML_authors = authors_to_HTML(self.authors, 
                                       bold_authors=self.result.get('authors', []),
                                       max_authors=None)
        HTML_abstract = abstract_to_HTML(self.abstract,
                                         bold_keywords=self.result.get('abstract_keywords', []))
        HTML = f'{HTML_title}'
        HTML += f'<a href="#Top" style="text-decoration: none"><span>[Top]</span></a> - {HTML_authors} | {self.journal}'
        HTML += f'<br><hr style="margin:0pt">{HTML_abstract}'

        return HTML
    
def filter_papers(papers, authors=[], title_keywords=[], abstract_keywords=[]):
    filtered_papers = []
    for paper in papers:
        result = paper.matches(authors=authors,
                               title_keywords=title_keywords,
                               abstract_keywords=abstract_keywords,
                               update=True)
        if result:
            filtered_papers.append(paper)
    return filtered_papers

def sort_papers(papers, sort_order, authors=[], title_keywords=[], abstract_keywords=[]):
    if not papers:
        return []
    if not sort_order:
        return list(papers)
    
    first_sort_name = sort_order[0]
    first_sort = eval(first_sort_name)
    
    papers_first_sort = []
    papers_no_first_sort = []
    for paper in papers:
        if first_sort_name in paper.result and paper.matches(**{first_sort_name: first_sort}):
            papers_first_sort.append(paper)
        else:
            papers_no_first_sort.append(paper)
            
    sorted_papers = []
    # Continue sorting by other conditions if they exist
    for papers_segment in [papers_first_sort, papers_no_first_sort]:
        sorted_papers += sort_papers(papers=papers_segment,
                                     sort_order=sort_order[1:],
                                     authors=authors,
                                     title_keywords=title_keywords,
                                     abstract_keywords=abstract_keywords)
        
    return sorted_papers
