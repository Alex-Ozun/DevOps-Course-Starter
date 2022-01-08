all:
	docker build --target production --tag todo-app:prod .
	docker run -p 80:5050 --env-file ./.env todo-app:prod
