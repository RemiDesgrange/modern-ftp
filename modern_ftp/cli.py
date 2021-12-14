import click
from modern_ftp.ftp import FTPServer
from modern_ftp.queue import TestListener

@click.command()
@click.option("-p", "--port", default=2323)
@click.option("-h", "--host", default="127.0.0.1")
def main(host: str, port: int) -> None:
    FTPServer(host, port).serve()


@click.command()
def listen():
    TestListener('ftp').listen()
