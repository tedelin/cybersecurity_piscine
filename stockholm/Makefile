NAME = stockholm
SOURCE = stockholm.py
VENV_DIR = venv
PIP = $(VENV_DIR)/bin/pip

all: $(NAME)

$(NAME): $(SOURCE)
	python -m venv venv
	$(PIP) install -r requirements.txt
	$(VENV_DIR)/bin/pyinstaller --onefile --name=$(NAME) $(SOURCE)
	docker build -t $(NAME) .

start: stop
	docker run -d --name tedelin stockholm
	docker exec -it tedelin bash

stop:
	if [ $$(docker ps -aq) ]; then docker kill tedelin; docker rm -f tedelin; fi

clean: 
	rm -rf $(VENV_DIR) dist build $(NAME).spec

re: clean all

.PHONY: all build start run stop clean
