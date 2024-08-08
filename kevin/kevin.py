import click
import json
from config import config
from modules.linter import execute_lint, read_lint_output
from config import ModelConfig, config
from modules.llm import send_message

def welcome_greeting():
    kevin_art = [
        "                                      ",
        "     Watch out Devin, here comes...   ", 
        "                                      ",
        "██╗  ██╗███████╗██╗   ██╗██╗███╗   ██╗",
        "██║ ██╔╝██╔════╝██║   ██║██║████╗  ██║",
        "█████╔╝ █████╗  ██║   ██║██║██╔██╗ ██║",
        "██╔═██╗ ██╔══╝  ╚██╗ ██╔╝██║██║╚██╗██║",
        "██║  ██╗███████╗ ╚████╔╝ ██║██║ ╚████║",
        "╚═╝  ╚═╝╚══════╝  ╚═══╝  ╚═╝╚═╝  ╚═══╝",
        "                                      ",
    ]

    for line in kevin_art:
        print(line)

# Function to generate code
@click.command(help="Generate new code based on given templates.")
@click.option('--template', default=None, 
              help='Specify a template for code generation.')
def generate_code(template):
    """Generate new code based on given templates."""
    if template is None:
        template = click.prompt("Enter the template name", type=str)
    click.echo(f"Generating new code using the template: {template}")

# Function to update code
@click.command(help="Update a code with the given instruction.")
@click.option('--file', default=None, 
              help='Specify the file to update.', )
def update(file):
    """Update a code with the given instruction."""
    if file is None:
        file = click.prompt("Enter the file name to update", type=str)
    click.echo(f"Updating code in the file: {file}")

# Function to fix code
@click.command(help="Fix warnings or errors in a code.")
@click.option('--file', default=None, 
              help='Specify the file to fix.')
def fix(file):
    """Fix warnings or errors in a code."""
    lint_result = execute_lint()
    print("-----------------")
    print(lint_result)
    print("=================")
    errors = read_lint_output(lint_result)
    print(json.dumps(errors, indent=2))


# Function to commit code
@click.command(help="Issue commit to git repository.")
@click.option('--message', default=None, 
              help='Specify the commit message.')
def commit(message):
    """Send commit to git repository."""
    if message is None:
        message = click.prompt("Enter the commit message", type=str)
    click.echo(f"Committing code to the git repository with message: {message}")



# Function to send a hello message to the AI model
@click.command(help="Sends a hello message to the AI model. Execute to test your LLM configuration.")
def hello_ai():
    """
    Sends a hello chat message to the AI model.
    """
    click.echo("")
    click.echo("You: Hello. Who are you?")
    ModelConfig.update_temperature(temperature=0.8)
    response = send_message("hello_kevin", "Hello. How are you?")
    click.echo(f"Kevin: {response}")
    ModelConfig.update_temperature(temperature=0)
    
# Main CLI group to combine all commands
@click.group()
def cli():
    pass

# initialize the LLM model to use
ModelConfig.initialize_model()

# Add commands to the CLI group
cli.add_command(generate_code)
cli.add_command(update)
cli.add_command(fix)
cli.add_command(commit)
cli.add_command(hello_ai)

@click.command()
@click.option('--dir', default=config.get('dir'), prompt='Base project directory',
              help='The root of the project directory')
def begin(dir):
    welcome_greeting()

    while True:
        # Display menu options
        click.echo("")
        click.echo("select an option (1-6):")
        click.echo("1. generate code")
        click.echo("2. update")
        click.echo("3. fix")
        click.echo("4. commit")
        click.echo("5. help")
        click.echo("6. hello AI")
        click.echo("0. exit")

        # Get user input and execute the corresponding command
        try:
            option = int(click.prompt("Enter your choice", type=int))

            if option == 1:
                generate_code.main(standalone_mode=False)
            elif option == 2:
                update.main(standalone_mode=False)
            elif option == 3:
                fix.main(standalone_mode=False)
            elif option == 4:
                commit.main(standalone_mode=False)
            elif option == 5:
                click.echo(cli.get_help(click.Context(cli)))
            elif option == 6:
                hello_ai.main(standalone_mode=False)
            elif option == 0:                
                click.echo("Bye! Exiting now...")
                break
            else:
                click.echo("Invalid option. Please enter a number between 1 and 6. Type 0 to exit.")
        except ValueError:
            click.echo("Invalid input. Please enter a number.")


if __name__ == '__main__':
    begin()
