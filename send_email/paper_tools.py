import re
import time
from .HTML_tools import title_to_HTML, authors_to_HTML
from . import RSS_feed_parsers, RSS_urls


class Author:
    def __init__(self, author_string):
        author_string = author_string.replace('   ', ' ')
        author_string = author_string.replace('  ', ' ')
        author_string = author_string.replace('. ', '.').replace('.', '. ')
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
    def __init__(self, authors, title, abstract, link, journal, date,
                 pdf_link=None):
        self.authors = authors
        self.title = title
        self.abstract = abstract.replace('\n', ' ')
        self.link = link
        self.pdf_link = pdf_link
        self.journal = journal
        self.date = date

        self.result = None

    @property
    def author_list(self):
        return ', '.join(str(author) for author in self.authors)

    def __repr__(self):
        return f'{self.authors[0]} et al. - {self.title}'

    def matches(self, authors=None, title_keywords=None,
                abstract_keywords=None,
                update=False):
        result = {}
        if authors is not None:
            matching_authors = [author for author in authors if author in self.authors]
            if matching_authors:
                result['authors'] = matching_authors
        if title_keywords is not None:
            matching_title_keywords = [keyword for keyword in title_keywords
                                       if keyword.lower() in self.title.lower()]
            if matching_title_keywords:
                result['title_keywords'] = matching_title_keywords
        if abstract_keywords is not None:
            matching_abstract_keywords = [keyword for keyword in abstract_keywords
                                          if keyword.lower() in self.abstract.lower()]
            if matching_abstract_keywords:
                result['abstract_keywords'] = matching_abstract_keywords

        if update:
            self.result = result
        return result

    def HTML_highlight(self, id=None):
        HTML_title = title_to_HTML(self.title,
                                   bold_keywords=self.result.get('title_keywords', []),
                                   link=None if id is None else f'#abstract-{id}')
        HTML_authors = authors_to_HTML(self.authors,
                                       bold_authors=self.result.get('authors', []),
                                       max_authors=3)

        HTML_journal = f'<a href="{self.link}" style="text-decoration: none">' \
                            f'<span>{self.journal}</span></a>'

        HTML = f'{HTML_title}{HTML_authors} | {HTML_journal}'

        if self.pdf_link is not None:
            HTML += f' | <a href="{self.pdf_link}" style="text-decoration: none">PDF</a>'

        if 'abstract_keywords' in self.result:
            HTML += ' | Abstract keywords: ' + ', '.join(self.result['abstract_keywords'])

        HTML = f'<div>{HTML}</div>'
        return HTML

    def HTML_summary(self):
        HTML_title = title_to_HTML(self.title,
                                   bold_keywords=self.result.get('title_keywords', []),
                                   heading=None,
                                   link=self.link)
        HTML_authors = authors_to_HTML(self.authors,
                                       bold_authors=self.result.get('authors', []),
                                       max_authors=3)
        HTML = f'{HTML_title} - {HTML_authors}'
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

        HTML_abstract = self.abstract
        for bold_keyword in self.result.get('abstract_keywords', []):
            HTML_abstract = re.sub(bold_keyword, f'<b>{bold_keyword}</b>',
                                   HTML_abstract, flags=re.IGNORECASE)

        HTML = f'{HTML_title}'
        HTML += f'<a href="#Top" style="text-decoration: none"><span>[Top]</span></a> - {HTML_authors} | {self.journal}'
        HTML += f'<br><hr style="margin:0pt">{HTML_abstract}'

        return HTML


class Journal():
    def __init__(self, name, enabled, summary, date=None, **kwargs):
        assert name in RSS_urls, f"No RSS feed setup for {name}"

        self.name = name
        self.enabled = enabled
        self.summary = summary
        self.date = date

        self.RSS_url = RSS_urls[self.name]
        self.feed_parser = RSS_feed_parsers[self.name]

        self.filtered_papers = []
        self.sorted_papers = []

    def get_new_papers(self, authors, keywords,
                       sort_order=('authors', 'title_keywords', 'abstract_keywords')):
        self.papers = self.parse_feed()
        self.filtered_papers = self.filter_papers(papers=self.papers,
                                                  authors=authors,
                                                  keywords=keywords)
        self.sorted_papers = self.sort_papers(papers=self.filtered_papers,
                                              sort_order=sort_order,
                                              authors=authors,
                                              keywords=keywords)
        return self.sorted_papers

    def parse_feed(self):
        self.papers = self.feed_parser(self.RSS_url, journal=self.name)
        return self.papers

    def filter_papers(self, papers, authors=[], keywords=[]):
        self.filtered_papers = []
        for paper in papers:
            result = paper.matches(authors=authors,
                                   title_keywords=keywords,
                                   abstract_keywords=keywords,
                                   update=True)
            if result:
                self.filtered_papers.append(paper)
        return self.filtered_papers

    def sort_papers(self, papers, sort_order, authors=[], keywords=[]):
        if not papers:
            return []
        if not sort_order:
            return list(papers)

        first_sort_name = sort_order[0]
        if first_sort_name == 'authors':
            first_sort = authors
        elif first_sort_name in ['title_keywords', 'abstract_keywords']:
            first_sort = keywords
        else:
            raise SyntaxError('sorting must be authors, title_keywords, or abstract_')

        papers_first_sort = []
        papers_no_first_sort = []
        for paper in papers:
            if first_sort_name in paper.result and paper.matches(
                    **{first_sort_name: first_sort}):
                papers_first_sort.append(paper)
            else:
                papers_no_first_sort.append(paper)

        sorted_papers = []
        # Continue sorting by other conditions if they exist
        for papers_segment in [papers_first_sort, papers_no_first_sort]:
            sorted_papers += self.sort_papers(papers=papers_segment,
                                              sort_order=sort_order[1:],
                                              authors=authors,
                                              keywords=keywords)

        return sorted_papers