NAME = inquisitor
SOURCE = inquisitor.py
VENV_DIR = venv
PIP = $(VENV_DIR)/bin/pip

all: $(NAME)

$(NAME): $(SOURCE)
	python -m venv venv
	$(PIP) install -r requirements.txt
	$(VENV_DIR)/bin/pyinstaller --onefile --name=$(NAME) $(SOURCE)

compose:
	docker compose up --build -d

single:
	docker build -f Dockerfile.attacker -t $(NAME) .

start:
	docker run -d --name tedelin inquisitor
	docker exec -it tedelin bash

stop:
	docker kill tedelin
	docker rm -f tedelin

compose-stop:
	docker compose down

clean: stop
	rm -rf $(VENV_DIR) dist build $(NAME).spec

re: clean all

.PHONY: all build start run stop clean
