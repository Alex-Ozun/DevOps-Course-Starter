build:
ifdef dev
	docker build --target development --tag todo-app:dev .
else
	docker build --target production --tag todo-app:prod .
endif

run:
ifdef dev
	docker run -p 80:5050 --mount type=bind,source=`pwd`,target=/todo-app --env-file ./.env todo-app:dev
else
	docker run -p 80:5050 --env-file ./.env todo-app:prod
endif
	