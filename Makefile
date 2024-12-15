.PHONY: test coverage

test: test-unit test-integration

test-unit: 
	python -m pytest tests/unit

test-integration: 
	python -m pytest tests/integration

coverage:
	python -m pytest -s --cov-config=.coveragerc --cov-report html --cov-branch --cov=oddsportal tests/
