FROM python:3.8.18

WORKDIR /build/

COPY /src/ /build/
COPY .env /build/
COPY requirements.txt /build/

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

CMD ["python3", "main.py"]
