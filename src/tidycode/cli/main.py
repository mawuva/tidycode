"""
Main CLI
"""
import typer

from .commands import hooks, commitizen, dependabot, configs, clean


app = typer.Typer(help="Tidycode is a tool to help you keep your code clean and tidy.")

app.add_typer(hooks.app, name="hooks")
app.add_typer(commitizen.app, name="commitizen")
app.add_typer(dependabot.app, name="dependabot")
app.add_typer(configs.app, name="configs")
app.add_typer(clean.app, name="clean")

def main():
    app()

if __name__ == "__main__":
    main()




