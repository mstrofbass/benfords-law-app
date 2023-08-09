dev:
	flask run --debug

test:
	ptw -- --cov

docker-build:
	docker build . -t bds-benfords

docker-run:
	docker run -rf -p 5001:5000 bds-benfords
