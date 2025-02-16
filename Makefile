run:
	python manage.py runserver

migrate:
	python manage.py migrate

migrate-tubiao:
	python manage.py makemigrations

# Docker 相关命令

docker-build:
	docker buildx create --use --name multi-platform-builder || true
	docker buildx build --platform linux/amd64,linux/arm64 -t bluedocker123/stock-app --push .

docker-run:
	docker run -d --name stock-container -p 8000:8000 -e DJANGO_ALLOWED_HOSTS="*" stock-app

docker-stop:
	docker stop stock-container

docker-remove:
	docker rm stock-container

docker-clean:
	docker system prune -f

# docker.io/bluedocker123/stock-app
docker-push:
	docker tag stock-app bluedocker123/stock-app
	docker push bluedocker123/stock-app
	


# 一键部署命令
docker-deploy: docker-build docker-run