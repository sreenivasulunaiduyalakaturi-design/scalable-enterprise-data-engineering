install:  ; pip install pyspark pyyaml pytest
data:     ; python -m src.generate_data
run:      ; python -m src.main --stage all
test:     ; python -m pytest -q
docker:   ; docker build -t sales-pipeline . && docker run --rm sales-pipeline
