import re


def title_to_HTML(title, bold_keywords=[], link=None, id=None, pdf_link=None):
    title = title.lower().capitalize()
    for bold_keyword in bold_keywords:
        title = re.sub(bold_keyword, f'<b>{bold_keyword}</b>', title, flags=re.IGNORECASE)

    title_style = "font-weight:normal;margin:0;font-size:17px;max-width:44.5em;line-height:20px"

    HTML = title
    if link:
        HTML = f'<a href="{link}" style="text-decoration: none">{HTML}</a>'
    if pdf_link is not None:
        HTML = f'<a href="{pdf_link}" style="text-decoration: none">[PDF]</a> ' + HTML
    HTML = f'<h3 style="{title_style}">{HTML}</h3>'
    if id is not None:
        HTML = f'<a name="abstract-{id}"></a>' + HTML
    return HTML

def authors_to_HTML(authors, bold_authors=[], max_authors=None):
    HTML_authors = []
    author_idx = 0
    for k, author in enumerate(authors):
        if author in bold_authors:
            if author_idx > 0:
                HTML_authors += [f'({author_idx})']
                author_idx = 0
            HTML_authors += [f'<b>{repr(author)}</b>']
        elif 0 < k < len(authors) -1 and max_authors is not None and len(authors) > max_authors:
            author_idx += 1
        else:
            if author_idx > 0:
                HTML_authors += [f'({author_idx})']
                author_idx = 0
            HTML_authors += [str(author)]

    HTML = ', '.join(HTML_authors)
    HTML = f'<i>{HTML}</i>'
    return HTML


def create_HTML_paper_highlights(papers):
    HTML_papers = [paper.HTML_highlight(id=id) for id, paper in enumerate(papers)]
    HTML = '<br>'.join(HTML_papers)
    return HTML


def create_HTML_journal_summary(journal):
    HTML = f'<H2>{journal.name}</H2>'
    HTML += '<br>'.join([paper.HTML_summary() for paper in journal.papers])
    return HTML


def create_HTML_paper_abstracts(papers):
    HTML_papers = [paper.HTML_abstract(id=id) for id, paper in enumerate(papers)]
    HTML = '<br><br>'.join(HTML_papers)
    return HTML


def create_email_HTML(journals):
    HTML = '<a name="Top"></a><H2 id="top">Highlighted papers</H2>'
    highlighted_papers = [paper for journal in journals
                          for paper in journal.sorted_papers]
    HTML += create_HTML_paper_highlights(highlighted_papers)

    if any(journal.summary for journal in journals):
        HTML += '<H2>Paper summaries</H2>'
        for journal in journals:
            if journal.summary:
                HTML += create_HTML_journal_summary(journal)

    HTML += '<H2>Paper abstracts</H2>'
    HTML += create_HTML_paper_abstracts(highlighted_papers)
    return HTML