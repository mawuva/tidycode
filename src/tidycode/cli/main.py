"""
Main CLI
"""
import typer

from .commands import hooks, commitizen, dependabot, configs


app = typer.Typer(help="Tidycode is a tool to help you keep your code clean and tidy.")

app.add_typer(hooks.app, name="hooks")
app.add_typer(commitizen.app, name="commitizen")
app.add_typer(dependabot.app, name="dependabot")
app.add_typer(configs.app, name="configs")

def main():
    app()

if __name__ == "__main__":
    main()




