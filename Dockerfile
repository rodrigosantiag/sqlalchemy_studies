FROM python:3.11

WORKDIR /app

COPY requirements.txt .
COPY src .
COPY Makefile .

RUN make install

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
