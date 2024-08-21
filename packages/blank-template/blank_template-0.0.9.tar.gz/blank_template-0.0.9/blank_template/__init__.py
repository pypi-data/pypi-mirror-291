import typer

app = typer.Typer(add_completion=False)


@app.command()
def main() -> int:
    print("Hello from blank-template!")
    return 0
