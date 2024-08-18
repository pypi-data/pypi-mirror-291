import typer,utils as utils_cli
from pprint import pprint
from cryptography.fernet import Fernet
import spartaqube_cli as spartaqube_cli
app=typer.Typer()
@app.command()
def sparta_fe20d40805(port=None):spartaqube_cli.runserver(port)
@app.command()
def list():spartaqube_cli.list()
@app.command()
def sparta_5fc6b5adde():spartaqube_cli.sparta_5fc6b5adde()
@app.command()
def sparta_efd20b0c60(ip_addr,http_domain):A=spartaqube_cli.token(ip_addr,http_domain);print(A)
@app.command()
def sparta_958ca2a3b8():print('Hello world!')
if __name__=='__main__':app()