install:
	pip install -r requirements.txt
	cd frontend && npm install

run-api:
	python -m uvicorn api.main:app --reload

run-frontend:
	cd frontend && npm run dev
