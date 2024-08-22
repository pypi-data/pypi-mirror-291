import click
from .db import download_schema, generate_profiles

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
@click.option('--dbname', required=True, help='Database name.')
@click.option('--user', required=True, help='Database user.')
@click.option('--password', required=True, help='Database password.')
@click.option('--host', default='localhost', help='Database host.')
@click.option('--port', default='5432', help='Database port.')
def run(dbname, user, password, host, port):
    """Run all database operations."""
    download_schema(dbname, user, password, host, port)
    generate_profiles()

if __name__ == '__main__':
    cli()