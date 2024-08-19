import typer,utils as utils_cli
from pprint import pprint
from cryptography.fernet import Fernet
import spartaqube_cli as spartaqube_cli
app=typer.Typer()
@app.command()
def sparta_614be56fe7(port=None):spartaqube_cli.runserver(port)
@app.command()
def list():spartaqube_cli.list()
@app.command()
def sparta_f5be1a18c1():spartaqube_cli.sparta_f5be1a18c1()
@app.command()
def sparta_fe0d9a0f01(ip_addr,http_domain):A=spartaqube_cli.token(ip_addr,http_domain);print(A)
@app.command()
def sparta_e2583ab2a6():print('Hello world!')
if __name__=='__main__':app()