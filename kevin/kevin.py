import json
import click
import logging
from config import config
from modules.generator import apply_change, find_matching_files, perform_task
from modules.git import commit_code
from modules.linter import execute_lint, fix_lint, read_lint_output
from config import ModelConfig, config
from modules.llm import send_message
from modules.prisma import find_prisma, read_prisma

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

history = []

# Function to generate code
@click.command(help="Generate new code based on given templates.")
@click.option('--template', default=None, 
              help='Specify a template for code generation.')
def generate_code(template):
    """Generate new code based on given templates."""
    # read the project definition
    project_def = config.get('project')
    try:
        prisma_path = find_prisma(config.get('dir'))
        if prisma_path is None:
            click.echo("Warning. Prisma schema file not found.")
        else:
            prisma_def = read_prisma(prisma_path)
            click.echo(f"Loaded Prisma schema file: {prisma_path}")
        with open(f"templates/{project_def}.json", 'r') as f:
            project_data = json.load(f)
            click.echo(f"Loaded project: {project_data.get('name')}...")
            click.echo("Available tasks:")
            # display all available tasks
            tasks = project_data.get('tasks')
            for i, task in enumerate(tasks):
                click.echo(f"{i+1}. {task.get('name')}")
            click.echo("0. back")
            # prompt user to select a task
            task_index = click.prompt(f"Enter your choice (1-{len(tasks)}) ", type=int)
            click.echo(f"Selected task: {project_data.get('tasks')[task_index].get('name')}")
            if task_index == 0:
                return
            
            # select a model from the Prisma schema
            click.echo("Which model to you want to use:")
            for i, model in enumerate(prisma_def):
                click.echo(f"{i+1}. {model.get('name')}")
            click.echo("0. back")
            model_index = click.prompt(f"Enter your choice (1-{len(prisma_def)}) ", type=int)
            if model_index == 0:
                return
            model = prisma_def[model_index-1]
            task = tasks[task_index-1]
            click.echo(f"Running '{task.get('name')}' on '{model.get('name')}' model...")
            # generate code
            result = perform_task(task, model)
            click.echo("Code generation completed.")
            click.echo("Files created:")
            click.echo(f"  - {'\n  - '.join(result)}")
            history.append(f"Generated code for task '{task.get('name')}' on model '{model.get('name')}'")
    except Exception as e:        
        click.echo(f"Error: {e}")
        return

# Function to update code
@click.command(help="Update a code with the given instruction.")
@click.option('--file', default=None, 
              help='Specify the file to update.', )
def update(file):
    """Update a code with the given instruction."""
    keyword = ""
    while len(keyword) < 3:
        keyword = click.prompt("Please enter search term in filename")
        if (len(keyword) < 3):
            click.echo("Keyword must be at least 3 characters.")
    # find all the files that contain the keyword
    matching_files = find_matching_files(keyword)
    if len(matching_files) == 0:
        click.echo("No files found.")
        return
    # prompt user to select a file
    click.echo("Select a file to update:")
    for i, file in enumerate(matching_files):
        click.echo(f"{i+1}. {file}")
    click.echo("0. back")
    file_index = click.prompt(f"Enter your choice (1-{len(matching_files)}) ", type=int)
    if file_index == 0:
        return
    file_path = matching_files[file_index-1]
    click.echo(f"Selected file: {file_path}")    
    intruction = ""
    instruction = click.prompt("Please tell me the change you want to perform")
    if (len(instruction) < 3):
        click.echo("Instruction must be at least 3 characters.")
        return

    result = apply_change(file_path, instruction)
    if result:
        click.echo("Code updated successfully.")
        history.append(f"Updated code in file '{file_path}' with instruction '{instruction}'")
    else:
        click.echo("Failed to update code.")

# Function to fix code
@click.command(help="Fix warnings or errors in a code.")
@click.option('--file', default=None, 
              help='Specify the file to fix.')
def fix(file):
    """Fix warnings or errors in a code."""
    lint_result = execute_lint()
    errors = read_lint_output(lint_result)
    # remove entries with blank keys
    errors = {k: v for k, v in errors.items() if k}
    if len(errors) == 0:
        click.echo("No errors found.")
        return
    click.echo(f"There are {len(errors)} files with warnings/errors found.")
    success_records = []
    # run fix for every file    
    for file_path, messages in errors.items():
        result = fix_lint(file_path, messages)
        if result:
            success_records.append(file_path)          
    # add result to the history
    if len(success_records) > 0:
        history.append("Applied fixes to lint issues found on the following files: " + 
                       ", ".join(success_records))
        click.echo(f"Fixing completed. {len(success_records)} files fixed.")
        click.echo("Files fixed:")
        click.echo(f"  - {'\n  - '.join(success_records)}")
    else:
        click.echo("No fixes applied.")

# Function to commit code
@click.command(help="Issue commit to git repository.")
@click.option('--message', default=None, 
              help='Specify the commit message.')
def commit(message):
    """Send commit to git repository."""
    result = commit_code(history)
    if result:
        click.echo("Successfully committed code to Git.")
    else:
        click.echo("Failed to commit code to Git.")

# Function to send a hello message to the AI model
@click.command(help="Sends a hello message to the AI model. Execute to test your LLM configuration.")
def hello_ai():
    """
    Sends a hello chat message to the AI model.
    """
    click.echo("")
    click.echo("You: Hello. How are you?")
    ModelConfig.update_temperature(temperature=0.8)
    response = send_message("hello_kevin", 
                                   {"human":"Hello. How are you?"})
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

# setup the logging
logger = logging.getLogger(__name__)

@click.command()
@click.option('--dir', default=config.get('dir'), prompt='Base project directory',
              help='The root of the project directory')
def begin(dir):
    logging.basicConfig(filename='logs/kevin.log', level=logging.INFO)

    welcome_greeting()

    while True:
        # Display menu options
        click.echo("")
        click.echo("select an option (1-6):")
        click.echo("1. generate code")
        click.echo("2. update")
        click.echo("3. lint & fix")
        click.echo("4. commit")
        click.echo("5. help")
        click.echo("6. hello AI")
        click.echo("0. exit")

        # Get user input and execute the corresponding command
        try:
            option = int(click.prompt("Enter your choice", type=int))
            click.echo("")

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
