# Makefile

# Install dependencies using pip
install:
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt

# Format the code using Black
format:
	black src/ tests/

# Lint the code using Pylint
lint:
	pylint --disable=R,C src/

# Run tests with pytest and code coverage
test:
	python -m pytest -vv --cov=tests/
