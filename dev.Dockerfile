FROM python:3.10.0

WORKDIR /app

COPY ./cli.py /app/cli.py
COPY ./main.py /app/main.py
COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt
EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
