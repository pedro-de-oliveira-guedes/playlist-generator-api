run:
	docker build -t playlist-generator-api .
	docker run -d -p 52055:52055 --name playlist-generator-api playlist-generator-api

stop:
	docker stop $(shell docker ps -q --filter ancestor=playlist-generator-api)
