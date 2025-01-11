run:
	docker build -t playlist-generator-api .
	docker rm -f playlist-generator-api || true
	docker run -d -p 7777:7777 --name playlist-generator-api playlist-generator-api

stop:
	docker stop $(shell docker ps -q --filter ancestor=playlist-generator-api)
