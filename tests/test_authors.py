from send_email.paper_tools import Author
import pytest

def test_no_initials():
    author = Author('J. Doe')
    assert str(author) == 'J. Doe'
    assert author.first_initial == 'J'
    assert author.middle_initials == []
    assert author.last_name == 'Doe'


def test_initials():
    author = Author('J. K. L. Doe')
    assert str(author) == 'J. K. L. Doe'
    assert author.first_initial == 'J'
    assert author.middle_initials == ['K', 'L']
    assert author.last_name == 'Doe'
