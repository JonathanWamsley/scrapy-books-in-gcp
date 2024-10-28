# Makefile

# Install dependencies using pip
install:
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt

# Format the code using Black
format:
	black src/ tests/
