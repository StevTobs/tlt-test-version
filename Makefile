# Define variables
VENV_DIR=venv
PIP=$(VENV_DIR)/bin/pip
PYTHON=$(VENV_DIR)/bin/python
ifeq ($(OS),Windows_NT)
    PIP=$(VENV_DIR)/Scripts/pip
    PYTHON=$(VENV_DIR)/Scripts/python
endif

# Default target
.PHONY: all
all: setup install-requirements

# Create virtual environment
$(VENV_DIR):
	python3 -m venv $(VENV_DIR)

# Install requirements from requirements.txt
.PHONY: install-requirements
install-requirements: $(PIP)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Copy requirements.txt (placeholder, typically managed by version control)
.PHONY: copy-requirements
copy-requirements:
	@echo "Ensure requirements.txt is in the current directory"

# Setup target
.PHONY: setup
setup: $(VENV_DIR) copy-requirements install-requirements

# Run the Django server
.PHONY: run
run:
	if [ -f manage.py ]; then $(PYTHON) manage.py runserver 0.0.0.0:8001; else echo "manage.py not found!"; exit 1; fi

# Clean target: remove the virtual environment
.PHONY: clean
clean:
	rm -rf $(VENV_DIR)

# Freeze dependencies into requirements.txt
.PHONY: freeze
freeze:
	$(PIP) freeze > requirements.txt

# Activate virtual environment (manual)
.PHONY: on-env
on-env:
	@echo "Run 'source $(VENV_DIR)/bin/activate' to activate the virtual environment. (For Windows '/./\venv\Scripts\Activate')"

# Deactivate virtual environment (manual)
.PHONY: off-env
off-env:
	@echo "Run 'deactivate' to deactivate the virtual environment."

# Test target
.PHONY: test
test:
	$(PYTHON) manage.py test


#Load data
.PHONY: load-data
load-data:
	$(PYTHON) manage.py load_data resources/area_data/api_province_with_amphure_tambon.json

#Load data
.PHONY: load-data-pea
load-data-pea:
	$(PYTHON) manage.py load_data resources/area_data/api_province_with_amphure_tambon_pea_area.json