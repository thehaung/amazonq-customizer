import typer

app = typer.Typer()

@app.command()
def init():
    """Initialize Amazon Q directories."""
    pass

@app.command()
def convert():
    """Convert skills to Amazon Q Prompts."""
    pass

if __name__ == "__main__":
    app()