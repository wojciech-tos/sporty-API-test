# Sporty.com task

## How to run PoetryAPI test:

- Clone this repository locally
- Enter main folder **sporty_WAP_task**
- Install, create and activate virtual environment
> pip install virtualenv

> virtualenv venv

> source venv/Scripts/activate
- Install requirements
> pip install -r requirements.txt
- Run all tests
> pytest --html=report.html

## Tests can be ran separately according to endpoints
- Run smoke tests
> pytest --html=report.html -m smoke
- Run author tests
> pytest --html=report.html -m author
- Run title tests
> pytest --html=report.html -m title
- Run combined tests
> pytest --html=report.html -m combined
- Run random tests
> pytest --html=report.html -m random


| Test | Verification |
| ------ | ------ |
| test_get_all_authors | check all authors expected count, check if expected authors exist in all authors, check if fake author not exist in all authors |
| test_get_specific_data_by_author | check if expected poem count is retrieved, check if one expected poem is in the reponse |
| test_get_404_response_on_unknown_author | check if received 404 not found for unknown author |
| test_get_titles_by_keyword | check expected title count, check if expected keyword exists in titles |
| test_get_title_by_exact_match_title | check is exact title returns only one title and check its value |
| test_get_404_response_on_unfound_title_keyword | check if unknown title does not exist and return 404 not found |
| test_get_specific_data_in_text_format_by_title | check if returned data is in text format and all expected values are in the response |
| test_get_data_of_three_random_poems | check if three elements are received, check if all poems are having the set fields (author, title, linecount) |
| test_get_combined_data_by_title_author_linecount_and_poem_count | check if combined endpoint returns correct data (correct expected title keyword, author, lines count and poem count |

Every response has a check if request was sent correctly "assert_correct_response(response)".

After test succeeds a report will be generated in main folder (**report.html**).