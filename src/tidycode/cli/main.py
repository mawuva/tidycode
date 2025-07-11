"""
Main CLI
"""
import typer


app = typer.Typer(help="Tidycode is a tool to help you keep your code clean and tidy.")

@app.command()
def main():
    """Main CLI function."""
    typer.echo("Hello, world!")


if __name__ == "__main__":
    app()




