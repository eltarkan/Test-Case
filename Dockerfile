FROM python:3.10.0

WORKDIR /app

COPY ./alembic.ini /app/alembic.ini
COPY ./alembic /app/alembic
COPY ./migrations /app/migrations
COPY ./src /app/src

COPY ./cli.py /app/cli.py
COPY ./main.py /app/main.py
COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt
EXPOSE 8000

RUN python cli.py migrate

ENTRYPOINT ["python", "cli.py", "start-server", "--reload"]
