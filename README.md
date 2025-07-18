Run all tests
pytest

Run test with markers
pytest -m positive
pytest -m negative
pytest -m schema

html report
pytest --html=reports/trial_search_report.html --self-contained-html

File name:
pytest tests/api/test_trial_search.py
