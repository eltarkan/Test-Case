import click
import os


@click.group()
def cli():
    pass


@click.command()
@click.option('--reload', is_flag=True, help="Reload Uvicorn")
def start_server(reload):
    uvicorn_command = "uvicorn main:app --host 0.0.0.0 --port 8000"
    if reload:
        uvicorn_command += " --reload"

    click.echo(f"Uvicorn is starting 🚀: {uvicorn_command}")
    os.system(uvicorn_command)


@click.command()
@click.option('--name', is_flag=True, help="Create a new migration")
def create_migration(name):
    click.echo(f"Creating migration: {name}")
    os.system(f"alembic revision --autogenerate -m '{name}'")


@click.command()
def run_migrations():
    click.echo(f"Running migrations")
    os.system(f"alembic upgrade head")


if __name__ == "__main__":
    cli.add_command(start_server)
    cli.add_command(create_migration)
    cli.add_command(run_migrations)
    cli()
