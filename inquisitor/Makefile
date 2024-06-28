NAME = inquisitor

all: $(NAME)

$(NAME): $(SOURCE)
	docker compose up --build -d


client:
	docker exec -it client bash

attacker:
	docker exec -it attacker bash

clean:
	docker compose down

re: clean all

.PHONY: all client attacker clean
