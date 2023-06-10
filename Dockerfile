FROM python:3.9

COPY requirements.txt ./requirements.txt

COPY config.yaml ./config.yaml

COPY main.py ./main.py

COPY features.py ./features.py

COPY model.py ./model.py

COPY test.py ./test.py

RUN pip install --upgrade pip

RUN pip install numpy

RUN python -m pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113

RUN pip install -r requirements.txt

CMD python main.py