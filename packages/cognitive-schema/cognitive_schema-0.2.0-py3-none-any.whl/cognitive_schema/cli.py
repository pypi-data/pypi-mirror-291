import click
import click_spinner
from .db import download_schema, generate_profiles
from .query import load_profiles, construct_prompt, query_openai

@click.group()
def cli():
    """An AI driven CLI tool for database operations."""
    pass

@cli.command()
@click.option('--dbname', required=True, help='Database name.')
@click.option('--user', required=True, help='Database user.')
@click.option('--password', required=True, help='Database password.')
@click.option('--host', default='localhost', help='Database host.')
@click.option('--port', default='5432', help='Database port.')
def download(dbname, user, password, host, port):
    """Download the database schema."""
    download_schema(dbname, user, password, host, port)

@cli.command()
def profile():
    """Generate database profiles."""
    generate_profiles()

@cli.command()
@click.option('--query', required=True, help='The query to ask about the database schemas.')
def query(query):
    """Query the database schemas using the profiles as context."""
    profiles_path = "./db/profiles/"
    profiles_content = load_profiles(profiles_path)
    if profiles_content is None:
        click.echo("No profiles found. Please generate profiles first.")
        return
    prompt = construct_prompt(profiles_content, query)

    with click_spinner.spinner('Querying the database schemas...'):
        response = query_openai(prompt)

    response = query_openai(prompt)
    if response:
        click.echo(response)

if __name__ == '__main__':
    cli()