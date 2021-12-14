import click
from modern_ftp.ftp import FTPServer

@click.command()
@click.option("-p", "--port", default=2323)
@click.option("-h", "--host", default="127.0.0.1")
def main(host: str, port: int) -> None:
    FTPServer(host, port).serve()
