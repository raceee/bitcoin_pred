FROM python:3.9-alpine

COPY requirements.txt ./requirements.txt

COPY keys.yaml ./keys.yaml

COPY main.py ./main.py

COPY features.py ./features.py

COPY model.py ./model.py

RUN pip install -requirements.txt

RUN ["python", "-u", "./main.py"]