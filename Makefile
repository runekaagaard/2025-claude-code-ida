.PHONY: build serve clean

build:
	python build.py

serve: build
	uv run uvicorn server:app --reload --port 8000

clean:
	rm -rf build/
