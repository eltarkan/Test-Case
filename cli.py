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


if __name__ == "__main__":
    cli.add_command(start_server)
    cli()
