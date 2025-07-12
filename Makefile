.PHONY: test-purchase test-owner test-all

test-purchase:
	docker compose run --rm purchase-service sh -c "./wait-for-db.sh db pytest tests/"

test-owner:
	docker compose run --rm owner-service sh -c "./wait-for-db.sh db pytest tests/"

test-all: test-purchase test-owner