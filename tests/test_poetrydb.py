import pytest
import requests

BASE_URL = "https://poetrydb.org"
AUTHORS_ENDPOINT = "author"
TITLE_ENDPOINT = "title"
LINECOUNT_ENDPOINT = "linecount"
POEMCOUNT_ENDPOINT = "poemcount"
RANDOM_ENDPOINT = "random"
TEXT_FORMAT = ".text"
EXACT_MATCH_PARAM = ":abs"

SAMPLE_AUTHORS = ["William Shakespeare","Adam Lindsay Gordon", "William Wordsworth"]
SAMPLE_COMBINED_VALUES = ["Winter","William Shakespeare","14","1"]
SAMPLE_COMBINED_FIELDS = [TITLE_ENDPOINT, AUTHORS_ENDPOINT, LINECOUNT_ENDPOINT, POEMCOUNT_ENDPOINT]
SAMPLE_AUTHOR_FIELDS = ["author","title","linecount"]
SAMPLE_TITLE_FIELDS = ["title","lines"]
SAMPLE_KEYWORD = "spring"
SAMPLE_FULL_TITLE = "403. The Soldier’s Return: A Ballad"
SAMPLE_TITLE = "Ozymandias"
SAMPLE_UNKNOWN_AUTHOR = 'William Milkshake'
SAMPLE_UNKNOWN_TITLE_KEYWORD = '^^%#Stranger Things 4'
SAMPLE_RANDOM_POEMS_COUNT = '3'

EXPECTED_SHAKESPREARE_POEM = {
    SAMPLE_AUTHOR_FIELDS[0]: 'William Shakespeare',
    SAMPLE_AUTHOR_FIELDS[1]: 'Sonnet 99: The forward violet thus did I chide',
    SAMPLE_AUTHOR_FIELDS[2]: '15'}
EXPECTED_AUTHORS_COUNT = 129
EXPECTED_SHAKESPREARE_POEMS_COUNT = 162
EXPECTED_SPRING_POEMS_COUNT = 51
EXPECTED_POEM_CONTENT = """Tell that its sculptor well those passions read
Which yet survive, stamped on these lifeless things,
The hand that mocked them, and the heart that fed:
And on the pedestal these words appear:"""


def generate_url(base_url, *argv):
    params = ""
    for arg in argv: params += "/" + arg
    return base_url + params

def assert_correct_response(response):
    assert response.status_code == 200
    assert response.reason == "OK"

@pytest.mark.smoke
@pytest.mark.author
def test_get_all_authors():
    response = requests.get(generate_url(BASE_URL, AUTHORS_ENDPOINT))
    assert_correct_response(response)
    authors = response.json()['authors']
    assert len(authors) == EXPECTED_AUTHORS_COUNT
    assert all(element in authors for element in SAMPLE_AUTHORS)
    assert 'William Milkshake' not in authors

@pytest.mark.author
def test_get_specific_data_by_author():
    response = requests.get(generate_url(BASE_URL, AUTHORS_ENDPOINT, SAMPLE_AUTHORS[0], ",".join(SAMPLE_AUTHOR_FIELDS)))
    assert_correct_response(response)
    assert len(response.json()) == EXPECTED_SHAKESPREARE_POEMS_COUNT
    assert any(x == EXPECTED_SHAKESPREARE_POEM for x in response.json())

@pytest.mark.author
def test_get_404_response_on_unknown_author():
    response = requests.get(generate_url(BASE_URL, AUTHORS_ENDPOINT, SAMPLE_UNKNOWN_AUTHOR, ",".join(SAMPLE_AUTHOR_FIELDS)))
    assert_correct_response(response)
    assert response.json()["reason"] == 'Not found'
    assert response.json()["status"] == 404

@pytest.mark.title
def test_get_titles_by_keyword():
    response = requests.get(generate_url(BASE_URL, TITLE_ENDPOINT, SAMPLE_KEYWORD, "title"))
    assert_correct_response(response)
    assert len(response.json()) == EXPECTED_SPRING_POEMS_COUNT
    assert all(SAMPLE_KEYWORD.casefold() in x["title"].casefold() for x in response.json())

@pytest.mark.title
def test_get_title_by_exact_match_title():
    response = requests.get(generate_url(BASE_URL, TITLE_ENDPOINT, SAMPLE_FULL_TITLE + EXACT_MATCH_PARAM, "title"))
    assert_correct_response(response)
    assert len(response.json()) == 1
    assert SAMPLE_FULL_TITLE in response.json()[0]["title"]

@pytest.mark.title
def test_get_404_response_on_unfound_title_keyword():
    response = requests.get(generate_url(BASE_URL, TITLE_ENDPOINT, SAMPLE_UNKNOWN_TITLE_KEYWORD, "title"))
    assert_correct_response(response)
    assert response.json()["reason"] == 'Not found'
    assert response.json()["status"] == 404

@pytest.mark.title
def test_get_specific_data_in_text_format_by_title():
    response = requests.get(generate_url(BASE_URL, TITLE_ENDPOINT, SAMPLE_TITLE, ",".join(SAMPLE_TITLE_FIELDS) + TEXT_FORMAT))
    assert_correct_response(response)
    content = response.text
    assert response.headers.get('content-type') == 'application/json'
    assert all(element in content for element in SAMPLE_TITLE_FIELDS)
    assert SAMPLE_TITLE in content
    assert all(element in content for element in EXPECTED_POEM_CONTENT.splitlines())

@pytest.mark.title
def test_get_specific_data_in_text_format_by_title():
    response = requests.get(generate_url(BASE_URL, TITLE_ENDPOINT, SAMPLE_TITLE, ",".join(SAMPLE_TITLE_FIELDS) + TEXT_FORMAT))
    assert_correct_response(response)
    content = response.text
    assert response.headers.get('content-type') == 'application/json'
    assert all(element in content for element in SAMPLE_TITLE_FIELDS)
    assert SAMPLE_TITLE in content
    assert all(element in content for element in EXPECTED_POEM_CONTENT.splitlines())

@pytest.mark.random
def test_get_data_of_three_random_poems():
    response = requests.get(generate_url(BASE_URL,
                                         RANDOM_ENDPOINT,
                                         SAMPLE_RANDOM_POEMS_COUNT,
                                         ",".join(SAMPLE_AUTHOR_FIELDS)))
    assert_correct_response(response)
    content = response.json()
    assert len(content) == int(SAMPLE_RANDOM_POEMS_COUNT)
    for element in content:
        assert any(True for item in SAMPLE_AUTHOR_FIELDS if item in element.keys())

@pytest.mark.combined
def test_get_combined_data_by_title_author_linecount_and_poem_count():
    response = requests.get(generate_url(BASE_URL,
                                         ",".join(SAMPLE_COMBINED_FIELDS),
                                         ";".join(SAMPLE_COMBINED_VALUES)))
    assert_correct_response(response)
    content = response.json()[0]    
    assert SAMPLE_COMBINED_VALUES[0].casefold() in content["title"].casefold()
    assert SAMPLE_COMBINED_VALUES[1] in content["author"]
    assert int(SAMPLE_COMBINED_VALUES[2]) == len(content["lines"])
    assert int(SAMPLE_COMBINED_VALUES[3]) == len(response.json())